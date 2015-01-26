/* Javascript for GradeLeaderboardXBlock. */
function GradeLeaderboardStudioXBlock(runtime, element) {
    "use strict";
    $('.save-button', element).bind('click', function(e) {
        e.preventDefault();
        var data = {
            graded_target_id: $(element).find('#graded_target_id').val(),
            count: $(element).find('input[name=count]').val()
        };
        runtime.notify('save', {state: 'start', message: gettext("Saving")});
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'studio_submit'),
            data: JSON.stringify(data),
            dataType: "json",
            global: false,  // Disable Studio's error handling that conflicts with studio's notify('save') and notify('cancel') :-/
            success: function(response) { runtime.notify('save', {state: 'end'}); }
        }).fail(function(jqXHR) {
            var message = gettext("This may be happening because of an error with our server or your internet connection. Try refreshing the page or making sure you are online.");
            if (jqXHR.responseText) { // Is there a more specific error message we can show?
                try {
                    message = JSON.parse(jqXHR.responseText).error;
                } catch (error) { message = jqXHR.responseText; }
            }
            runtime.notify('error', {title: gettext("Unable to update leaderboard settings"), message: message});
        });
    });

    $(element).find('.cancel-button').bind('click', function(e) {
        e.preventDefault();
        runtime.notify('cancel', {});
    });
}
