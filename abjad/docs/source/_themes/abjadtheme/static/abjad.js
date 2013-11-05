$(document).ready(function() {
    $("div.abjad-book > pre").toggle();
    $("div.abjad-book > img").click(function(event){
        $(this).siblings("pre").toggle(250);
    });
});

