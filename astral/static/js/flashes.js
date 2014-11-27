$(document).ready(function() {
    $("#flashes li a.close").click(function() {
        $(this).parents("li").remove();
        return false;
    });
});
