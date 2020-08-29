const LOCALHOST_FLASK = 'http://127.0.0.1:5000/latest_button_push';

function httpGetAsync(callback)
{
  $.get( LOCALHOST_FLASK, callback);
}

function refresh() {
  // talk to Database every second
  setInterval(() => { httpGetAsync(renderTime)}, 1000);
}


function padNum(number) {
  if (number < 10) return '0' + number;
  return number;
}


function renderTime(time) {
  const date = new Date(time);
  const diff = Date.now() - date;
  var sec = padNum(Math.floor(diff % (1000 * 60) / 1000));
  var min = padNum(Math.floor(diff % (1000 * 60 * 60) / (1000 * 60)));
  var hour = padNum(Math.floor(diff / (1000 * 60 * 60)));

  document.getElementById("timer").innerHTML = hour + ':' + min + ':' + sec;

  var confettiSettings = {
      "target": "confetti-canvas",
      "max": "120",
      "size": "3",
      "animate": true,
      "props": [
        "circle",
        "square",
        "triangle",
        "line"
      ],
      "colors": [
        [
          165,
          104,
          246
        ],
        [
          230,
          61,
          135
        ],
        [
          0,
          199,
          228
        ],
        [
          253,
          214,
          126
        ]
      ],
      "clock": "80",
      "rotate": true,
      "start_from_edge": true,
      "respawn": false
    };

  if (hour == 0 && min == 0 && sec == 0) {
    var confetti = new ConfettiGenerator(confettiSettings);
    confetti.render();
  }
}
function renderAnimation() {

}
