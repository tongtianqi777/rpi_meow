const SAW_CAT_API = 'http://127.0.0.1:5000/saw_cat';
const LAST_TIME_SAW_CAT_TS_API = 'http://127.0.0.1:5000/last_time_saw_cat_ts';
const LAST_TIME_SAW_CAT_IMG_API = 'http://127.0.0.1:5000/last_time_saw_cat_img';

function httpGetAsync(api, callback)
{
  $.get(api, callback);
}

function setIntervals() {
  // talk to these APIs every second (these run on Redis on the back)
  setInterval(() => { httpGetAsync(SAW_CAT_API, renderSawCat)}, 1000);
  setInterval(() => { httpGetAsync(LAST_TIME_SAW_CAT_TS_API, renderLastTimeSawCat)}, 1000);

  // talk to these APIs every 10 second (less frequently because they are I/O intense)
  // todo
}

function renderSawCat(sawCat) {
    console.log("rending saw cat.. sawCat = " + sawCat);
    if (sawCat === "true") {
        $("#cat-alert").text("Hello Kitties!");
        $("#cat-alert").addClass("highlight");
    } else {
        $("#cat-alert").text("No Cat Around");
        $("#cat-alert").removeClass("highlight");
    }
}

function padNum(number) {
  if (number < 10) return '0' + number;
  return number;
}

function renderLastTimeSawCat(sawCatTs) {
    console.log("rending saw cat ts.. sawCatTs = " + sawCatTs);

    if (sawCatTs.length == 0) {
        $("#timer").text("No Cats were seen<br>so far");
        return;
    }
    const date = new Date(sawCatTs);
    const diff = Date.now() - date;

    var sec = Math.floor(diff % (1000 * 60) / 1000);
    var min = Math.floor(diff % (1000 * 60 * 60) / (1000 * 60));
    var hour = Math.floor(diff / (1000 * 60 * 60));

    $("#timer").text("Cats were seen<br>" + hour + 'h ' + min + 'm ' + sec + "s ago");
}
