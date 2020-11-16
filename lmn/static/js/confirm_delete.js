//find all delete buttons;
var deleteButtons = document.querySelectorAll('.delete');

deleteButtons.forEach(function(button){
  //add click event listener
  button.addEventListener('click', function(ev){

    // if clicked, show confirm dialog message
    var okToDelete = confirm("Delete note - are you sure?");

    // If user presses no, don't delete
    if (!okToDelete) {
      ev.preventDefault();  // no action - not deletion
    }

    // Otherwise, web page will send delete request to server 

  })
});