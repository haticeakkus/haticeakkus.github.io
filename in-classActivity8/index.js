$(document).ready(function(){
    $( "#birthday" ).datepicker();
  });

  var languages = ["ActionScript", "AppleScript", "Asp","JavaScript", "Lisp", "Perl", "PHP", "Python"];
    
  $( "#languages" ).ready(function(){
    $( "#languages" ).autocomplete({
      source: languages
    });
});
  
 