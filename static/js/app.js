$( document ).ready(function() {
	var url = '/api/v1' + window.location.pathname;
    $('#loading').html('<img src="/static/img/load.gif">');
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        success: function (d) {
			console.log(d);
			var p = new SqlViewer.Parser(d)
			p.draw();
        	$('#loading').html("");
        }
    });
});