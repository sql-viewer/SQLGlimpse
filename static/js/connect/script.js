$(document).ready(function () {
    var urlSplit = window.location.pathname.split("/");
    var model = urlSplit[2];
    var version = urlSplit[4];

    var setUpAutocomplete = function (selector, model, version) {
        var resultSize = 20;

        $(selector).autocomplete({
            minLength: 2,
            delay: 100,
            source: function (request, response) {
                $.getJSON("/api/v1/models/" + model + "/versions/" + version + "/tables", {name: $(selector).val(), size: resultSize}, response);
            },
            select: function (event, ui) {
                $(selector).val(ui.item.name);
                return false;
            }
        }).data("ui-autocomplete")._renderItem = function (ul, item) {
            return $("<li></li>")
                .data("item.autocomplete", item)
                .append("<a>" + item.name + "</a>")
                .appendTo(ul);
        };
    };

    setUpAutocomplete('#tableFrom', model, version);
    setUpAutocomplete('#tableTo', model, version);
});