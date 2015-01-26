/* Javascript for ForumLeaderboardXBlock. */
function ForumLeaderboardStudioXBlock(runtime, element) {
    $('.save-button', element).bind('click', function() {
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {
            discussion_id: $(element).find('input[name=discussion_id]').val(),
            count: $(element).find('input[name=count]').val()
        };
        $.post(handlerUrl, JSON.stringify(data)).success(function(response) {
            if (response['success']) {
                window.location.reload(false);
                return
            }
            alert(response['errors'].join('\n'));
        });
    });

    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });
}
