let screen_name = null;

document.addEventListener('DOMContentLoaded', function() {
    // Get the URL parameters
    let urlParams = new URLSearchParams(window.location.search);

    // Check if the parameter exists
    if (urlParams.has('parameter')) {
        // Retrieve the parameter value
        screen_name = urlParams.get('parameter');

        // Use the parameter value as needed
        console.log('Parameter value:', screen_name);
    } else {
        console.log('Parameter not found');
    }
});