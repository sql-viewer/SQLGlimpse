SqlViewer.namespace("SqlViewer.Table"); 
SqlViewer.Table = function (x, y, name, rows) {
    if (!(this instanceof SqlViewer.Table)) {
        return new SqlViewer.Table(x, y, name, rows);
    }

    // Properties:
    this.id = SqlViewer.generateGuid();
    this.x = x;
    this.y = y;
    this.name = name;
    this.rows = rows;

    this.draw = function() {

        SqlViewer.draw.svg(this.createTable(this.name, this.rows)).attr({ x:this.x, y:this.y, class: "sqlv-table" });

    };

    this.createTable = function() {

        if( Object.prototype.toString.call( rows ) !== '[object Array]' ) {
            console.error("CreateTable argument is not array!");
            throw "CreateTable argument is not array!";
        }

        table = SqlViewer.stringFormat('<foreignobject x="{0}" y="{1}">', this.x, this.y);

        table += SqlViewer.stringFormat("<table class='sqlv-table'><tr><th>{0}</th></tr>", this.name);
        for (var i = 0; i < this.rows.length; i++) {
            table += SqlViewer.stringFormat("<tr><td>{0}</td></tr>", rows[i]);
        };
        table += "</table></foreignobject>";

        return table;
    }
};

