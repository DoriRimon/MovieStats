const basePosterPath = 'https://image.tmdb.org/t/p/' 
const size = 'w780'

function createTop() {
    movies.forEach((entity, index) => {
        let title = entity[0];
        let image = basePosterPath + size + entity[1];
        let revenue = entity[2];
        let overview = entity[3];

        // create row div
        let row = document.createElement('div');
        row.setAttribute('class', 'row');
        wrapper.appendChild(row);


        // create row > number div
        let num = document.createElement("div");
        num.setAttribute('class', 'number');
        row.appendChild(num);

        let digit = document.createElement('h1');
        digit.innerText = index + 1;
        num.appendChild(digit);


        // create row > card div
        let card = document.createElement("div");
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
        rev.setAttribute('class', 'revenue');
        rev.innerText = createRevText(revenue);
        text.appendChild(rev);

        // handle no overview
        let t = document.createElement('div');
        t.setAttribute('class', 'overview')
        if (!overview) 
            t.innerText = "The creators of the movie kept the description from us )-:";
        else
            t.innerText = overview;
        text.appendChild(t);
    });
}

function createRevText(revenue) {
    return 'Revenue: ' + revenue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + '$';
}

let wrapper = document.getElementById('wrapper');
