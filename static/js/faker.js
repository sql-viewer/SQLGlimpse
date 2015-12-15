function getRandomWord() {
	var word = ["cadaver","ephebi","epicanthic","fast-food","mayoresses","opilio","quintals","racialization","tradeable","welds"];
	return word[Math.floor((Math.random() * word.length) + 1)];
}



var layer = function () {
	this.id = SqlViewer.generateGuid();
	this.name = getRandomWord();
	this.comment = "Some Layer Comment";
	this.element = {
		x: 10,
		y: 10,
		width: 500,
		height: 500,
		color: SqlViewer.generateColor(),
	}
}