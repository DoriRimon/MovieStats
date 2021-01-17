const basePosterPath = 'https://image.tmdb.org/t/p/';
const size = 'w780';

/**
 * create the page layout for the top 10 movies of a genre
 */
function createTopMovies() {
    topMovies.forEach((entity, index) => {
        let title = entity[0];
        let image = basePosterPath + size;

        if (!entity[1])
            image = 'https://123moviesfree.zone/no-poster.png';

        else
            image += entity[1];

        let revenue = entity[2];
        let overview = entity[3];
        let id = entity[4];

        // create row div
        let row = document.createElement('div');
        row.setAttribute('class', 'row');
        movies.appendChild(row);


        // create row > number div
        let num = document.createElement("div");
        num.setAttribute('class', 'number');
        row.appendChild(num);

        let digit = document.createElement('h1');
        digit.innerText = index + 1;
        num.appendChild(digit);


        // create row > card div
        let card = document.createElement("div");
        card.setAttribute('id', id);
        card.setAttribute('class', 'card');
        row.appendChild(card);


        // create card > poster div
        let poster = document.createElement('div');
        poster.setAttribute('class', 'poster');
        card.appendChild(poster);

        let img = document.createElement('img');
        img.setAttribute('src', image);
        poster.appendChild(img);


        // create card > text div
        let text = document.createElement('div');
        text.setAttribute('class', 'text')
        card.appendChild(text);

        let h = document.createElement("h1");
        h.innerText = title;
        text.appendChild(h);

        let rev = document.createElement('div');
        rev.setAttribute('class', 'subtitle');
        rev.innerText = createRevText(revenue);
        if (!revenue)
            rev.innerText = "Renenue isn't availabe";
        text.appendChild(rev);

        let t = document.createElement('div');
        t.setAttribute('class', 'description')
        if (!overview) 
            t.innerText = "The creators of the movie kept the description from us )-:";
        else
            t.innerText = overview;
        text.appendChild(t);


        h.addEventListener('click', e => {
            window.location.href = `/movie/${id}`;
        });

        poster.addEventListener('click', e => {
            window.location.href = `/movie/${id}`;
        });
    });
}

/**
 * create the page layout for the top 10 actors of a genre
 */
function createTopActors() {
    topActors.forEach((entity, index) => {
        let name = entity[0];
        let image = basePosterPath + size;

        if (!entity[1])
            image = 'https://123moviesfree.zone/no-poster.png';

        else
            image += entity[1];

        let biography = entity[2];
        let amount = entity[3];
        let id = entity[4];

        // create row div
        let row = document.createElement('div');
        row.setAttribute('class', 'row');
        actors.appendChild(row);


        // create row > number div
        let num = document.createElement("div");
        num.setAttribute('class', 'number');
        row.appendChild(num);

        let digit = document.createElement('h1');
        digit.innerText = index + 1;
        num.appendChild(digit);


        // create row > card div
        let card = document.createElement("div");
        card.setAttribute('id', id);
        card.setAttribute('class', 'card');
        row.appendChild(card);


        // create card > poster div
        let poster = document.createElement('div');
        poster.setAttribute('class', 'poster');
        card.appendChild(poster);

        let img = document.createElement('img');
        img.setAttribute('src', image);
        poster.appendChild(img);


        // create card > text div
        let text = document.createElement('div');
        text.setAttribute('class', 'text')
        card.appendChild(text);

        let h = document.createElement("h1");
        h.innerText = name;
        text.appendChild(h);

        let movieAmount = document.createElement('div');
        movieAmount.setAttribute('class', 'subtitle');
        movieAmount.innerText = `Acted in ${amount} movies`;
        text.appendChild(movieAmount);

        let t = document.createElement('div');
        t.setAttribute('class', 'description')
        if (!biography) 
            t.innerText = "The actor didn't want to share his biography with us )-:";
        else
            t.innerText = biography;
        text.appendChild(t);

        h.addEventListener('click', e => {
            window.location.href = `/actor/${id}`;
        });

        poster.addEventListener('click', e => {
            window.location.href = `/actor/${id}`;
        });
    });
}

/**
 * 
 * @param {number} revenue number
 * 
 * @returns {string} of the number with commas seperating each 3 digits
 */
function createRevText(revenue) {
    return 'Revenue: ' + revenue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + '$';
}

/**
 * Switch from movies to actors
 */
function switchToActors() {
    movies.style.display = 'none';
    actors.style.display = 'flex';
}

/**
 * Switch from actors to movies
 */
function swtichToMovies() {
    actors.style.display = 'none';
    movies.style.display = 'flex';
}

let movies = document.getElementById('movies');
let actors = document.getElementById('actors');

/**
 * Return to home page
 */
function home() {
    window.location.href = '/';
}
