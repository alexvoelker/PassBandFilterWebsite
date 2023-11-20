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
	"What time it it again?",
	"c̵̰̣͚̞̤̲̣̺͑̋̃͑͠o̵̢̢͍̟̙̲̹̘̲̟͗́̊̓̇̈̌͆̂̊̅́́̒̋͘ͅͅö̵́͜k̸̦̮̰̮̼̯̓͘͝ī̸̧̧̤̯̩̰̜͓̮͉͓̗̻̮͗̌̊͝ͅe̶̙̥̫̯̬̼̣̘͉̱̘̖̩̳͕͇̅͐̀̐̍̎ͅ"
]

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function load() {
	fetch("complete/").then(async (template) => {document.body.innerHTML = await template.text();})
}

function random_facts(){
	return facts[getRandomInt(facts.length-1)];
}

function change_fact(){
	// get fact text
	document.getElementById("facts").innerHTML = random_facts().valueOf();

	fact_loop()
}

function fact_loop() {
	sleep(8000).then(r => change_fact())
}

setTimeout(load,0);
fact_loop();