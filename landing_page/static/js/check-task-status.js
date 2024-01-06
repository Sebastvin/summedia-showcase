function checkTaskStatus(taskId, fullUrl)
{
    let checkInterval = setInterval(function () {
        fetch(fullUrl)
            .then(response => response.json())
            .then(data => {
                // console.log("Task status", data.status);

                if (data.status === 'SUCCESS') {
                    // Stop checking
                    document.getElementById('loading').style.display = 'none';

                    clearInterval(checkInterval);
                    document.getElementById("output").innerText = data.result;
                    // console.log('Task Result:', data.result);

                } else if(data.status === 'FAILURE')
                {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById("output").innerText = "Something go wrong, check again...";
                }
        })
        .catch(error => console.error('Error:', error ));
    }, 3000);
}