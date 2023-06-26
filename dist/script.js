window.onload = function() {
    setInterval(fetchData, 500); // Call fetchData every 500ms
}

function fetchData() {
    fetch('/api/state')
        .then(response => response.json())
        .then(data => {
            document.body.innerHTML = JSON.stringify(data, null, 4); // Pretty print JSON
        });
}
