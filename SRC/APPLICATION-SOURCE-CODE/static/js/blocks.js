function blocks() {
    rec.forEach(entity => {
        let title = entity[0];
        let card = document.createElement("div");
        let h = document.createElement("h1");
        card.appendChild(h);
        h.innerHTML = title;
        wrapper.appendChild(card);
    });
}

var wrapper = document.getElementById('blocks');
