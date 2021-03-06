SqlViewer.namespace("SqlViewer.Table"); 
SqlViewer.Table = function (table, canvasX, canvasY, data) {
    if (!(this instanceof SqlViewer.Table)) {
        return new SqlViewer.Table(table, canvasX, canvasY, data);
    }

    // Properties:
    this.id = table.id;
    this.table = table;
    this.data = data;
    this.canvasX = canvasX;
    this.canvasY = canvasY;
};

SqlViewer.Table.prototype.draw = function() {
    SqlViewer.draw.svg(this.createTable());
}

SqlViewer.Table.prototype.createTable = function() {

    table = SqlViewer.stringFormat('<foreignobject x="{0}" y="{1}" width="{2}" height="{3}">', 
        this.table.element.x + this.canvasX, 
        this.table.element.y + this.canvasY,
        this.table.element.width,
        this.table.element.height
    );

    table += SqlViewer.stringFormat("<div style='width:{4}px; height:{5}px;'class='sqlv-table'data-toggle='tooltip'title='{1}'id='{2}'>"
        + "<ul><li style='background-color: {3}' class='sqlv-tableHeader'>{0}</li>", 
        this.data.name, 
        this.data.comment,
        this.data.id,
        this.table.element.color,
        this.table.element.width,
        this.table.element.height   
    );
    for (var i = 0; i < this.data.columns.length; i++) {

        var column = this.data.columns[i];
        var icon = (column.flags.key) ? "<i class='fa fa-key key'></i>" : "<i class='fa fa-circle-o'></i>";
        table += SqlViewer.stringFormat("<li data-toggle='tooltip'id='{1}'>{2} {0}</li>", 
            column.name, 
            column.id,
            icon
        );

    }
    table += "<ul></div></foreignobject>";

    return table;
}