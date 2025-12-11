// Event listener for refreshButton class
// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function () {
    // Get the button element by class name
    var refreshButton = document.querySelector('.refreshButton');
    // Check if button exists
    if (refreshButton) {
        // Add click event listener
        refreshButton.addEventListener('click', function () {
            // Send request to Flask endpoint
            fetch('/button-click')
                .then(function (response) { return response.text(); })
                .then(function (data) {
                console.log('Flask responded:', data);
                alert('Hello World');
            })
                .catch(function (error) {
                console.error('Error calling Flask:', error);
            });
        });
    }
    else {
        console.log('Button with class "refreshButton" not found');
    }
});
