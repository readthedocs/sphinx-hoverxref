$(document).ready(function() {
    $('.hoverxref').tooltipster({
        theme: 'tooltipster-shadow',
        interactive: true,
        animation: 'fade',
        animationDuration: 0,
        content: 'Loading...',

        functionBefore: function(instance, helper) {
            var $origin = $(helper.origin);
            var project = $origin.data('project');
            var version = $origin.data('version');
            var doc = $origin.data('doc');
            var section = $origin.data('section');

            // we set a variable so the data is only loaded once via Ajax, not every time the tooltip opens
            if ($origin.data('loaded') !== true) {
                // TODO: improve URL handling here
                var url = 'https://readthedocs.org/api/v2/embed/?' + 'project=' + project + '&version=' + version + '&doc=' + doc + '&section=' + section;
                $.get(url, function(data) {

                    // call the 'content' method to update the content of our tooltip with the returned data.
                    // note: this content update will trigger an update animation (see the updateAnimation option)
                    instance.content(data['content']);

                    // to remember that the data has been loaded
                    $origin.data('loaded', true);
                });
            }
        }
    })});
