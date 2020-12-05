// HTML page info is needed, the element ID's set by Django are used to identify
// the title and text form elements
let title_count = document.getElementById('id_title');
let text_count = document.getElementById('id_text');
let show_info = document.getElementById('show_info').innerText.length;

// initial count set, this subtracts the show info length from the total, as that is part of the tweet
document.getElementById('counter').innerHTML = ((280 - show_info) + "/280");

// each time the title or text is typed in, the listener will activate, recounting the lengths of the two elements
// and including the original show_info length, and subtract from 280 (the tweet character limit)
document.getElementById('id_title').onkeyup = function () {
  document.getElementById('counter').innerHTML = (280 - (this.value.length + text_count.value.length + show_info)) + "/280"
};
document.getElementById('id_text').onkeyup = function () {
  document.getElementById('counter').innerHTML = (280 - (this.value.length + title_count.value.length + show_info)) + "/280"
};