$( document ).ready(function() {
	var url = '/api/v1' + window.location.pathname;
	$.get( url, function( data ) {
		console.log(data);
		var p = new SqlViewer.Parser(data)
		p.draw();
	});
});

