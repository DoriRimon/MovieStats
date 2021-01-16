const basePosterPath = 'https://image.tmdb.org/t/p/';
const size = 'w780';

function createPage() {
    let id = actorRec[0];
    let name = actorRec[1];
    let profile = basePosterPath + size;
    if (!actorRec[2])
        profile = 'https://123moviesfree.zone/no-poster-bright.png';

    else
        profile += actorRec[2];
    
    let biography = actorRec[3];
    if (!biography) 
            biography = "The actor didn't want to share his biography with us )-:";


    // create movie div
    let actor = document.createElement('div');
    actor.setAttribute('id', 'actor');
    wrapper.appendChild(actor);

    // create actor > poster div
    let poster = document.createElement('div');
    poster.setAttribute('class', 'poster');
    actor.appendChild(poster);

    let img = document.createElement('img');
    img.setAttribute('src', profile);
    poster.appendChild(img);


    // create actor > innerWrapper div
    let innerWrapper = document.createElement('div');
    innerWrapper.setAttribute('id', 'inner-wrapper');
    actor.appendChild(innerWrapper);

    let text = document.createElement('div');
    text.setAttribute('id', 'text')
    innerWrapper.appendChild(text);

    let h = document.createElement("h1");
    h.setAttribute('id', 'name');
    h.innerText = name;
    text.appendChild(h);

    let biographyElem = document.createElement('div');
    biographyElem.setAttribute('id', 'biography')
    biographyElem.innerText = biography;
    text.appendChild(biographyElem);

    let movies = document.createElement('div');
    movies.setAttribute('id', 'movies');
    innerWrapper.appendChild(movies);

    moviesRec.forEach(entity => {
        let title = entity[0];
        let image = basePosterPath + size;

        
        if (!entity[1])
            image = 'https://123moviesfree.zone/no-poster.png';

        else
            image += entity[1];
        
        let movieId = entity[2];

        let card = document.createElement("div");
        card.setAttribute('id', movieId);
        card.setAttribute('class', 'card');
        card.style.backgroundImage = `url('${image}')`;
        movies.appendChild(card);

        let cardOverlay = document.createElement('div');
        cardOverlay.setAttribute('class', 'overlay');
        card.appendChild(cardOverlay);

        let movieTitle = document.createElement("h1");
        movieTitle.innerText = title;
        card.appendChild(movieTitle);

        card.addEventListener('click', e => {
            window.location.href = `/movie/${movieId}`;
        });
    });

    if (recActorsRec.length > 0) {
        let recWrapper = document.createElement('div');
        recWrapper.setAttribute('id', 'rec-wrapper');
        wrapper.appendChild(recWrapper);

        let recText = document.createElement('div');
        recText.setAttribute('id', 'rec-text');
        recText.innerText = `${name} acted mostly with...`
        recWrapper.appendChild(recText);

        let recActors = document.createElement('div');
        recActors.setAttribute('id', 'rec-cards');
        recWrapper.appendChild(recActors);
    

        recActorsRec.forEach(entity => {
            let recTitle = entity[0];
            let recImage = basePosterPath + size;

            if (!entity[1])
                recImage = 'https://123moviesfree.zone/no-poster.png';

            else
                recImage += entity[1];

            let recId = entity[2];

            let card = document.createElement("div");
            card.setAttribute('id', recId);
            card.setAttribute('class', 'card');
            card.style.backgroundImage = `url('${recImage}')`;
            recActors.appendChild(card);

            let cardOverlay = document.createElement('div');
            cardOverlay.setAttribute('class', 'overlay');
            card.appendChild(cardOverlay);

            let recName = document.createElement("h1");
            recName.innerText = recTitle;
            card.appendChild(recName);

            card.addEventListener('click', e => {
                window.location.href = `/actor/${recId}`;
            });
        });
    }
}

let wrapper = document.getElementById('wrapper');
createPage();

function home() {
    window.location.href = '/';
}
