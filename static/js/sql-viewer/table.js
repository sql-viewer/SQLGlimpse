SqlViewer.namespace("SqlViewer.Table"); 
SqlViewer.Table = function (x, y, data) {
    if (!(this instanceof SqlViewer.Table)) {
        return new SqlViewer.Table(x, y, data);
    }

    // Properties:
    this.id = SqlViewer.generateGuid();
    this.x = x;
    this.y = y;
    this.data = data;
};

SqlViewer.Table.prototype.draw = function() {
    SqlViewer.draw.svg(this.createTable(this.data));
}

SqlViewer.Table.prototype.createTable = function(data) {

    table = SqlViewer.stringFormat('<foreignobject x="{0}" y="{1}">', this.x, this.y);

    table += SqlViewer.stringFormat("<table class='sqlv-table' data-toggle='tooltip' title='{1}'><tr><th>{0}</th></tr>", 
        data.name, 
        data.comment);

    for (var i = 0; i < this.data.columns.length; i++) {

        var column = this.data.columns[i];

        table += SqlViewer.stringFormat("<tr data-toggle='tooltip' title='{1}' ><td>{0}</td></tr>", 
            column.name, 
            column.comment);
    };
    table += "</table></foreignobject>";

    return table;
}

