SqlViewer.namespace("SqlViewer.Link"); 
SqlViewer.Link = function (id,source, destination, type, visible) {
    if (!(this instanceof SqlViewer.Link)) {
        return new SqlViewer.Link(id,source, destination, type, visible);
    }

    this.id = id;
    this.source = source
    this.destination = destination;
    this.type = type;
    this.visible = visible || "full";
};


SqlViewer.Link.prototype.draw = function() {
    
    if (this.type === "COLUMN") {
        this.drawColumnLink();
    }
    else if (this.type === "TABLE") {
        this.drawTableLink();
    }
}

SqlViewer.Link.prototype.drawColumnLink = function() {

    var sourceColumn = $("#" + this.source.columnId);
    var sx = sourceColumn.parent().position().left;
    var sy = sourceColumn.position().top + (sourceColumn.height() / 2);
    

    var destinationColumn = $("#" + this.destination.columnId);
    var dx = destinationColumn.parent().position().left + destinationColumn.width()+10;
    var dy = destinationColumn.position().top + (destinationColumn.height() / 2);
    

    SqlViewer.draw.line(sx,sy,dx,dy).stroke({ width: 5 }).attr({ "stroke-dasharray" : "10 5", class : "svg-link" });
    SqlViewer.draw.rect(10,4).attr({ x: sx-10, y: sy, class : "svg-link"});
    SqlViewer.draw.rect(10,4).attr({ x: dx, y: dy, class : "svg-link"});
}

SqlViewer.Link.prototype.drawTableLink = function() {
    console.log('TODO: drawTableLink');
}