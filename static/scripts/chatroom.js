var scroll_on_reload = true;

var load_chat = window.setInterval(function() {
    var iframe = document.getElementById('chat_iframe')
    var iframe2 = document.getElementById('chat_iframe2')
    if (iframe.style.display == "block") {
        iframe.style.display = "none";
        iframe2.style.display = "block";
        iframe.contentWindow.location.reload();
        if (scroll_on_reload == true) {
            iframe2.contentWindow.scrollTo(0, iframe2.contentDocument.body.scrollHeight);
            iframe.contentWindow.scrollTo(0, iframe.contentDocument.body.scrollHeight);
        }
    } else {
        iframe2.style.display = "none";
        iframe.style.display = "block";
        iframe2.contentWindow.location.reload();
        if (scroll_on_reload == true) {
            iframe.contentWindow.scrollTo(0, iframe.contentDocument.body.scrollHeight);
            iframe2.contentWindow.scrollTo(0, iframe2.contentDocument.body.scrollHeight);
        }
    };
}, 2000)

function disable_scroll() {
    scroll_on_reload = false;
};

function enable_scroll() {
    scroll_on_reload = true;
};

function disable_load() {
    clearInterval(load_chat)
}

function send_message() {
    var chat_id = document.getElementById("chat_id_value");
    var xhttp = new XMLHttpRequest();
    var data = new FormData();
    data.append('message', document.getElementById("message").value);
    var url = "/pyxia/send_message/" + chat_id.value;
    xhttp.open("POST", url, false);
    xhttp.onload = function () {
        document.getElementById("message").value = ""
    };
    xhttp.send(data)
}