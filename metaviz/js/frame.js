// This file detects changes in either of the selectors in index.html and loads the appropriate view into the iframe

$(document).ready(function(){

  //Handles selection of different slicing (perspectivity, descriptor, and oid)
  $("#slice").change(function(){
    var url = "html/" + $(this).val() + "_" + $("#view").val() + ".html";
    $("iframe").attr("src",url);
  });

    //Handles selection of different view (3D and 2D)
  $("#view").change(function(){
    var url = "html/" + $("#slice").val() + "_" + $(this).val() + ".html";
    $("iframe").attr("src",url);
  });

});
