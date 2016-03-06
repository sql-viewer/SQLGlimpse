SqlViewer.namespace("SqlViewer.Parser"); 

SqlViewer.Parser = function ( diagram ) {
    if (!(this instanceof SqlViewer.Parser)) {
        return new SqlViewer.Parser(diagram);
    }
	this.diagram = diagram;
    this.tablesData = [];
};

SqlViewer.Parser.prototype.draw = function() {
    this.setTableData();
    this.createMain();
    this.drawLayersAndTables();
    //this.drawLinks();
}

SqlViewer.Parser.prototype.drawLayersAndTables = function() {
    
    for (var i = 0; i < this.diagram.layers.length; i++) {
        var layer = this.diagram.layers[i];
        var canvas = new SqlViewer.Canvas(
            layer.element.x,
            layer.element.y,
            layer.element.height,
            layer.element.width,
            layer.element.color,
            layer.name);
        canvas.draw();

        this.drawTables(layer.tables, layer.element.x, layer.element.y );
    }; 
}

SqlViewer.Parser.prototype.drawTables = function(tables, canvasX, canvasY) {
    if (tables.length > 0) {
        for (var i = 0; i < tables.length; i++) {
            var table = tables[i];
            var tableData = this.tablesData[table.tableId];

            var tab = new SqlViewer.Table(
                table,
                canvasX,
                canvasY,
                tableData
            );
            tab.draw();
        }
    }
}

SqlViewer.Parser.prototype.setTableData = function() {
	var tables = this.diagram.data.tables;
	for (var i = 0; i < tables.length; i++) {
        this.tablesData[tables[i].id] = tables[i];
	}
}

SqlViewer.Parser.prototype.getLinksData = function(data) {

    var retVal = [];
    for (var i = 0; i < data.links.length; i++) {
        retVal[data.links[i].id] = data.links[i];
    }

    return retVal;
}

SqlViewer.Parser.prototype.createMain = function() {
   var height = this.getHeight() + this.getHeight()*0.2;
   var widht = this.getWidht()+ this.getHeight()*0.2;

   $("#main").width(widht).height(height );
}

SqlViewer.Parser.prototype.drawLinks = function() {
    //console.log(this.links);

    //id,source, destination, type, draw

    for (var linkId in this.links) {
        var l = this.links[linkId];

        var link = new SqlViewer.Link(
            l.id,
            l.source,
            l.destination,
            l.type,
            null
        );

        link.draw();
    }
}

SqlViewer.Parser.prototype.getHeight = function() {
    var sortedArray = this.diagram.layers.sort(function(a , b) {
        return a.element.y - b.element.y; 
    });

    return sortedArray[sortedArray.length-1].element.y + 
        sortedArray[sortedArray.length-1].element.height;
}

SqlViewer.Parser.prototype.getWidht = function() {
    var sortedArray = this.diagram.layers.sort(function(a , b) {
        return a.element.x - b.element.x; 
    });

    return sortedArray[sortedArray.length-1].element.x + 
        sortedArray[sortedArray.length-1].element.width;
}
