const sleep = ms => new Promise(r => setTimeout(r, ms));

const facts = [
    "Did you know, if the salt of the ocean was to cover the earth's land surface, it would be 166 meters or 500 feet deep?",
    "Did you know, 50% of the water in the US and 90% of the ocean has yet to be mapped?",
    "\"Technoblade never dies!\"",
    "The number of species that live the ocean today remains unknown but estimates put it about 8.7 million!",
    "50-80% of the world's oxygen is produced from the ocean. Majority of which is produced by plankton.",
    "\"Hello there!\"",
    "In the US, $282 billion is generated in goods and services by the ocean",
    "The ocean might know Obama's lastname...",
    "What time is it again?",
    "c̵̰̣͚̞̤̲̣̺͑̋̃͑͠o̵̢̢͍̟̙̲̹̘̲̟͗́̊̓̇̈̌͆̂̊̅́́̒̋͘ͅͅö̵́͜k̸̦̮̰̮̼̯̓͘͝ī̸̧̧̤̯̩̰̜͓̮͉͓̗̻̮͗̌̊͝ͅe̶̙̥̫̯̬̼̣̘͉̱̘̖̩̳͕͇̅͐̀̐̍̎ͅ",
    "There are more planes in the ocean than submarines in the sky"
]

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function load() {
    fetch("complete/").then(async (template) => {
        document.body.innerHTML = await template.text();
    })
}

function random_facts() {
    return facts[getRandomInt(facts.length - 1)];
}

function change_fact() {
    // get fact text
    let check = document.getElementById("facts");

    if (check !== null) {
        check.innerHTML = random_facts().valueOf();

        fact_loop()
    }

}

let currentZoom = 1;
let minZoom = 1;
let stepSize = 0.1;
let container = null;

function disableScroll() {
    // Get the current page scroll position
    scrollTop =
        window.pageYOffset || document.documentElement.scrollTop;
    scrollLeft =
        window.pageXOffset || document.documentElement.scrollLeft,

        // if any scroll is attempted,
        // set this to the previous value
        window.onscroll = function () {
            window.scrollTo(scrollLeft, scrollTop);
        };
}

function enableScroll() {
    window.onscroll = function () {
    };
}

function zoomImage(direction) {
    let newZoom = currentZoom + direction * stepSize;

    // Limit the zoom level to the minimum and maximum values
    if (newZoom < minZoom) {
        return;
    }

    currentZoom = newZoom;

    // Update the CSS transform of the image to scale it
    let image = document.querySelector('#image-container img');
    image.style.transform = 'scale(' + currentZoom + ')';
}

function scroll_lock() {

    // Get the current page scroll position
    scrollTop =
        window.pageYOffset || document.documentElement.scrollTop;
    scrollLeft =
        window.pageXOffset || document.documentElement.scrollLeft,

        // if any scroll is attempted,
        // set this to the previous value
        window.onscroll = function () {
            window.scrollTo(scrollLeft, scrollTop);
        };
}

function fact_loop() {
    sleep(8000).then(r => change_fact())
}

setTimeout(load, 0);
fact_loop();

while (container === null) {
    container = document.getElementById('image-container');
    co
}

container.addEventListener('wheel', function (event) {
    // Zoom in or out based on the scroll direction
    let direction = event.deltaY > 0 ? -1 : 1;
    zoomImage(direction);
});