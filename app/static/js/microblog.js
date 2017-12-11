/**
 * Created by Smile on 2017/12/8.
 */

function translate(post) {
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


function setUpTime() {
    var startdate = new Date();  //开始时间
    startdate.setFullYear(2017, 8, 3)
    startdate.setHours(00, 00, 00)
    var enddate = new Date();    //结束时间
    var interval = enddate.getTime() - startdate.getTime()  //时间差的毫秒数
    var days = Math.floor(interval / (24 * 3600 * 1000)) + 1
    $('.menuRight').text('今天是我们相爱的第' + days + '天')
    $('.menuRight').css('visibility', 'visible')

}

$(function () {
    setUpTime()
});

