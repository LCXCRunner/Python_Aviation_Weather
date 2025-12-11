// Event listener for refreshButton class

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    // Get the button element by class name
    const refreshButton = document.querySelector('.refreshButton') as HTMLElement;
    
    // Check if button exists
    if (refreshButton) {
        // Add click event listener
        refreshButton.addEventListener('click', () => {
            // Send request to Flask endpoint
            fetch('/button-click')
                .then(response => response.text())
                .then(data => {
                    console.log('Flask responded:', data);
                    alert('Hello World');
                })
                .catch(error => {
                    console.error('Error calling Flask:', error);
                });
        });
    } else {
        console.log('Button with class "refreshButton" not found');
    }
});
