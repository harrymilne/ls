from struct import *
from web import Webpage
from markupsafe import escape
from ConfigParser import ConfigParser

import errno
import socket
import binascii
import time
import sys
import traceback
import logging

class LegionsClient:

    def __init__(self):
        self.ip_list = []
        self.server_info = {}

        #Structs
        self.reply_struct       = Struct('BBHHBBH')
        self.server_struct      = Struct('4sH')

        self.byte_struct        = Struct('B')
        self.info_struct_req    = Struct('BBI')

        self.info_struct_resp   = Struct('BBBBH')

        #Network
        self.master_socket  = ("master.legionsoverdrive.com",28002)
        self.game_info_req  = 18
        self.game_ping_req  = 14

        self.game_ping_resp = 16
        self.game_info_resp = 20

    def pack_master(self):
        packet_type     = 6
        flags           = 0
        session         = 0
        key             = 1
        index           = 255
        game_type       = b"Legions: Overdrive"
        game_len        = len(game_type)
        mission_type    = b"any"
        mission_len     = len(mission_type)
        min_players     = 0
        max_players     = 255
        region_mask     = 2
        version         = 0
        status          = 0
        max_bots        = 0
        min_cpu         = 255
        buddy_count     = 0
        buddy_list      = 0

        packet = pack('BBHHBB18sB3sBBiiBBBBB',
             packet_type,
             flags,
             session,
             key,
             index,
             game_len,
             game_type,
             mission_len,
             mission_type,
             min_players,
             max_players,
             region_mask,
             version,
             status,
             max_bots,
             min_cpu,
             buddy_count,
             buddy_list)
        return packet

    def send_master(self, packet):
        data = []
        fail_sleep_len = 15     

        req_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        req_sock.settimeout(5)

        try:
            req_sock.connect(self.master_socket)
            req_sock.send(packet)
            data.append(req_sock.recv(4096))
            print("MSG: {0}".format(binascii.hexlify(data[-1])))
            packet_count = self.reply_struct.unpack_from(data[-1])[-2]
            if packet_count-1 > 0:
                for i in range(packet_count-1):
                    data.append(req_sock.recv(4096))
                    print("MSG: ", binascii.hexlify(data[-1]))
            req_sock.close()
            return data

        except socket.timeout:
            message = "ERR: Master server timed out, will retry..."
            print(message)
            time.sleep(fail_sleep_len)
            return False

        except socket.gaierror:
            message = "ERR: Master server DNS fail, will retry..."
            print(message)
            time.sleep(fail_sleep_len)
            return False

        except socket.error as e:
            if e.errno != errno.ECONNREFUSED:
                print("ERR: Master server refused the connection, will retry...")
            else:
                raise e

        except OSError:
            message = "ERR: Connection error..."
            print(message)
            time.sleep(fail_sleep_len)

    def parse_master(self, data):
        offset = 10
        server_data = []

        for packet in data:
            servers_in_packet = self.reply_struct.unpack_from(packet)[-1]
            for servers in range(servers_in_packet):
                data = self.server_struct.unpack_from(packet, offset = offset)
                server_data.append(data)
                offset += self.server_struct.size

        for server in server_data:
            self.ip_list.append((".".join([str(ord(i)) for i in server[0]]),server[1]))

    def query_master(self):
        packet = self.pack_master()
        master_data = self.send_master(packet)
        if master_data:
            self.parse_master(master_data)
        else:
            self.retry = True


    def pack_single(self, header):
        flags = 2
        session = 0
        return self.info_struct_req.pack(header, flags, session)

    def send_single(self, host, packet):
        data = None
        try:
            req_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            req_sock.connect(host)
            req_sock.send(packet)
            req_sock.settimeout(4)
            data = req_sock.recv(4096)
        except socket.timeout:
            print("ERR: {0} timed out...".format(host))
        except socket.gaierror:
            print("ERR: {0} DNS error...".format(host))
        except socket.error as e:
            if e.errno != errno.ECONNREFUSED:
                print("ERR: {0} refused the connection...".format(host))
            else:
                raise e
        except OSError:
            print("ERR: Connection error...")
        req_sock.close()
        return data

    def parse_single(self, data):
        offset = 1
        if self.byte_struct.unpack_from(data)[0] == self.game_info_resp:
            flags, key = Struct("<BI").unpack_from(data, offset = offset)
            offset += 5

            game_type_len = self.byte_struct.unpack_from(data, offset = offset)[0]
            offset += self.byte_struct.size

            game_type = Struct("<{0}s".format(game_type_len)).unpack_from(data, offset = offset)[0].decode()
            offset += game_type_len

            mission_type_len = self.byte_struct.unpack_from(data, offset = offset)[0]
            offset += self.byte_struct.size

            mission_type = Struct("<{0}s".format(mission_type_len)).unpack_from(data, offset = offset)[0].decode()
            offset += mission_type_len

            mission_name_len = self.byte_struct.unpack_from(data, offset = offset)[0]
            offset += self.byte_struct.size

            mission_name = Struct("<{0}s".format(mission_name_len)).unpack_from(data, offset = offset)[0].decode()
            offset += mission_name_len

            status, player_count, max_players, bot_count, cpu = self.info_struct_resp.unpack_from(data, offset = offset)
            offset += self.info_struct_resp.size
            offset += 3 #unused bytes

            status = bin(status)[2:] #binary to string
            status = '0'*(3-len(status)) + status #turns 1 to 001

            #subscriptable flags
            dedicated = bool(int(status[0]))
            password = bool(int(status[1]))

            raw_players = data[offset:].decode("utf-8", errors="replace").splitlines()

            players = []
            for player in raw_players:
                players.append(str(escape(player[2:-2])))

            return {"mission":mission_name, "gamemode":mission_type, "players":players, "player_count":player_count, "max_players":max_players, "passworded":password}

        elif self.game_ping_resp:
            flags, key, ver_len = Struct("<BIB").unpack_from(data, offset = offset)
            offset += 6

            ver = Struct("<{0}s".format(ver_len)).unpack_from(data, offset = offset)[0]
            offset += ver_len

            curr_ver, min_ver, ver_num, name_len = Struct("<IIIB").unpack_from(data, offset = offset)
            offset += 13

            name = Struct("<{0}s".format(name_len)).unpack_from(data, offset = offset)[0].decode("utf-8")
            offset += name_len

            return name

    def query_all(self):
        game_info_packet = self.pack_single(self.game_info_req)
        game_ping_packet = self.pack_single(self.game_ping_req)
        for server in self.ip_list:
            print("MSG: Querying {0}...".format(server))
            game_ping_data = self.send_single(server, game_ping_packet)
            game_info_data = self.send_single(server, game_info_packet)
            if game_info_data and game_ping_data:
                print("MSG: Success, info and ping recieved.")

                server_name = self.parse_single(game_ping_data)
                server_dict = self.parse_single(game_info_data)
                server_dict["socket"] = server
                self.server_info[server_name] = server_dict
                print("MSG: {0} with {1} players sucessfully parsed.".format(server_name, len(server_dict["players"])))

def get_cfg():
    if "-c" in sys.argv:
        flag_index = sys.argv.index("-c")
        filen = sys.argv[flag_index+1]
        if os.path.exists(filen) and os.path.isfile(filen):
            return filen


if __name__ == "__main__":
    error_count = 0
    ##cfg
    cfg = ConfigParser()
    cfg_file = get_cfg()

    if cfg_file:
        cfg.read(cfg_file)
    else:
        cfg.read("default.cfg")

    ##log
    logging.basicConfig(filename=cfg.get("core", "errors"))


    ##setup webpage editor object
    webpage = Webpage(cfg)
    while True:
        try:
            l_client = LegionsClient()
            l_client.query_master()
            l_client.query_all()
            server_data = l_client.server_info
            webpage.write(server_data)
            print("MSG: Sleeping for 60 seconds...")
            time.sleep(60)
        except KeyboardInterrupt:
            sys.exit()
        except:
            error_count += 1
            logging.exception("")
            if error_count < 5:
                print("ERR: Error has been logged and the script will continue in 5 seconds...")
            else:
                print("ERR: Continuous error, program cannot recover...")
                exit()
            time.sleep(5)

