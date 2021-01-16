const words = [['Drama', 6876], ['Comedy', 2723], ['Romance', 1851], ['Thriller', 1211], ['Action', 1162], ['Crime', 1125], 
            ['Adventure', 699], ['Family', 658], ['History', 631], ['War', 596], ['Fantasy', 530], ['Animation', 476], 
            ['Mystery', 474], ['Music', 359], ['Science Fiction', 307], ['Horror', 254], ['Western', 161], ['Documentary', 44],
            ['TV Movie', 8]];

toggleSearch = () => {
    document.getElementById("cloudToggle").classList.remove("selected");
    searchToggleBtn = document.getElementById("searchToggle");
    searchToggleBtn.classList.add("selected");
    document.getElementById("wordcloud-container").classList.add("hidden");
    document.getElementById("search-interface").classList.remove("hidden");
}

toggleCloud = () => {
    document.getElementById("searchToggle").classList.remove("selected");
    toggleCloudBtn = document.getElementById("cloudToggle");
    toggleCloudBtn.classList.add("selected");
    document.getElementById("search-interface").classList.add("hidden");
    document.getElementById("wordcloud-container").classList.remove("hidden");
    WordCloud(document.getElementById("wordcloud"), 
    {
        list: factorWeights(words),
        wait: 500,
        hover: addTitleOnSpan,
        gridSize: 40,
        backgroundColor: "transparent",
        color: 'random-dark',
        fontWeight: 'bold',
    });
}

factorWeights = (sortedWordsArr) => {
    rMin = sortedWordsArr[sortedWordsArr.length - 1][1];
    rMax = sortedWordsArr[0][1];
    tMin = 10;
    tMax = 100;

    return sortedWordsArr.map(word => [word[0], ((word[1] - rMin) / (rMax - rMin)) * (tMax - tMin) + tMin ])
}

addTitleOnSpan = (item) => {
    let spanTags = document.getElementsByTagName("span");
    for (let i = 0; i < spanTags.length; i++) {
        if (spanTags[i].textContent === item[0]) {
            spanTags[i].setAttribute("title", `${words.find(word => word[0] === item[0])[1]} ${item[0]} movies`)
        }
    }
}