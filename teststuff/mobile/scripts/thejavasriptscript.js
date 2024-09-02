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
        document.getElementById("sidebar-container").style.display = "block";
        document.getElementById("container").style.display = "none";
        document.getElementById('opencloseImage').src = "images/exit.png";
    } else if (source == "exit.png") {
        document.getElementById("sidebar-container").style.display = "none";
        document.getElementById("container").style.display = "flex";
        document.getElementById('opencloseImage').src = "images/menu.png";
    };
};

function profile() {
    location.href = "profile";
};

function notification() {
    location.href = "notifications";
};
function search() {
    location.href = "search";
};

function home() {
    location.href = "main";
};

function friends() {
    location.href = "friends"
}

function trending() {
    location.href = "trending";
}

function clips() {
    location.href = "clips"
}

