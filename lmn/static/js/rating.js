function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


$(':radio').change(function() {
    
    rating_out_of_five = this.value
    show = this.name
    send_data(rating_out_of_five, show);

});


function send_data(rating_out_of_five, show) {

    $.ajax({ 
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        url: '/shows/rate/' + show + '/',
        data: {
            "rating_out_of_five": rating_out_of_five,
        },
        dataType: "json",
    });
    document.getElementById("rating_form").hidden = true
    document.getElementById("rating_form").submit();
  }
