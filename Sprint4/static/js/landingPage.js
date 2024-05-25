$(document).ready(function () {
    // Fade in text area
    $(".textArea").fadeIn(1000);

    // Update date and time
    function updateDateTime() {
        $.ajax({
            url: 'http://worldtimeapi.org/api/timezone/Europe/Istanbul',
            method: 'GET',
            success: function (data) {
                var datetime = new Date(data.datetime);
                var date = datetime.toLocaleDateString('tr-TR');
                var time = datetime.toLocaleTimeString('tr-TR');
                $('#datetime').html('' + date + '<br>' + time);
            },
            error: function (error) {
                console.error('Error fetching date and time:', error);
                $('#datetime').text('Failed to load date and time.');
            }
        });
    }

    // Update date and time on page load
    updateDateTime();

    // Update date and time every millisecond
    setInterval(updateDateTime, 1000); // 1000 milliseconds = 1 second

    var messages = [];
    var currentIndex = 0;

    // Update message
    function updateMessage() {
        if (messages.length > 0) {
            $('.message').fadeOut(function () {
                $(this).text(messages[currentIndex]).fadeIn();
                currentIndex = (currentIndex + 1) % messages.length;
            });
        }
    }

    // Fetch messages
    $.ajax({
        url: '/messages',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            messages = data;
            updateMessage();
            setInterval(updateMessage, 2000); // 2000 milliseconds = 2 seconds
        },
        error: function (error) {
            console.error('Error fetching messages:', error);
            $('.message').text('Failed to load messages.');
        }
    });
});