document.getElementById('submitUser').addEventListener('submit', function(event) {
    event.preventDefault();

    const userid = document.getElementById('userid').value;
    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const email = document.getElementById('email').value;
    const address = document.getElementById('address').value;
    const contactnumber = document.getElementById('contactnumber').value;

    fetch('https://<your-function-app-name>.azurewebsites.net/api/register-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            userid: userid,
            firstname: firstname,
            lastname: lastname,
            email: email,
            address: address,
            contactnumber: contactnumber
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('registeruser').innerText = data.message;
    })
    .catch(error => {
        document.getElementById('registeruser').innerText = "Error registering user!";
        console.error('Error:', error);
    });
});
