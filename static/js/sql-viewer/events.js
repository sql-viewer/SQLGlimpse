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

function setEvents() {
    
    var hoverClass = "sqlv-selected-row-hover";
    var selectedClass = "sqlv-selected-row";

    $(".svg-hoverlink").mouseover(function() {
        var data = $(this).data();
        selectLink(data,hoverClass);
    }); 

    $(".svg-hoverlink").mouseout(function() {
        var data = $(this).data();
        deselectLink(data, hoverClass);
    });

    $(".svg-hoverlink").click(function() {
        var data = $(this).data();
        var hasSelectedClass = sessionStorage.getItem($(this).attr('id'));

        if (hasSelectedClass == null || hasSelectedClass == "false") {
            selectLink(data, selectedClass); 
            sessionStorage.setItem($(this).attr('id'), "true");
        }
        else {
            sessionStorage.setItem($(this).attr('id'), "false");
            deselectLink(data, selectedClass);
        }
    });
}

function selectLink(data, c) {
    $("#" + data.linkid).attr("class", "svg-link svg-link-hover"); 
    $("#" + data.targetid).addClass(c); 
    $("#" + data.sourceid).addClass(c); 
}

function deselectLink(data, c) {
    $("#" + data.linkid).attr("class", "svg-link"); 
    $("#" + data.targetid).removeClass(c); 
    $("#" + data.sourceid).removeClass(c); 
}