$( document ).click(function(e) {
	$(".sqlv-table-selected").removeClass("sqlv-table-selected");

 	$(e.target).parents(".sqlv-table").addClass("sqlv-table-selected");

	if ($(e.target).hasClass("sqlv-table")) {
		$(e.target).addClass("sqlv-table-selected");
	}
});