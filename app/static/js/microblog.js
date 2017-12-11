/**
 * Created by Smile on 2017/12/8.
 *
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
    menuRight = $('.menuRight')
    if (menuRight.css('visibility') == 'hidden') {
        menuRight.css('visibility', 'visible')
    }

    var startdate = new Date();  //开始时间
    startdate.setFullYear(2017, 8, 3)
    startdate.setHours(21, 00, 00)
    var enddate = new Date();    //结束时间
    //计算天
    var interval = enddate.getTime() - startdate.getTime()  //时间差的毫秒数
    var days = Math.floor(interval / (24 * 3600 * 1000)) + 1//天
    //计算小时
    var leave1 = interval % (24 * 3600 * 1000)    //计算天数后剩余的毫秒数
    var hours = Math.floor(leave1 / (3600 * 1000)) + 1  //小时
    //计算相差分钟数
    var leave2 = leave1 % (3600 * 1000)        //计算小时数后剩余的毫秒数
    var minutes = Math.floor(leave2 / (60 * 1000))//分钟
    //计算相差秒数
    var leave3 = leave2 % (60 * 1000)      //计算分钟数后剩余的毫秒数
    var seconds = Math.round(leave3 / 1000)//秒
    menuRight.text('这是我们相爱的第' + days + '天' + hours + '小时' + minutes + '分钟' + seconds + '秒')

}

$(function () {
    setUpTime()
    setInterval(setUpTime, 1000)

    $("[data-toggle='popover']").popover();

});

