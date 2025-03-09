const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    themeToggle.textContent = isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode';
});

// Load existing chats on page load
async function loadChats() {
    try {
        const response = await fetch('/get-chats');
        const chats = await response.json();
        const chatBox = document.getElementById('chat-box');
        const chatCount = document.getElementById('chat-count');

        chatBox.innerHTML = '';
        chats.forEach(chat => {
            const chatItem = document.createElement('li');
            chatItem.textContent = `${chat.username}: ${chat.message}`;
            chatBox.appendChild(chatItem);
        });

        chatCount.textContent = chats.length;
    } catch (error) {
        console.error('Error loading chats:', error);
    }
}

async function saveChat(newChat) {
    try {
        await fetch('/add-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newChat)
        });
        loadChats();
    } catch (error) {
        console.error('Error saving chat:', error);
    }
}

document.getElementById('chat-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const message = document.getElementById('message').value;
    saveChat({ username, message });
    document.getElementById('chat-form').reset();
});

loadChats();
