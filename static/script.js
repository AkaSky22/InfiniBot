document.getElementById('userInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const userMessage = userInput.value.trim();

    if (userMessage === '') return;

    addMessage('user', userMessage);
    userInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('bot', data.reply);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function addMessage(sender, message) {
    const chatlog = document.getElementById('chatlog');
    const messageElement = document.createElement('div');
    messageElement.className = sender;
    messageElement.textContent = `ROBO: ${message}`;
    chatlog.appendChild(messageElement);
    chatlog.scrollTop = chatlog.scrollHeight;
}

