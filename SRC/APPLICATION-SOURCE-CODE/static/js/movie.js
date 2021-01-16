const basePosterPath = 'https://image.tmdb.org/t/p/';
const size = 'w780';

function createPage() {
    let id = movieRec[0];
    let title = movieRec[1];
    let budget = movieRec[2];
    let revenue = movieRec[3];
    let date = movieRec[4];

    if (!date)
        date = 'Date not available';
    else {
        date = date.slice(0, -13);
        // let day = date.getDate();
        // let month = date.getMonth();
        // let year = date.getFullYear();
        // date = day + '.' + (month + 1) + '.' + year; 
    }

    let image = basePosterPath + size;

    if (!movieRec[5])
        image = 'https://123moviesfree.zone/no-poster.png';

    else
        image += movieRec[5];
    
    let overview = movieRec[6];

    if (!overview) 
            overview = "The creators of the movie kept the description from us )-:";
    
    let rating = movieRec[7];


    // create movie div
    let movie = document.createElement('div');
    movie.setAttribute('id', 'movie');
    wrapper.appendChild(movie);

    // create movie > poster div
    let poster = document.createElement('div');
    poster.setAttribute('class', 'poster');
    movie.appendChild(poster);

    let img = document.createElement('img');
    img.setAttribute('src', image);
    poster.appendChild(img);


    // create movie > innerWrapper div
    let innerWrapper = document.createElement('div');
    innerWrapper.setAttribute('id', 'inner-wrapper');
    movie.appendChild(innerWrapper);

    let text = document.createElement('div');
    text.setAttribute('id', 'text')
    innerWrapper.appendChild(text);

    let h = document.createElement("h1");
    h.setAttribute('id', 'title');
    h.innerText = title;
    text.appendChild(h);

    let dateElem = document.createElement('h2');
    dateElem.setAttribute('id', 'date');
    dateElem.innerText = date;
    text.appendChild(dateElem);

    let rate = document.createElement('div');
    rate.setAttribute('id', 'rate');
    text.appendChild(rate);

    let ratingElem = document.createElement('div');
    ratingElem.setAttribute('id', 'rating');
    ratingElem.innerText = `Rating: ${rating}/10`;
    rate.appendChild(ratingElem);

    let ratingPos = document.createElement('div');
    ratingPos.setAttribute('id', 'rating-pos');
    ratingPos.innerText = `This is rated at #${moviePos}`;
    rate.appendChild(ratingPos);

    let money = document.createElement('div');
    money.setAttribute('id', 'money');
    text.appendChild(money);

    let budgetElem = document.createElement('div');
    budgetElem.setAttribute('id', 'budget');
    budgetElem.innerText = 'Budget: ' + createMoneyText(budget)
    if (!budget)
        budgetElem.innerText = "Budget isn't available";
    money.appendChild(budgetElem);

    let revenueElem = document.createElement('div');
    revenueElem.setAttribute('id', 'revenue');
    revenueElem.innerText = 'Revenue: ' + createMoneyText(revenue);
    if (!revenue)
        revenueElem.innerText = "Revenue isn't available";
    money.appendChild(revenueElem);

    let overviewElem = document.createElement('div');
    overviewElem.setAttribute('id', 'overview')
    overviewElem.innerText = overview;
    text.appendChild(overviewElem);

    let actors = document.createElement('div');
    actors.setAttribute('id', 'actors');
    innerWrapper.appendChild(actors);

    actorsRec.forEach(entity => {
        let name = entity[0];
        let profile = basePosterPath + size;

        
        if (!entity[1])
            profile = 'https://123moviesfree.zone/no-poster.png';

        else
            profile += entity[1];
        
        let actorId = entity[2];

        let card = document.createElement("div");
        card.setAttribute('id', actorId);
        card.setAttribute('class', 'card');
        card.style.backgroundImage = `url('${profile}')`;
        actors.appendChild(card);

        let cardOverlay = document.createElement('div');
        cardOverlay.setAttribute('class', 'overlay');
        card.appendChild(cardOverlay);

        let actorName = document.createElement("h1");
        actorName.innerHTML = name;
        card.appendChild(actorName);
    });
}

function createMoneyText(revenue) {
    return revenue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + '$';
}

let wrapper = document.getElementById('wrapper');
createPage();
