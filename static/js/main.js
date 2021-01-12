


function send(term){
  var data_list = {'term':'cielo'};

  fetch(`http://127.0.0.1:5000/rae/${encodeURI(term)}`, {
      method: "get",
      credentials: "same-origin",
      headers: {
          // "X-CSRFToken"  : getCookie("csrftoken"),
          "Accept"       : "application/json",
          "Content-Type" : "application/json"
      },
      // body: JSON.stringify(data_list)
  }).then(function(response) {
      return response.json();
  }).then(function(data) {
    var print = document.querySelector('#resultado');
    print.innerHTML = data.data;

  }).catch(function(ex) {

    console.log("parsing failed", ex);

  });
}



var termino =  document.querySelectorAll('.js-buscar-termino');

termino.forEach(function(element){
    element.addEventListener('click', function(e){
      e.preventDefault();
      var term = document.querySelector('#term');
      console.log(term.value, term);
      send(term.value);
    });
});

