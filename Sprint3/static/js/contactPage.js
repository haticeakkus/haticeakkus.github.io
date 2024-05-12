$(document).ready(function() {
  // Create the dialog
  $("#dialog").dialog({
    autoOpen: false, // Don't open automatically when the page loads
    modal: false, // Allow interactions with elements outside the dialog
    closeOnEscape: false, // Disable closing the dialog when pressing the escape key
    closeText: "X", // Change the close button text to "X"
    buttons: [], // Remove all buttons from the dialog
    close: function() {
      // Restore opacities when the dialog is closed
      $("#header, #footer, .container").css("opacity", "1");
      // Hide the overlay
      $("#overlay").hide();
    }
  });

  // Submit event handler for contactForm
  $("#contactForm").submit(function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Perform form validation
    if ($(this).valid()) {
      // Show dialog instead of alert
      $("#dialog").dialog("open").text("Your message has been submitted."); // You can customize the message here

      // Show the overlay
      $("#overlay").show();

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

      // Reset the form fields (optional)
      $(this).trigger("reset");
    }
  });

  // Initialize form validation
  $("#contactForm").validate({
    rules: {
      name: {
        required: true
      },
      email: {
        required: true,
        email: true
      },
      message: {
        required: true
      }
    },
    messages: {
      name: {
        required: "Please enter your full name."
      },
      email: {
        required: "Please enter your email address.",
        email: "Please enter a valid email address."
      },
      message: {
        required: "Please enter your message."
      }
    },
  });
});
