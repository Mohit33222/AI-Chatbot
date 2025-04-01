// Send user message to Flask backend
function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    addMessage('user', message);
    input.value = '';

    fetch('/chat', {
        method: 'POST',
        body: JSON.stringify({ message: message }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        addMessage('bot', data.response);
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('bot', "An error occurred.");
    });
}

// Add messages to the chatbox
function addMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.textContent = message;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("message");
    const sendButton = document.getElementById("send-btn");

    // Pressing 'Enter' triggers the send button click
    inputField.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();  // Prevent form submission
            sendButton.click();
        }
    });

    // Sending the message
    sendButton.addEventListener("click", () => {
        const message = inputField.value.trim();
        
        if (message === "") return;  // Prevent sending empty messages
        
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
            const chatBox = document.getElementById("chat-box");
            
            // Append user message
            const userMessage = `<div class="message user-message">${message}</div>`;
            chatBox.innerHTML += userMessage;

            // Append bot response
            const botMessage = `<div class="message bot-message">${data.response}</div>`;
            chatBox.innerHTML += botMessage;

            inputField.value = "";  // Clear the input field

            // Scroll to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => console.error("Error:", error));
    });
});
