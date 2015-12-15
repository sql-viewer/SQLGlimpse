SqlViewer.namespace("SqlViewer.Table"); 
SqlViewer.Table = function (x, y, name, columns) {
    if (!(this instanceof SqlViewer.Table)) {
        return new SqlViewer.Table(x, y, name, columns);
    }

    // Properties:
    this.id = SqlViewer.generateGuid();
    this.x = x;
    this.y = y;
    this.name = name;
    this.columns = columns;
};

SqlViewer.Table.prototype.draw = function() {
    SqlViewer.draw.svg(this.createTable(this.name, this.columns));
}

SqlViewer.Table.prototype.createTable = function(name, columns) {

    table = SqlViewer.stringFormat('<foreignobject x="{0}" y="{1}">', this.x, this.y);

    table += SqlViewer.stringFormat("<table class='sqlv-table'><tr><th>{0}</th></tr>", name);
    for (var i = 0; i < columns.length; i++) {
        table += SqlViewer.stringFormat("<tr><td>{0}</td></tr>", columns[i]);
    };
    table += "</table></foreignobject>";

    return table;
}