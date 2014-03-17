// JavaScript Document

function login() {
    $("#hint").html("登录中...请稍候");
    var g = false;
    $.ajax({
        url: "/login/", async: false, data: { uname: $('#uname').val(), passwd: $('#passwd').val() }, success:
            function (data) {
                if (data == "OK")
                    g = true;
                else {
                    $("#hint").html(data);
                    g = false;
                }
            }, type: "POST"
    });
    return g;
}

function tealogin() {
    $("#hint").html("登录中...请稍候");
    var g = false;
    $.ajax({
        url: $("#tealogin_fr").attr("action"), async: false, data: { login:"1", passwd: $('#passwd').val() }, success:
            function (data) {
                if (data == "OK")
                    g = true;
                else {
                    $("#hint").html(data);
                    g = false;
                }
            }, type: "POST"
    });
    return g;
}

/*修改密码*/
function chpwd() {
    if ($('#passwd').val() != $('#repasswd').val()) {
        $("#hint").html("两次密码不同");
        return false;
    }
    $("#hint").html("密码修改中...请稍候");
    var act = $("#chpwd_fr").attr("action");
    $.ajax({
        url: act + "/chpwd/", async: false, data: { passwd: $('#passwd').val() }, success:
            function (data) {
                if (data == "OK") {
                    alert("修改成功！");
                    top.location = act.replace("teaedit", "tea").replace("cms", "");
                }
                else {
                    $("#hint").html(data);
                }
            }, type: "POST"
    });
    return false;
}

function photost(info,src) {
    if (info == "OK") {
        $("#photo_img").attr("src", src);
        $('#photoif').html("");
        return;
    }
    $('#photoif').html(info);
}


function preteaedit() {
    for (var i = 0; i<10; i++) {
        $("#fr_teaedit").find("input").eq(i).val($("textarea").eq(i).val());
    }
    return true;
}

$(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?  
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute  
        var host = document.location.host; // host + port  
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin  
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.  
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});