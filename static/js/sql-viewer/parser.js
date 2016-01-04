SqlViewer.namespace("SqlViewer.Parser"); 
SqlViewer.Parser = function (data, diagram) {
    if (!(this instanceof SqlViewer.Parser)) {
        return new SqlViewer.Parser(data, diagram);
    }

    this.tableData = this.getTableData(data);
    this.links = this.getLinksData(data);
	this.diagram = diagram;
};

SqlViewer.Parser.prototype.getTableData = function(data) {

	var retVal = [];
	for (var i = 0; i < data.tables.length; i++) {
		retVal[data.tables[i].tableId] = data.tables[i];
	}

	return retVal;
}

SqlViewer.Parser.prototype.getLinksData = function(data) {

    var retVal = [];
    for (var i = 0; i < data.links.length; i++) {
        retVal[data.links[i].id] = data.links[i];
    }

    return retVal;
}

SqlViewer.Parser.prototype.draw = function() {

    this.drawLayers();
    this.drawLinks();
}

SqlViewer.Parser.prototype.drawLayers = function() {
    
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

        this.drawTables(layer.tables);
    }; 
}

SqlViewer.Parser.prototype.drawTables = function(tables) {

	for (var i = 0; i < tables.length; i++) {
		var table = tables[i];
		var tableData = this.tableData[table.id];

		var tab = new SqlViewer.Table(
			table.element.x,
			table.element.y,
			tableData
		);

		tab.draw();		
	}
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


