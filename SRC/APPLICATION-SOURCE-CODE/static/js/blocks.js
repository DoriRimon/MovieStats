const basePosterPath = 'https://image.tmdb.org/t/p/' 
const size = 'w780'

function blocks() {
    rec.forEach(entity => {
        let title = entity[0];
        let image = basePosterPath + size + entity[1];
        if (!entity[1])
            image = 'https://www.google.com/url?sa=i&url=https%3A%2F%2F123moviesfree.zone%2Ftvshows.php&psig=AOvVaw2_0OQ_47am7iDNxGmfEr-_&ust=1610765735450000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMDpsI34nO4CFQAAAAAdAAAAABAO';

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

