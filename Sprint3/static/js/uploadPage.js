$(document).ready(function () {
    // Object to store files
    var files = {};

    // File change event handler
    $("#classroomCSV").change(function () {
        var file = this.files[0];
        var key = $(this).attr("id");

        if (file) {
            // Store the file in the files object
            files[key] = file;
            var fileInfo = `Selected file for Classroom CSV: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;

            // Check for existing information and update or create new
            var existingInfo = $(`#info-${key}`);
            if (existingInfo.length) {
                existingInfo.text(fileInfo);
            } else {
                $(".uploadClassroomInfo").append(`<div id="info-${key}">${fileInfo}</div>`);
            }
        }
    });

    // File change event handler
    $("#CENG, #CE, #EE, #ESE, #IE, #MATH, #MCE, #MSE, #SENG").change(function () {
        var file = this.files[0];
        var key = $(this).attr("id");

        if (file) {
            // Store the file in the files object
            files[key] = file;
            var fileInfo = `Selected file for ${key}: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;

            // Check for existing information and update or create new
            var existingInfo = $(`#info-${key}`);
            if (existingInfo.length) {
                existingInfo.text(fileInfo);
            } else {
                $(".uploadCourseInfo").append(`<div id="info-${key}">${fileInfo}</div>`);
            }
        }
    });


    // Submit event handler for courseForm
    $("#courseForm").submit(function (event) {
        var fileInputs = $(this).find("input[type='file']");  // All file inputs in the form
        var isAnyFileSelected = fileInputs.toArray().some(function (fileInput) {
            return fileInput.files.length > 0;  // Return true if at least one file is selected
        });

        if (!isAnyFileSelected) {  // If no file is selected
            event.preventDefault();  // Prevent form submission
            // Show dialog instead of alert
            $("#dialog").dialog("open").text("Please upload at least one course file before submitting.");
            // Change the opacity of the header, footer, and container
            $("#header, #footer").css("opacity", "0.6");
            $(".container").css("opacity", "0.4");
            // Open the dialog
            $("#dialog").dialog("open");

            // Center the dialog on the screen
            $("#dialog").parent().css({
                position: "fixed",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)"
            });
        }
    });

    // Submit event handler for classroomForm
    $("#classroomForm").submit(function (event) {
        var fileInput = $("#classroomCSV")[0];  // The specific file input to check

        if (fileInput.files.length === 0) {  // If no file is selected
            event.preventDefault();  // Prevent form submission
            // Show dialog instead of alert
            $("#dialog").dialog("open").text("Please upload classroom and capacities file before submitting.");
            // Change the opacity of the header, footer, and container
            $("#header, #footer").css("opacity", "0.6");
            $(".container").css("opacity", "0.4");
            // Open the dialog
            $("#dialog").dialog("open");

            // Center the dialog on the screen
            $("#dialog").parent().css({
                position: "fixed",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)"
            });
        }
    });

    // Enable the datepicker
    $("#examStartDate, #examEndDate").datepicker();

    // Event handler for the generateFields button
    $("#generateFields").click(function() {
        const container = $("#examTimesContainer");
        container.empty(); // Clear previous content
      
        const numExamsPerDay = $("#numExamsPerDay").val();
      
        if (numExamsPerDay > 0) {
          // Dynamically create fields based on the number of exams
          for (let i = 1; i <= numExamsPerDay; i++) {
            const newField = $("<div></div>").addClass("input-group"); // Grouping for styling
            newField.html(`
              <label for="examStart${i}">Exam ${i} Start Time</label>
              <input
                type="time"
                id="examStart${i}"
                name="examStart${i}"
                required
              />
      
              <label for="examEnd${i}">Exam ${i} End Time</label>
              <input
                type="time"
                id="examEnd${i}"
                name="examEnd${i}"
                required
              />
            `);
            container.append(newField); // Add the new fields
          }
        }
      });
      

    // Create the dialog
    $("#dialog").dialog({
        autoOpen: false, // Don't open automatically when the page loads
        modal: false, // Allow interactions with elements outside the dialog
        closeOnEscape: false, // Disable closing the dialog when pressing the escape key
        closeText: "X", // Change the close button text to "X"
        buttons: [], // Remove all buttons from the dialog
        close: function () {
            // Restore opacities when the dialog is closed
            $("#header, #footer, .container").css("opacity", "1");
        }
    });

    function generateExamSchedule(numExamsPerDay) {
        // Take the start and end dates
        const startDate = $('#examStartDate').val();
        const endDate = $('#examEndDate').val();
      
        // Take the start and end times for each exam
        const startTime = $('#examStart1').val();
        const endTime = $('#examEnd1').val();
      
        // Take the Friday prayer times
        const fridayPrayerStart = $('#fridayPrayerStart').val();
        const fridayPrayerEnd = $('#fridayPrayerEnd').val();
      
        // Create the JSON data
        const jsonData = {
          "examDates": {
            "startDate": startDate,
            "endDate": endDate
          },
          "exams": [],
          "numExamsPerDay": numExamsPerDay,
          "fridayPrayerTimes": {
            "startTime": fridayPrayerStart,
            "endTime": fridayPrayerEnd
          }
        };
      
        // Add the start and end times for each exam
        for (let i = 1; i <= numExamsPerDay; i++) {
          jsonData.exams.push({
            "startTime": $(`#examStart${i}`).val(),
            "endTime": $(`#examEnd${i}`).val()
          });
        }
      
        return JSON.stringify(jsonData);
      }
      $('#numExamsPerDay').on('input', function() {
        // Girilen değeri kontrol et
        const numExamsPerDay = parseInt($(this).val());
        if (numExamsPerDay > 0) {
            $('#generateFields').click(); // "Generate Fields" düğmesine tıkla
        }
    });

    $('#constraintsForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission
      
        const jsonData = generateExamSchedule(parseInt($('#numExamsPerDay').val()));
        console.log(jsonData); // write to console for debugging
      
        // Send the JSON data to the server
        $.ajax({
          url: '/write_constraints_json_to_file', 
          type: 'POST',
          contentType: 'application/json',
          data: jsonData,
          success: function(response) {
            console.log('Response from server:', response);
          },
          error: function(error) {
            console.error('Error:', error);
          }
        });
        $('#constraintsForm').trigger('reset'); // Reset the form fields
      });
    
  
    // Prevent interactions outside the dialog when it is open
    $('.runExamSchedulerSubmitButton').click(function () {
        $('#progress-container').show();
        startProgress(); // Start the progress bar
    });

    function setProgress(percentage) {
        // Ensure percentage is between 0 and 100
        if (percentage < 0) percentage = 0;
        if (percentage > 100) percentage = 100;

        $('#progress-bar').css('width', percentage + '%'); // Make the progress bar the specified width
    }

    function startProgress() {
        let progress = 0;
        const interval = setInterval(function () {
            progress += 10; // Increase progress by 10
            setProgress(progress);

            if (progress >= 100) {
                clearInterval(interval); // Stop the interval
            }
        }, 550);
    }
});




