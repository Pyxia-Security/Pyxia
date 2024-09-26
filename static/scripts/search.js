function peopleSearch() {
    document.getElementById("people-button").style.backgroundColor = "#BB8493";
    document.getElementById("posts-button").style.backgroundColor = "#DBAFA0";
    document.getElementsByName("search-input")[0].placeholder="Search People";
    var search_type = document.getElementById("search_type");
    search_type.value = "people";
    // Change the form options so that it posts to look for people.
};


function postSearch() {
    document.getElementById("posts-button").style.backgroundColor = "#BB8493";
    document.getElementById("people-button").style.backgroundColor = "#DBAFA0";
    document.getElementsByName("search-input")[0].placeholder="Search Posts";
    var search_type = document.getElementById("search_type");
    search_type.value = "posts";
    // Change the form options so that it posts to look for posts.
};