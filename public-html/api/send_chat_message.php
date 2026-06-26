// Remplacer ou compléter votre logique d'envoi dans le script du chat :
function sendMessage() {
    const text = chatInputText.value.trim();
    if (!text) return;
    
    appendMessage('user', text);
    chatInputText.value = '';

    // Générer ou récupérer un session_id unique pour le visiteur
    if (!localStorage.getItem('oyeo_chat_session')) {
        localStorage.setItem('oyeo_chat_session', 'client_' + Math.random().toString(36).substr(2, 9));
    }
    const sessionId = localStorage.getItem('oyeo_chat_session');

    // Envoi synchrone vers Hostinger
    const params = new FormData();
    params.append('message', text);
    params.append('session_id', sessionId);
    params.append('expediteur', 'client');

    fetch('/api/send_chat_message.php', { method: 'POST', body: params });
}

// Écouteur automatique (Polling) pour recevoir les réponses de l'admin toutes les 4 secondes
setInterval(() => {
    const sessionId = localStorage.getItem('oyeo_chat_session');
    if (!sessionId || !chatWindow.classList.contains('active')) return;

    fetch('/api/get_chat_messages.php?session_id=' + sessionId)
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success' && data.messages.length > chatHistory.length) {
                // S'il y a des nouveaux messages de l'admin en BDD, on met à jour l'interface
                chatBody.innerHTML = ''; // On rafraîchit proprement
                data.messages.forEach(msg => {
                    const msgDiv = document.createElement('div');
                    msgDiv.className = `chat-msg ${msg.expediteur === 'user' || msg.expediteur === 'client' ? 'msg-user' : 'msg-bot'}`;
                    msgDiv.textContent = msg.message;
                    chatBody.appendChild(msgDiv);
                });
                chatBody.scrollTop = chatBody.scrollHeight;
                chatHistory = data.messages;
            }
        });
}, 4000);