/**
 * Created by Smile on 2017/12/8.
 */
function translate(post, translatedid) {
            $(post).hide();
            $.post('/translate', {
                text: $(post).text()
            }).done(function (translated) {

                $(post).text(translated['text'])
                $(post).show();

            }).fail(function () {
                $(post).text("{{ _('Error: Could not contact server.') }}");
                $(post).show();
            });
        }