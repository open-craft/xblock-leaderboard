function LeaderboardTools(runtime, element) {
    "use strict";
    return {
        studio_submit: function(data) {
            var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
            runtime.notify('save', {state: 'start', message: gettext("Saving")});
            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify(data),
                dataType: "json",
                global: false,  // Disable Studio's error handling that conflicts with studio's notify('save') and notify('cancel') :-/
                success: function(response) { runtime.notify('save', {state: 'end'}); }
            }).fail(function(jqXHR) {
                var message = gettext("This may be happening because of an error with our server or your internet connection. Try refreshing the page or making sure you are online.");
                if (jqXHR.responseText) { // Is there a more specific error message we can show?
                    try {
                        message = JSON.parse(jqXHR.responseText).error;
                    } catch (error) { message = jqXHR.responseText.substr(0, 300); }
                }
                runtime.notify('error', {title: gettext("Unable to update leaderboard settings"), message: message});
            });
        }
    };
}
