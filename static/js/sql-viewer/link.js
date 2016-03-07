SqlViewer.namespace("SqlViewer.Link"); 
SqlViewer.Link = function (link, data) {
    if (!(this instanceof SqlViewer.Link)) {
        return new SqlViewer.Link(link, data);
    }

    this.link = link;
    this.data = data;
};


SqlViewer.Link.prototype.draw = function() {
    if (this.data.type = "column") {
        this.drawColumnLink();
    }
}

SqlViewer.Link.prototype.drawColumnLink = function() {
    var correction = $(".glimpse-container").position();

    var sourceColumn = $("li[id^='" + this.data.source.columnId +"']");
    var sx = sourceColumn.parent().position().left - correction.left;
    var sy = sourceColumn.position().top + (sourceColumn.height() / 2) - correction.top;
    
    var targetColumn = $("li[id^='" + this.data.target.columnId +"']");
    var tx = targetColumn.parent().position().left - correction.left;
    var ty = targetColumn.position().top + (targetColumn.height() / 2)- correction.top;
    
    var sxCorrection = 0;
    var txCorrection = 0;

    
    if (sx < tx) {
        sx = sx + sourceColumn.width() + 5;

    }
    else {
        sx = sx - 10;
    }

    if (tx < sx) {
        tx = tx + targetColumn.width() + 5;
        txCorrection = 10;
    }
    else {
        tx = tx - 10; 
    }


    if (this.link.element.draw == "full") {

        SqlViewer.draw.line(sx,sy,tx + txCorrection ,ty).stroke({ width: 15, opacity: 0 }).attr({ 
            "class" : "svg-hoverlink",
            "data-linkid" : this.link.id,
            "data-sourceid" : this.data.source.columnId,
            "data-targetid" : this.data.target.columnId,
            "data-linkselected" : "f"
        });

        SqlViewer.draw.line(sx,sy,tx + txCorrection ,ty).stroke({ width: 1 }).attr({ 
            "stroke-dasharray" : "10 5", 
            "class" : "svg-link",
            "id"    : this.link.id
        });
    }
    SqlViewer.draw.rect(10,4).attr({ x: sx, y: sy, class : "svg-link"});
    SqlViewer.draw.rect(10,4).attr({ x: tx, y: ty, class : "svg-link"});
}