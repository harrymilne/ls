#ls


This script is built to run with a Torque Master Server, which very little games use. It's been made for a game called Legions: Overdrive which just needed a better way to view servers without launching the game itself.
However, if you do want to run this yourself, here's how to do it.


##Requirements

  * Python 3.3
  * Jinja2
  * Font Awesome for icon support

##Setup

  You'll need to edit the prefs.ini so that "index" points to the HTML file you want to write to.
  The "js" variable in prefs.ini is just the javascript file which contains the JS to create the sliding playerbox effect
  so have that point to your "main.js" file for that HTML page.
  The error variable just points to a file to write errors to, you can leave this as default.
  Timezone is pretty self-explanatory but it's just the difference off GMT time, so add "+4" for instance.
  
##First Run
  Once you have all the prefs set up you'll want to be able to run this (presumably) on some kind of linux dedi, so just    create a screen or tmux and start legions_client.py with python 3.
  That should be it!
  

###To Do
	[x] Legions URI implementation
	[x] Player name box
	[x] Cleaner rewrite with better packet decoding
	[ ] Graphs using Google Graphs?
	[ ] Finish stats implementation (maybe sqldb)
	[x] Better HTML implementation (Jinja)
	[x] Better logger?
	

