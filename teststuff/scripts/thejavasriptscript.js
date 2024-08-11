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
        document.getElementById("sidebar").style.display = "block";
        document.getElementById('opencloseImage').src = "images/exit.png";
        document.getElementById('sidebar-container').style.backgroundColor = "#704264";
        document.getElementById('sidebar-container').style.borderRight = "solid black 2px";
        document.getElementById('sidebar-container').style.borderBottom = "solid black 2px";
    
    } else if (source == "exit.png") {
        document.getElementById("sidebar").style.display = "none";
        document.getElementById('opencloseImage').src = "images/menu.png";
        document.getElementById('sidebar-container').style.backgroundColor = "rgba(0, 0, 0, 0)";
        document.getElementById('sidebar-container').style.border = "none";
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
    location.href = "/";
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

