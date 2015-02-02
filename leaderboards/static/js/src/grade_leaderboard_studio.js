/* Javascript for GradeLeaderboardXBlock. */
function GradeLeaderboardStudioXBlock(runtime, element) {
    "use strict";
    var tools = new LeaderboardTools(runtime, element);
    $('.save-button', element).bind('click', function(e) {
        e.preventDefault();
        var data = {
            graded_target_id: $(element).find('#graded_target_id').val(),
            count: $(element).find('input[name=count]').val()
        };
        tools.studio_submit(data);
    });

    $(element).find('.cancel-button').bind('click', function(e) {
        e.preventDefault();
        runtime.notify('cancel', {});
    });
}
