let genres = [];

/**
 * Toggle the main page search
 */
toggleSearch = () => {
    document.getElementById("cloudToggle").classList.remove("selected");
    searchToggleBtn = document.getElementById("searchToggle");
    searchToggleBtn.classList.add("selected");
    document.getElementById("wordcloud-container").classList.add("hidden");
    document.getElementById("search-interface").classList.remove("hidden");
}

/**
 * Toggle the main page genres cloud
 */
toggleCloud = () => {
    document.getElementById("searchToggle").classList.remove("selected");
    toggleCloudBtn = document.getElementById("cloudToggle");
    toggleCloudBtn.classList.add("selected");
    document.getElementById("search-interface").classList.add("hidden");
    document.getElementById("wordcloud-container").classList.remove("hidden");
    WordCloud(document.getElementById("wordcloud"), 
    {
        list: factorWeights(genres),
        wait: 500,
        gridSize: 40,
        backgroundColor: "transparent",
        color: '#DEF2F1',
        fontWeight: 'bold',
    });
}

/**
 * normalize the weights of the genres, so that these amounts can be used as font sizes for the words cloud
 */
factorWeights = (sortedWordsArr) => {
    rMin = sortedWordsArr[sortedWordsArr.length - 1][1];
    rMax = sortedWordsArr[0][1];
    tMin = 10;
    tMax = 100;

    return sortedWordsArr.map(word => [word[0], ((word[1] - rMin) / (rMax - rMin)) * (tMax - tMin) + tMin ])
}

/**
 * Fetch the genres and their movies amount fro the server
 */
fetchGenres = () => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", '/allGenres', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function() 
    {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            genres = JSON.parse(xhr.response)
            document.getElementById("cloudToggle").classList.remove("hidden")
        }
    }

    xhr.send();
}

fetchGenres();