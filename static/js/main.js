


function send(term){

  var data_list = {'term':'cielo'};

  fetch(`/rae/${encodeURI(term)}`, {
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
      window.location.hash = encodeURIComponent(term);
      document.querySelector("#term").value = term;
  }).catch(function(ex) {

    console.log("parsing failed", ex);

  });
}


function local_storage_add(term){

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



document.addEventListener('click', e => {
    if(e.target.matches("mark") || e.target.matches("a")){ 
      e.preventDefault();
      let word = e.target.textContent.replace(/[^a-záéíóúñü\s]/gmi, '');
      send(word);
    }
});


var hash_term = function(){
  let hash = decodeURIComponent(window.location.hash).replace("#", '');
  if(hash){
    send(hash);
  }
};

document.addEventListener('DOMContentLoaded', hash_term, false);
window.addEventListener('hashchange', hash_term, false);




