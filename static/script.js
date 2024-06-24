function displayText(data) {
    document.getElementById('user_input').disabled = true;
    const wrapperDiv = document.createElement('div');
    wrapperDiv.setAttribute('class', 'wrapper');
    const newDiv = document.createElement('div');
    newDiv.setAttribute('class', 'data');
    wrapperDiv.appendChild(newDiv);
    const newContent = document.createTextNode(data);
    newDiv.appendChild(newContent);
    const currentDiv = document.getElementById('div1');
    document.getElementById('chatwindow').insertBefore(wrapperDiv, currentDiv);
    wrapperDiv.scrollIntoView(false);
    document.getElementById('user_input').disabled = false;
}

function processInput() {
    var user_input = document.getElementById('user_input').value;
    displayText(user_input);
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user_input=' + encodeURIComponent(user_input),
    })
    .then(response => response.text())
    .then(data => {
        displayText(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    document.getElementById('user_input').value='';
}

document.getElementById('send').addEventListener('click', processInput)
document.getElementById('user_input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      processInput();
    }
});