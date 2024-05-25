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
      $("#dialog").dialog({
        modal: true,
        open: function () {
          // Change the opacity of the header, footer, and container
          $("#header, #footer").css("opacity", "0.6");
          $(".container").css("opacity", "0.4");
          // Set the text inside the dialog
          $(this).text("Please upload at least one course file before submitting.");

          // Center the dialog on the screen
          $(this).parent().css({
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)"
          });
        },
        close: function () {
          // Reset the opacity when the dialog is closed
          $("#header, #footer, .container").css("opacity", "1");
        }
      }).dialog("open");
    }
  });

  // Submit event handler for classroomForm
  $("#classroomForm").submit(function (event) {
    var fileInput = $("#classroomCSV")[0];  // The specific file input to check

    if (fileInput.files.length === 0) {  // If no file is selected
      event.preventDefault();  // Prevent form submission
      $("#dialog").dialog({
        modal: true,
        open: function () {
          // Change the opacity of the header, footer, and container
          $("#header, #footer").css("opacity", "0.6");
          $(".container").css("opacity", "0.4");
          // Set the text inside the dialog
          $(this).text("Please upload classroom and capacities file before submitting.");

          // Center the dialog on the screen
          $(this).parent().css({
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)"
          });
        },
        close: function () {
          // Reset the opacity when the dialog is closed
          $("#header, #footer, .container").css("opacity", "1");
        }
      }).dialog("open");
    }
  });

  // Enable the datepicker
  $("#examStartDate, #examEndDate").datepicker();

  // numExamsPerDay input event handler
  $('#numExamsPerDay').on('input', function () {
    // Check the entered value
    const numExamsPerDay = parseInt($(this).val());
    if (numExamsPerDay > 0) {
      $('#generateFields').click();  // Click the "Generate Fields" button
    }
  });

  // Event handler for the generateFields button
  $("#generateFields").click(function () {
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


  // Submit event handler for constraintsForm
  $("#constraintsForm").submit(function (event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = $(this).serialize(); // Serialize the form data
    // Send the form data to the server
    $.ajax({
      type: "POST",
      url: "/submit_constraints",
      data: formData,
      success: function (response) {
        $("#constraintsFormResponse").html("<p>Form submitted succesfully!</p>");
        $("#constraintsForm")[0].reset(); // Reset the form
      },
      error: function (error) {
        $("#respoconstraintsFormResponsense").html("<p>There was an error submitting the form.</p>");
      }
    });
  });


  // Submit event handler for Scheduler code
  $('.runExamSchedulerSubmitButton').click(function () {
    // Show the progress container
    $('#progress-container').show();
    // Start the progress animation
    startProgress();
  });

  // Progress bar animation
  function setProgress(percentage) {
    if (percentage < 0) percentage = 0;
    if (percentage > 100) percentage = 100;

    $('#progress-bar').css('width', percentage + '%');
  }

  // Progress animation
  function startProgress() {
    let progress = 0;
    const interval = setInterval(function () {
      progress += 10;
      setProgress(progress);

      if (progress >= 100) {
        clearInterval(interval); // stop the progress animation
        animateLoadingDots(); // Loading animation
      }
    }, 550); // 550 miliseconds
  }

  // Loading animation
  function animateLoadingDots() {
    const dots = ['.', '..', '...'];
    let dotIndex = 0;
    const dotInterval = setInterval(function () {
      $('#loading-dots').text("Loading" + dots[dotIndex]);
      dotIndex = (dotIndex + 1) % dots.length;
    }, 500); // 500 miliseconds
  }
});