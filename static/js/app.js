// TODO:
// $( document ).ready(function() {
//     var apiUrl = SqlViewer.stringFormat("{0}/api/v1{1}?format=json", window.location.origin, window.location.pathname);
//     $.ajax({
//   		dataType: "json",
//   		url: apiUrl,
//   		success: function(json) {
//   			var data = JSON.parse(json);

//   			console.log(data);
// 			var _ = new SqlViewer.Parser(data.model.data, data.model.diagrams[0])
// 			_.draw();
//   		}
// 	});
// });




var json = '{"model":{"id":"2DA9EE96-A55D-4585-96C8-F84CF63264E3","name":"OmniDB","version":"20151010T1010","diagrams":[{"id":"A40EC320-032E-499E-8654-E9FC97952C5F","name":"Some Diagram","layers":[{"id":"F9F617B3-C1AD-4A11-A090-87C2BF257A28","name":"Root","comment":"Some Layer Comment","element":{"x":10,"y":10,"width":750,"height":750,"color":"#f39c12"},"tables":[{"id":"9DC4D5AC-F943-45E1-B242-9E9E24BED7DC","element":{"x":50,"y":150,"width":100,"height":100,"color":"#3498db","collapsed":false}},{"id":"20CB57F3-AA19-44CC-9C90-EC3E11DA3AA5","element":{"x":300,"y":150,"width":100,"height":100,"color":"#3498db","collapsed":false}}],"links":[{"id":"39678F83-EB7A-4848-84E2-A568D27FB0C6","linkId":"DE954174-8A6C-4977-BD28-E93C72D9F776","element":{"draw":"hidden|full|split"}}]}]}],"data":{"tables":[{"id":"5C772FCD-80E6-49DF-AA3E-649BCCAA333C","tableId":"9DC4D5AC-F943-45E1-B242-9E9E24BED7DC","name":"Orders","comment":"Orders table","columns":[{"id":"4BD3ACC4-4564-4C21-B93A-6270102152E3","name":"OrderID","dataType":"BINARY(16)","customType":"","comment":"order id comment","default":null,"flags":{"key":false,"nullable":false,"autoIncrement":false,"hidden":false,"reference":false}},{"id":"4BA0DD11-FF3C-4E22-BECD-7AFFFA1A63B6","name":"CustomerRefID","dataType":"BINARY(16)","customType":"","comment":"","default":null,"flags":{"key":false,"nullable":false,"autoIncrement":false,"hidden":false,"reference":false}},{"id":"718BD94C-4411-4D72-9AAA-DD9BD1B14FA5","name":"OrderDate","dataType":"DATETIME","customType":"","comment":"","default":null,"flags":{"key":false,"nullable":false,"autoIncrement":false,"hidden":false,"reference":false}}]},{"id":"28AC3A4A-5C5D-4E56-B752-D2C3D3DFEA92","tableId":"20CB57F3-AA19-44CC-9C90-EC3E11DA3AA5","name":"Customers","comment":"Customers table","columns":[{"id":"E6EF88AE-AC44-4638-8264-74A315859BE1","name":"CustomerID","dataType":"BINARY(16)","customType":"","comment":"order id comment","default":null,"flags":{"key":false,"nullable":false,"autoIncrement":false,"hidden":false,"reference":false}},{"id":"55D7DBCF-8094-4C3E-B86E-2C520D1FBEB8","name":"CustomerName","dataType":"VARCHAR(120)","customType":"","comment":"","default":null,"flags":{"key":false,"nullable":false,"autoIncrement":false,"hidden":false,"reference":false}},{"id":"95F03099-3BE2-4801-8A09-F3D86CFED5DC","name":"ContactName","dataType":"VARCHAR(120)","customType":"","comment":"","default":null,"flags":{"key":false,"nullable":false,"autoIncrement":false,"hidden":false,"reference":false}},{"id":"D5C42496-8874-41E8-9A7C-4F6AA1F63008","name":"Country","dataType":"VARCHAR(120)","customType":"","comment":"","default":null,"flags":{"key":false,"nullable":false,"autoIncrement":false,"hidden":false,"reference":false}}]}],"links":[{"id":"35A77DBD-EDFB-46CA-A11C-BF8BC3CD3677","type":"COLUMN","source":{"tableId":"28AC3A4A-5C5D-4E56-B752-D2C3D3DFEA92","columnId":"E6EF88AE-AC44-4638-8264-74A315859BE1"},"destination":{"tableId":"5C772FCD-80E6-49DF-AA3E-649BCCAA333C","columnId":"4BA0DD11-FF3C-4E22-BECD-7AFFFA1A63B6"}}]}}}';
var data = JSON.parse(json);

var p = new SqlViewer.Parser(data.model.data, data.model.diagrams[0])
p.draw();