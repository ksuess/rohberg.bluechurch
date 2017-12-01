$(document).ready(function() {

    var random_22 = Math.floor((Math.random() * 22) + 1);
    $("#visual-portal-wrapper")
        .css("background-image", "url('/++theme++bluechurch/images/backgrounds/blue_church_" + random_22 + ".jpg')");
    
});