SqlViewer.namespace("SqlViewer.Parser"); 
SqlViewer.Parser = function (data, diagram) {
    if (!(this instanceof SqlViewer.Parser)) {
        return new SqlViewer.Parser(data, diagram);
    }

    this.tableData = this.getTableData(data);
	this.diagram = diagram;
};

/** 
 * get table data from json model
 */
SqlViewer.Parser.prototype.getTableData = function(data) {

	var retVal = [];

	for (var i = 0; i < data.tables.length; i++) {
		retVal[data.tables[i].tableId] = data.tables[i];
	}

	return retVal;
}

SqlViewer.Parser.prototype.draw = function() {

    this.drawLayers(this.diagram.layers);
}

SqlViewer.Parser.prototype.drawLayers = function(layers) {
    
    for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
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
		var tabRows = this.getTableColumns(tableData.columns);

		var tab = new SqlViewer.Table(
			table.element.x,
			table.element.y,
			tableData.name,
			tabRows
		);

		tab.draw();		
	}
}

SqlViewer.Parser.prototype.getTableColumns = function(columns) {

	var r = [];
	for (var i = 0; i < columns.length; i++) {
		r.push(columns[i].name);
	}
	return r;
}