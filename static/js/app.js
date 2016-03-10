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

            setEvents();
        }
    });

    var urlSplit = window.location.pathname.split("/");
    $.get( "/api/v1/models/" + urlSplit[2] + "/versions/" + urlSplit[4], function( data ) {

        for(var i=0;i<data.diagrams.length;i++) {
            var option = "<li><a href='/models/" +urlSplit[2] 
                + "/versions/" +urlSplit[4] 
                + "/diagrams/" + data.diagrams[i].id + "'>" + data.diagrams[i].name + "</a></li>"

            $('.models').append(option);
        }
    });
});