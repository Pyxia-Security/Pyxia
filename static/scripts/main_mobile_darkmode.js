var button = document.getElementById('opencloseMenu');
function openclosemenu() {
    var buttonsrc = document.getElementById("opencloseImage").src;
    srcLength = buttonsrc.length;
    const imagelocationLetters = [];
    for (let i = 0; i < 9; i++) {
        a = buttonsrc[srcLength - i];
        imagelocationLetters.push(a);
    };
    var source = "";
    for (let i = 8; i > 0; i--) {
        source = source + imagelocationLetters[i];
    };
    if (source == "menu.png") {
        document.getElementById("container").style.display = "none";
        document.getElementById("sidebar-container").style.display = "block";
        document.getElementById('opencloseImage').src = document.getElementById("exit_address").src;
        document.getElementById('sidebar-container').style.backgroundColor = "#344955";
        document.getElementById('sidebar-container').style.borderRight = "solid black 2px";
        document.getElementById('sidebar-container').style.borderBottom = "solid black 2px";
    
    } else if (source == "exit.png") {
        document.getElementById("container").style.display = "flex";
        document.getElementById("sidebar-container").style.display = "none";
        document.getElementById('opencloseImage').src = document.getElementById("menu_address").src;
        document.getElementById('sidebar-container').style.backgroundColor = "rgba(0, 0, 0, 0)";
        document.getElementById('sidebar-container').style.border = "none";
    };
};

function notificationcloseMenu() {
    document.getElementById("notification-overlay").style.display = "none";
    document.getElementById("html").style.overflow = "auto";
}

function notificationopenMenu() {
    document.getElementById("notification-overlay").style.display = "block";
    document.getElementById("html").style.overflow = "hidden";
}

function notification() {
    location.href = "/notifications"
}

function profile() {
    location.href = "/pyxia/profile";
};

function search() {
    location.href = "/pyxia/search";
};

function home() {
    location.href = "/pyxia";
};

function friends() {
    location.href = "/pyxia/friends";
}

function trending() {
    location.href = "/pyxia/trending";
}

function clips() {
    location.href = "/pyxia/clips";
}

function like_post(post_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.status == 201) {
            document.getElementById("like_button_img_" + post_id).src = "/static/images/liked.png";
            document.getElementById("like_button_" + post_id).setAttribute( "onClick", "javascript: unlike_post(" + post_id + ");" );
            document.getElementById("post_likes_" + post_id).textContent = this.responseText;
        };
    };
    var post_id_request = "/pyxia/like_post/" + post_id;
    xhttp.open("POST", post_id_request, false)
    xhttp.send();
}

function unlike_post(post_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.status == 201) {
            document.getElementById("like_button_img_" + post_id).src = "/static/images/like.png";
            document.getElementById("like_button_" + post_id).setAttribute( "onClick", "javascript: like_post(" + post_id + ");" );
            document.getElementById("post_likes_" + post_id).textContent = this.responseText;
        };
    };
    var post_id_request = "/pyxia/unlike_post/" + post_id;
    xhttp.open("POST", post_id_request, false);
    xhttp.send();
};

function save_post(post_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.status == 201) {
            document.getElementById("bookmark_button_img_" + post_id).src = "/static/images/bookmarked.png";
            document.getElementById("bookmark_button_" + post_id).setAttribute( "onClick", "javascript: unsave_post(" + post_id + ");" );
        };
    };
    var post_id_request = "/pyxia/save_post/" + post_id;
    xhttp.open("POST", post_id_request, false);
    xhttp.send();
};

function unsave_post(post_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.status == 201) {
            document.getElementById("bookmark_button_img_" + post_id).src = "/static/images/bookmark.png";
            document.getElementById("bookmark_button_" + post_id).setAttribute( "onClick", "javascript: save_post(" + post_id + ");" );
        };
    };
    var post_id_request = "/pyxia/unsave_post/" + post_id;
    xhttp.open("POST", post_id_request, false)
    xhttp.send();
};

function copy_link() {
    var url = document.getElementById("share_link_box");
    url.select();
    url.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(url.value);
};

function open_share(post_id) {
    var url = document.getElementById("share_link_box");
    url.value = "https://pyxia.tech/pyxia/posts/" + post_id;
    document.getElementById("share_overlay").style.display = "flex";
};

function close_share() {
    document.getElementById("share_overlay").style.display = "none";
}

function edit_desc_close() {
    document.getElementById("description-overlay").style.display = "none";
}

function edit_desc_open() {
    document.getElementById("description-overlay").style.display = "flex";
}

function change_pfp() {
    location.href = "/pyxia/profile/change_pfp";
}

function logout() {
    location.href = "/logout";
}

var check_alive = window.setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.responseText == "redirect") {
            location.href = "/logout";
        } else if (this.responseText == "DISABLE") {
            kill_check_alive()
        };
    };
    var check_alive_request = "/pyxia/check_auth";
    xhttp.open("POST", check_alive_request, false)
    xhttp.send();
}, 60000)

function kill_check_alive() {
    clearInterval(check_alive);
}

function add_post() {
    location.href = "/pyxia/create_post";
}

function messages() {
    location.href = "/pyxia/chat";
}

function image_left(img_post_id) {
    var start_image_element = document.getElementById(img_post_id + "_start_image");
    var start_images = start_image_element.getAttribute("name");
    var current_div = document.getElementById(img_post_id + "_container_thingy");
    var current_div_id = current_div.getAttribute("name");
    if (current_div_id != start_images) {
        var current_div_id_int = parseInt(current_div_id)
        var change_to = current_div_id_int - 1
        document.getElementById("post_image_" + img_post_id + "_" + current_div_id).className = "post-image-hidden post-image-video";
        current_div.className = "post-image-hidden";
        current_div.id = img_post_id + "_" + current_div_id;
        document.getElementById(img_post_id + "_" + change_to).className = "container_thingy";
        document.getElementById("post_image_" + img_post_id + "_" + change_to).className = "post-image post-image-video";
        document.getElementById(img_post_id + "_" + change_to).id = img_post_id + "_container_thingy";
    }
}

function image_right(img_post_id) {
    var total_image_element = document.getElementById(img_post_id + "_total_image");
    var total_images = total_image_element.getAttribute("name");
    var current_div = document.getElementById(img_post_id + "_container_thingy");
    var current_div_id = current_div.getAttribute("name");  
    if (current_div_id != total_images) {
        var current_div_id_int = parseInt(current_div_id)
        var change_to = current_div_id_int + 1
        document.getElementById("post_image_" + img_post_id + "_" + current_div_id).className = "post-image-hidden post-image-video";
        current_div.className = "post-image-hidden post-image-video";
        current_div.id = img_post_id + "_" + current_div_id;
        document.getElementById(img_post_id + "_" + change_to).className = "container_thingy";
        document.getElementById("post_image_" + img_post_id + "_" + change_to).className = "post-image post-image-video";
        document.getElementById(img_post_id + "_" + change_to).id = img_post_id + "_container_thingy";
    }
}

function savedposts() {
    location.href = '/pyxia/bookmarks';
}

function settings() {
    location.href = '/pyxia/settings';
}