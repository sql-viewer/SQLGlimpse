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
    
    $(".svg-hoverlink").mouseover(function() {
        var data = $(this).data();
        selectLink(data);
    }); 

    $(".svg-hoverlink").mouseout(function() {
        var data = $(this).data();
        deselectLink(data);
    });

    // $(".svg-hoverlink").click(function() {
    //     var data = $(this).data();
    //     selectLink(data); 
    // });

    // $(".svg-hoverlink").dblclick()(function() {
    //     var data = $(this).data();
    //     console.log(data);
    //     deselectLink(data); 
    // });
}

function selectLink(data) {
    $("#" + data.linkid).attr("class", "svg-link svg-link-hover"); 
    $("#" + data.targetid).addClass("sqlv-selected-row"); 
    $("#" + data.sourceid).addClass("sqlv-selected-row"); 
}

function deselectLink(data) {
    $("#" + data.linkid).attr("class", "svg-link"); 
    $("#" + data.targetid).removeClass("sqlv-selected-row"); 
    $("#" + data.sourceid).removeClass("sqlv-selected-row"); 
}