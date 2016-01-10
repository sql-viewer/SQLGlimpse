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
    SqlViewer.draw.svg(this.createTable());
}

SqlViewer.Table.prototype.createTable = function() {

    table = SqlViewer.stringFormat('<foreignobject x="{0}" y="{1}">', this.x, this.y);

    table += SqlViewer.stringFormat("<table class='sqlv-table' data-toggle='tooltip' title='{1}' id='{2}'>"
        + "<tr><th>{0}</th></tr>", 
        this.data.name, 
        this.data.comment,
        this.data.id
    );

    for (var i = 0; i < this.data.columns.length; i++) {

        var column = this.data.columns[i];

        table += SqlViewer.stringFormat("<tr data-toggle='tooltip'title='{1}' ><td id='{2}'>{0}</td></tr>", 
            column.name, 
            this.createRowTitle(column),
            column.id);
    };
    table += "</table></foreignobject>";

    return table;
}

SqlViewer.Table.prototype.createRowTitle = function(column) {

    var type = column.customType || column.dataType;

    separator = "";
    for (var i = type.length+5; i >= 0; i--) {
        separator += "- ";
    };

    return SqlViewer.stringFormat("{0}&#xA;{1}&#xA;{2}", type, separator, column.comment.replace("\n", "&#xA;"));
}