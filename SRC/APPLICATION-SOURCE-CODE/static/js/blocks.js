const basePosterPath = 'https://image.tmdb.org/t/p/' 
const size = 'w780'

function blocks() {
    rec.forEach(entity => {
        let title = entity[0];
        let image = basePosterPath + size + entity[1];
        if (!entity[1])
            image = 'https://123moviesfree.zone/no-poster.png';

        let card = document.createElement("div");
        card.setAttribute('class', 'card');
        card.style.backgroundImage = `url('${image}')`;

        let cardOverlay = document.createElement('div');
        cardOverlay.setAttribute('class', 'overlay');

        let h = document.createElement("h1");
        h.innerHTML = title;

        card.appendChild(h);
        card.appendChild(cardOverlay);
        wrapper.appendChild(card);
    });
}

var wrapper = document.getElementById('blocks');

