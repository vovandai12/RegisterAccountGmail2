https://www.mailticking.com/vi
$(document).on('click', '.changeMailbox', function () {
    var type = $(this).data('type');
    $('#active-mail').attr('data-clipboard-target', '');
    var boxNow = $('#active-mail').val();
    $('#active-mail').val('Wait...');
    var changeUrl = "/index/index/change.html";

    $.post(changeUrl, { type: type }, function (data) {
        if (data) {
            if (data == 1) {
                alert('Access too frequently, please try again later');
                $('#active-mail').val(boxNow);
                return false;
            } else {
                $('#active-mail').val(data);
                window.location.href = "/vi";
            }

        } else {
            alert('Failed, try again');
            return false;
        }
    });
});
$(function () {
    $('#active-mail').tooltip('show');
    $('#active-mail').on('hide.bs.tooltip', function (e) {
        e.preventDefault();
    });
    $('#active-mail').click(function () {
        var my = $(this);
        var clipboard = new ClipboardJS('#active-mail');
        clipboard.on('success', function (e) {
            console.log(e);
            var lefttime = setInterval(TipTime, 1000);
            var left = 3;

            function TipTime() {
                if (left == 0) {
                    $('.tooltip-inner').text('Click to copy');
                    clearInterval(lefttime);
                }
                left--;
            }

            my.select();
            $('.tooltip-inner').text('Copied');
        });
        clipboard.on('error', function (e) {
            $('.tooltip-inner').text('Failed, try again');

        });
    });
    $('#trigger-copy').click(function () {
        $('#active-mail').trigger('click');
        var my = $(this);
        my.html('<i class="fa fa-copy"></i>Copied');
        setTimeout(function () {
            my.html('<i class="fa fa-copy"></i>Click to copy');
        }, 1000);
    });
    $('#newMailbox').click(function () {
        var randomIndex = Math.floor(Math.random() * 3) + 1;;
        var randomElement = $('.changeMailbox').eq(randomIndex - 1);
        randomElement.trigger('click');
    });
});