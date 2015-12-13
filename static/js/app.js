var canvas = new SqlViewer.Canvas(10,10, 500,500,"#e67e22", "Books");
canvas.draw();

var book_rows = ["id", "title", "author_refId", "isDeleted", "TimeStemp"];
var books = new SqlViewer.Table(50, 120, "books", book_rows);
books.draw();

var author_rows = ["id", "firstname", "lastname", "isDeleted"];
var author = new SqlViewer.Table(300, 120, "author", author_rows);
author.draw();