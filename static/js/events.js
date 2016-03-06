function showModels(id) {
	$.get( "models/" + id, function( data ) {
  		$( ".models" ).html( data );
	});
}
