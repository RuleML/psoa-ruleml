// This file detects when a tile is clicked, updates tile focus, and loads the appropriate information into the card

$(document).ready(function () {
  var tileContainer = document.getElementById("tiles");
  var tiles = tileContainer.getElementsByClassName("tile");

  //Loops through all tiles
  for (var i = 0; i < tiles.length; i++) {

    //Checks for click event of any tile
    tiles[i].addEventListener("click", function() {

      var current = document.getElementsByClassName("focus");

      //Flag to remove card info
      var remove = false;

      //If there is already a tile selected:
      if(current[0]){

        //If the current selected tile is the same as the clicked tile:
        if(current[0].className == this.className){
          remove = true;
          this.className = this.className.replace(" focus", "");
        }
        //If the current selected tile is not the same as the clicked tile:
        else {
          current[0].className = current[0].className.replace(" focus", "");
          this.className += " focus";
        }
      }
      //If no tile is selected:
      else {
        this.className += " focus";
      }

      var id = this.id;

      //Load cards.json
      $.getJSON("../json/cards.json", function(json) {

          //Loop through each card in file
          json.cards.forEach(function(card) {

              //If the id of the card data matches the id of the clicked tile:
              if(card.systematicName ==  id) {

                //Remove card info
                if(remove) {
                  document.getElementById("systematicName").innerHTML = "";
                  document.getElementById("commonName").innerHTML = "";
                  document.getElementById("perspectivity").innerHTML = "";
                  document.getElementById("descriptor").innerHTML = "";
                  document.getElementById("oid").innerHTML = "";
                  document.getElementById("semantics").innerHTML = "";
                  document.getElementById("syntax").innerHTML = "";
                  document.getElementById("symbol").innerHTML = "";
                  document.getElementById("diagram").src = "";
                  remove = false;
                }

                //Update card info
                else {
                  document.getElementById("systematicName").innerHTML = card.systematicName;
                  document.getElementById("commonName").innerHTML = card.commonName;
                  document.getElementById("perspectivity").innerHTML = card.perspectivity;
                  document.getElementById("descriptor").innerHTML = card.descriptor;
                  document.getElementById("oid").innerHTML = card.oid;
                  document.getElementById("semantics").innerHTML = card.semantics;
                  document.getElementById("syntax").innerHTML = card.syntax;
                  document.getElementById("symbol").innerHTML = card.symbol;
                  document.getElementById("diagram").src = "../images/" + card.diagram;
                }
              }
          });
      });
    });
  }
});
