document.getElementById('submitItem').addEventListener('submit', function(event) {
    event.preventDefault();

    const item_name = document.getElementById('item_name').value;
    const description = document.getElementById('description').value;
    const price = document.getElementById('price').value;
    const owner = document.getElementById('owner').value;

    fetch('https://<your-function-url>/api/create-item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: item_name,
            description: description,
            price: price,
            owner: owner
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.message;
    })
    .catch(error => {
        document.getElementById('response').innerText = "Error submitting item!";
        console.error('Error:', error);
    });
});
