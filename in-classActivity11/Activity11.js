$(document).ready(function() {
   
    var sidebarLinks = $('#nav_list a');
  
    sidebarLinks.on('click', function(event) {
      event.preventDefault(); 
  
      var jsonFile = $(this).attr('title') + '.json';
  
      var mainContent = $('main');
      mainContent.empty();
  
      $.ajax({
        url: 'json_files/' + jsonFile,
        dataType: 'json',
        success: function(data) {
          var speakerHTML = '';
          
          data.speakers.forEach(function(speaker) {
            speakerHTML += '<h2>' + speaker.speaker + '</h2>' +
                           '<img src="' + speaker.image + '" alt="' + speaker.speaker + '">' +
                           '<p>' + speaker.text + '</p>';
          });
          mainContent.html(speakerHTML);
        },
        error: function() {
          console.log('JSON file could not be imported.');
        }
      });
    });
  });
  