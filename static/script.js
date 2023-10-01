// script.js
function downloadVideo() {
    const url = $("#url").val();
    $.ajax({
        url: "/download",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ url: url }),
        success: function(response) {
            alert(response.message);
        },
        error: function(xhr, status, error) {
            if (xhr.status === 400) {
                alert(xhr.responseJSON.message);
            } else {
                alert("Server error occurred");
            }
        }
    });
}
