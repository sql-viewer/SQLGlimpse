/**
 * Created by stefa on 3/10/2016.
 */
$(document).ready(function () {

    var $form = $('.box');
    var $input = $('#file');
    var droppedFiles = false;

    $form.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
    })
    .on('dragover dragenter', function () {
        $form.addClass('is-dragover');
    })
    .on('dragleave dragend drop', function () {
        $form.removeClass('is-dragover');
    })
    .on('drop', function (e) {
        droppedFiles = e.originalEvent.dataTransfer.files;
        $form.trigger('submit');
    }).on('submit', function (e) {
        if ($form.hasClass('is-uploading')) return false;
        $form.addClass('is-uploading').removeClass('is-error');
        e.preventDefault();

        var ajaxData = new FormData($form.get(0));

        if (droppedFiles) {
            $.each(droppedFiles, function (i, file) {

                ajaxData.append($input.attr('name'), file);
            });
        }

        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: ajaxData,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            complete: function () {
                $form.removeClass('is-uploading');
            },
            success: function (data) {
                $form.addClass(data.success == true ? 'is-success' : 'is-error');
            },
            error: function () {
                console.log("error uploading file")
            }
        });

    });
});