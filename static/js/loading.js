function load() {
	fetch("complete/").then(async (template) => {document.body.innerHTML = await template.text();})
}

load();