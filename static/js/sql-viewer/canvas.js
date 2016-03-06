SqlViewer.namespace("SqlViewer.Canvas"); 
SqlViewer.Canvas = function (x, y, h, w, color, text) {
    if (!(this instanceof SqlViewer.Canvas)) {
        return new SqlViewer.Canvas(x, y, h, w, color, text);
    }

    // Properties:
    this.id = SqlViewer.generateGuid();
    this.x = x;
    this.y = y;
    this.height = h;
    this.weight = w;
    this.color = color || SqlViewer.generateColor();
    this.text = text || "";
};


SqlViewer.Canvas.prototype.draw = function() {
    SqlViewer.draw.rect(this.weight, this.height).attr({ x:this.x, y:this.y, fill: this.color, class: "sqlv-canvas" });

    if (this.text != "")
        SqlViewer.draw.text(this.text).attr({ x:this.x, y:this.y, class: "sqlv-canvasText"});
}