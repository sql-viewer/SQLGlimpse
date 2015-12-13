// GLOBAL NAMESPACE
var SqlViewer = SqlViewer || {};

SqlViewer.draw = SVG("main").size('100%', '100%');

// GLOBAL FUNCTIONS: 
// Extends global namespace
SqlViewer.namespace = function (namespace_string) {
    var parts = namespace_string.split('.'),
        parent = SqlViewer,
        i, max;

    if (parts[0] === "SqlViewer") {
        parts = parts.slice(1);
    }
    for (i = 0, max = parts.length; i < max; i++) {
        if (typeof parent[parts[i]] == 'undefined') {
            parent[parts[i]] = {};
        }
        parent = parent[parts[i]];
    }
    return parent;
};

// Enables class inherance 
SqlViewer.inherits = function (child, parent) {
    for (var property in parent) {
        if (parent.hasOwnProperty(property)) {
            child[property] = parent[property];
        }
    }
    function Ghost() { this.constructor = child; }
    Ghost.prototype = parent.prototype;
    child.prototype = new Ghost();
    child._super = parent.prototype;
    return child;
};

SqlViewer.generateGuid = function () {
    function S4() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1); 
    }
    return (S4() + S4() + "-" + S4() + "-4" + S4().substr(0,3) + "-" + S4() + "-" + S4() + S4() + S4()).toLowerCase();
};

SqlViewer.generateColor = function() {
	var letters = '0123456789ABCDEF'.split('');
	var color = '#';
	for (var i = 0; i < 6; i++ ) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}

SqlViewer.stringFormat = function (format) {
    if (typeof format === "undefined") return;

    var args = Array.prototype.slice.call(arguments, 1);
    return format.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined' ? args[number] : match;
    });
};