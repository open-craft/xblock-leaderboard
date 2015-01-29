/* Javascript for ForumLeaderboardXBlock. */
function ForumLeaderboardStudioXBlock(runtime, element) {
    "use strict";
    var tools = new LeaderboardTools(runtime, element);
    $('.save-button', element).bind('click', function(e) {
        e.preventDefault();
        var data = {
            discussion_id: $(element).find('input[name=discussion_id]').val(),
            count: $(element).find('input[name=count]').val()
        };
        tools.studio_submit(data);
    });

    $(element).find('.cancel-button').bind('click', function(e) {
        e.preventDefault();
        runtime.notify('cancel', {});
    });
}
