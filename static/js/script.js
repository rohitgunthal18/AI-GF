document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    
    // Function to format the current time for messages
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messagePara = document.createElement('p');
        messagePara.innerHTML = message; // Using innerHTML to render emojis properly
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = getCurrentTime();
        
        messageContent.appendChild(messagePara);
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to send the user message to the API and get a response
    async function sendMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                return data.response;
            } else {
                console.error('Error:', data.error);
                return 'Sorry, I encountered an error. Please try again later. 😢';
            }
        } catch (error) {
            console.error('Error:', error);
            return 'Sorry, I encountered an error. Please try again later. 😢';
        }
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing';
        typingDiv.id = 'typing-indicator';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const typingDots = document.createElement('div');
        typingDots.className = 'typing-dots';
        typingDots.innerHTML = '<span></span><span></span><span></span>';
        
        messageContent.appendChild(typingDots);
        typingDiv.appendChild(messageContent);
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Get response from API
        const response = await sendMessage(message);
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add bot response to chat
        addMessage(response);
    });

    // Add some CSS for the typing indicator
    const style = document.createElement('style');
    style.textContent = `
        .typing-dots {
            display: flex;
            gap: 4px;
            align-items: center;
        }
        
        .typing-dots span {
            width: 8px;
            height: 8px;
            background: #aaa;
            border-radius: 50%;
            display: inline-block;
            animation: bounce 1.3s infinite;
        }
        
        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-4px);
            }
        }
    `;
    document.head.appendChild(style);
}); 