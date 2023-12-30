document.addEventListener('DOMContentLoaded', function() {
    let form = document.querySelector('form');

    document.getElementById('fetch-data').addEventListener('click', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            form.reportValidity();
        } else {
            document.getElementById('loading').style.display = 'block'; // Show loading if valid
        }
    });
});