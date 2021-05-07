$(':radio').change(function() {
    console.log('New star rating: ' + this.value);
    result = this.value
    show = this.name
    send_data(result);

});

function send_data(result) {

    $.ajax({
        type: "GET",
        url: '/shows/rate/' + show,
        data: {
            "result": result,
            "show": show,
        },
        dataType: "json",
    });
    document.getElementById("rating_form").hidden = true
    document.getElementById("rating_form").submit();
  }
