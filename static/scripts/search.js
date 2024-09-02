function peopleSearch() {
    document.getElementById("people-button").style.backgroundColor = "#BB8493";
    document.getElementById("posts-button").style.backgroundColor = "#DBAFA0";
    document.getElementsByName("search-input")[0].placeholder="Search People";
    // Change the form options so that it posts to look for people.
};


function postSearch() {
    document.getElementById("posts-button").style.backgroundColor = "#BB8493";
    document.getElementById("people-button").style.backgroundColor = "#DBAFA0";
    document.getElementsByName("search-input")[0].placeholder="Search Posts";
    // Change the form options so that it posts to look for posts.
};