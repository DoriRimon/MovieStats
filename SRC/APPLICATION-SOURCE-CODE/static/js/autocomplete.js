function autocomplete(inp) {
  var currentFocus;
  inp.addEventListener("input", function(e) {
      let arr = []

      var xhr = new XMLHttpRequest();
      xhr.open("POST", '/search', true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

      xhr.onreadystatechange = function() 
      {
          if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
          {
              arr = JSON.parse(xhr.response)
              var a, b, i;

              closeAllLists();

              if (arr.length === 0)
              {
                return;
              }

              currentFocus = -1;

              // create wrapper element
              a = document.createElement("div");
              a.setAttribute("id", inp.id + "autocomplete-list");
              a.setAttribute("class", "autocomplete-items");
              inp.parentNode.appendChild(a);

              for (i = 0; i < arr.length; i++) 
              {
                // create new inner element
                b = document.createElement("div");
                b.innerHTML = arr[i]
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) 
                {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });

                a.appendChild(b);
              }
          }
      }

      let select = document.getElementById('menu');
      let table = select.value;

      // table - selected talbe, text - user input text
      xhr.send(`table=${table}&text=${inp.value}`);

  });


  // navigate through drop down with keys
  inp.addEventListener("keydown", function(e) 
  {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.key == 'ArrowDown')
      { 
        currentFocus++;
        addActive(x);
      } 
      else if (e.key == 'ArrowUp')
      { 
        currentFocus--;
        addActive(x);
      } 
      else if (e.key == 'Enter')
      { 
        e.preventDefault();
        if (currentFocus > -1) 
        {
          if (x) x[currentFocus].click();
        }
      }
      else if (e.key === "Escape")
      {
        closeAllLists(null);
      }
  });


  // activate inner row
  function addActive(x) {
    if (!x) 
      return false;
    removeActive(x);
    if (currentFocus >= x.length) 
      currentFocus = 0;
    if (currentFocus < 0) 
      currentFocus = (x.length - 1);
    x[currentFocus].classList.add("autocomplete-active");
  }


  // deactivate inner row
  function removeActive(x) {
    for (var i = 0; i < x.length; i++)
      x[i].classList.remove("autocomplete-active");
  }

  function closeAllLists(elmnt) {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) 
    {
      if (elmnt != x[i] && elmnt != inp)
        x[i].parentNode.removeChild(x[i]);
    }
}


// close on click
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}



// send request and create autocomplete drop down based on result
autocomplete(document.getElementById("myInput"));


// change input place holder when table selection have been changed
function menuChange() {
  let cat = document.getElementById('menu').value;
  cat = cat.toLowerCase();
  let input = document.getElementById('myInput');
  let l = 'a';
  if (['a', 'e', 'i', 'o', 'u'].includes(cat.charAt(0)))
    l = 'an'
  input.placeholder = `Type ${l} ${cat} name..`;
}


function getEntities() {
  let type = document.getElementById('menu').value;
  let text = document.getElementById('myInput').value;

  // var xhr = new XMLHttpRequest();
  // xhr.open("GET", `/blocks/${type}/${text}`, true);
  // xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  // xhr.send();

  window.location.href = `/blocks/${type}/${text}`;
}