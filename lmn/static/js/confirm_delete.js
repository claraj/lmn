//find all delete buttons; add click event listener; if clicked, show confirm dialog


var deleteButtons = document.querySelectorAll('.delete');

deleteButtons.forEach(function(button){

  button.addEventListener('click', function(ev){

    // Show a confirm dialog
    var okToDelete = confirm("Delete note - are you sure?");

    // If user presses no, prevent the form submit
    if (!okToDelete) {
      ev.preventDefault();  // Prevent the click event propagating
    }

    // Otherwise, the web page will continue processing the event, 
    // and send the delete request to the server.


  })
});