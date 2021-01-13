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
              a = document.createElement("div");
              a.setAttribute("id", inp.id + "autocomplete-list");
              a.setAttribute("class", "autocomplete-items");
              inp.parentNode.appendChild(a);
              for (i = 0; i < arr.length; i++) 
              {
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
      xhr.send(`table=${table}&text=${inp.value}`);

  });

  inp.addEventListener("keydown", function(e) 
  {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.key == 'ArrowDown') // down key
      { 
        currentFocus++;
        addActive(x);
      } 
      else if (e.key == 'ArrowUp') // up key
      { 
        currentFocus--;
        addActive(x);
      } 
      else if (e.key == 'Enter') // enter key
      { 
        e.preventDefault();
        if (currentFocus > -1) 
        {
          if (x) x[currentFocus].click();
        }
      }
      else if (e.key === "Escape") // esc key
      {
        closeAllLists(null);
      }
  });

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

document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}


autocomplete(document.getElementById("myInput"));

function menuChange() {
  let cat = document.getElementById('menu').value;
  let input = document.getElementById('myInput');
  let l = 'a';
  if (cat.charAt(0) in ['a', 'e', 'i', 'o', 'u'])
    l = 'an'
  input.placeholder = `Type ${l} ${cat} name..`;
}