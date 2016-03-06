$( document ).click(function(e) {
	$(".sqlv-table-selected").removeClass("sqlv-table-selected");

 	$(e.target).parents(".sqlv-table").addClass("sqlv-table-selected");

	if ($(e.target).hasClass("sqlv-table")) {
		$(e.target).addClass("sqlv-table-selected");
	}
});

$("#footer-header").click(function() {
    if ( $("#footer").height() != 30) {
    	$( this ).text('see more');
        $( "#footer" ).animate({ height: 30 }, 600 );
    }
    else {
    	$( this ).text('see less');
    	$( "#footer" ).animate({ height: 350 }, 600 );
    }
});