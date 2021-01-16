const basePosterPath = 'https://image.tmdb.org/t/p/' 
const size = 'w780'

function blocks() {
    rec.forEach(entity => {
        let title = entity[0];
        let image = basePosterPath + size;
        let id = entity[2];

        if (!entity[1])
            image = '../img/no-poster-bright.png';

        else
            image += entity[1];

        let card = document.createElement("div");
        card.setAttribute('id', id);
        card.setAttribute('class', 'card');
        card.style.backgroundImage = `url('${image}')`;

        let cardOverlay = document.createElement('div');
        cardOverlay.setAttribute('class', 'overlay');

        let h = document.createElement("h1");
        h.innerHTML = title;

        card.appendChild(h);
        card.appendChild(cardOverlay);
        wrapper.appendChild(card);


        card.addEventListener('click', e => {
            window.location.href = `/${type.toLowerCase()}/${card.id}`;
        });
    });
}

var wrapper = document.getElementById('blocks');

function home() {
    window.location.href = '/';
}
