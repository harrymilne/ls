$(document).ready(function(){
{% for i in server_num %}
	$("#server{{ i }}").click(function() {
		$("#server{{ i }}list").slideToggle("fast", "linear");
	});
{% endfor %}
});