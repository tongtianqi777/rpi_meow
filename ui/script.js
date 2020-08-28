const LOCALHOST_FLASK = 'http://127.0.0.1:5000/latest_button_push';

function httpGetAsync(callback)
{
  $.get( LOCALHOST_FLASK, callback);
}

function refresh() {
  // talk to Database every second
  setInterval(() => { httpGetAsync(renderTime)}, 1000);
}

function renderTime(time) {
  const date = new Date(time);
  const diff = Date.now() - date;
  var sec = Math.floor(diff % (1000 * 60) / 1000);
  var min = Math.floor(diff % (1000 * 60 * 60) / (1000 * 60));
  var hour = Math.floor(diff / (1000 * 60 * 60));
  document.getElementById("timer").innerHTML = hour + 'h ' + min + 'm ' + sec + 's';
}
function renderAnimation() {

}
