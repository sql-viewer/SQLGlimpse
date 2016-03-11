$(".glimpse-container").click(function(e) {
	$(".sqlv-table-selected").("sqlv-table-selected");

 	$(e.target).parents(".sqlv-table").addClass("sqlv-table-selected");

	if ($(e.target).hasClass("sqlv-table")) {
		$(e.target).addClass("sqlv-table-selected");
	}
});

$("#footer-header").click(function() {
    if ( $("#footer").height() != 30) {
    	$( "footer-header" ).text('see more');
        $( "#footer" ).animate({ height: 30 }, 600 );
    }
    else {
    	$( "footer-header" ).text('see less');
    	$( "#footer" ).animate({ height: 500 }, 600 );
    }
});

function setEvents() {
    
    setEventsForFullConnections();

    setEventsForSplitConnections();

}

function setEventsForFullConnections() {
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

function setEventsForSplitConnections() {
    var hoverClass = "sqlv-selected-row-hover";
    var selectedClass = "sqlv-selected-row";

    $(".svg-link-split").mouseover(function() {
        var data = $(this).data();
        selectLinkSplit(data,hoverClass);
    }); 

    $(".svg-link-split").mouseout(function() {
        var data = $(this).data();
        deselectLinkSplit(data, hoverClass);
    });

    $(".svg-link-split").click(function() {
        var data = $(this).data();
        var hasSelectedClass = sessionStorage.getItem($(this).attr('id'));

        if (hasSelectedClass == null || hasSelectedClass == "false") {
            selectLinkSplit(data, selectedClass); 
            sessionStorage.setItem($(this).attr('id'), "true");

            //turn off mouseoff event
            $(this).off("mouseout");

        }
        else {
            sessionStorage.setItem($(this).attr('id'), "false");
            deselectLinkSplit(data, selectedClass);

            //turn back on mouseoff event
            $(".svg-link-split").mouseout(function() {
                var data = $(this).data();
                deselectLinkSplit(data, hoverClass);
            });
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

function selectLinkSplit(data, c, linkClass) {
    $("#" + data.linkid).attr("class", "svg-link-hidden-hover " + linkClass); 
    $("#" + data.targetid).addClass(c); 
    $("#" + data.sourceid).addClass(c); 
}

function deselectLinkSplit(data, c) {
    $("#" + data.linkid).attr("class", "svg-link-hidden"); 
    $("#" + data.targetid).removeClass(c); 
    $("#" + data.sourceid).removeClass(c); 
}