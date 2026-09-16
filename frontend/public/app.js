const input = document.getElementById("message-input");
const button = document.getElementById("send-button");
const chatBox = document.getElementById("chat-box");


// ================= FORMAT RESPONSE =================

function formatResponse(text) {

    if (!text) {
        return "";
    }

    let formatted = String(text);

    // Escape HTML
    formatted = formatted
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Code blocks
    formatted = formatted.replace(
        /```(?:python|javascript|js|html|css|json)?\n?([\s\S]*?)```/g,
        "<pre><code>$1</code></pre>"
    );

    // Bold
    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    // Headings
    formatted = formatted.replace(
        /^### (.*)$/gm,
        "<h3>$1</h3>"
    );

    // Bullet points
    formatted = formatted.replace(
        /^\* (.*)$/gm,
        "• $1"
    );

    // New lines
    formatted = formatted.replace(/\n/g, "<br>");

    return formatted;
}


// ================= ADD MESSAGE =================

function addMessage(sender, text, isUser = false) {

    const message = document.createElement("div");

    message.className = isUser
        ? "message user"
        : "message";

    const avatar = isUser
        ? "👤"
        : "✦";

    message.innerHTML = `
        ${isUser ? "" : `<div class="avatar">${avatar}</div>`}

        <div class="message-content">

            <div class="message-name">
                ${isUser ? "YOU" : "AURA"}
            </div>

            <div class="message-text">
                ${formatResponse(text)}
            </div>

        </div>

        ${isUser ? `<div class="avatar">${avatar}</div>` : ""}
    `;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// ================= TYPING =================

function showTyping() {

    const typing = document.createElement("div");

    typing.id = "typing";
    typing.className = "message";

    typing.innerHTML = `
        <div class="avatar">✦</div>

        <div class="message-content">

            <div class="message-name">
                AURA
            </div>

            <div class="message-text">

                <div class="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>

            </div>

        </div>
    `;

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


// ================= SEND MESSAGE =================

async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    addMessage("You", message, true);

    input.value = "";
    input.style.height = "auto";

    button.disabled = true;

    showTyping();

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        if (!response.ok) {
            throw new Error(
                "Server error: " + response.status
            );
        }


        const data = await response.json();

        removeTyping();

        addMessage(
            "AURA",
            data.response,
            false
        );

    }

    catch (error) {

        console.error("Chat error:", error);

        removeTyping();

        addMessage(
            "AURA",
            "Sorry, something went wrong while connecting to the backend.",
            false
        );
    }

    finally {

        button.disabled = false;

        input.focus();
    }
}


// ================= SUGGESTIONS =================

function useSuggestion(text) {

    input.value = text;

    input.focus();

    sendMessage();
}


// ================= NEW CHAT =================

function newChat() {

    chatBox.innerHTML = `
        <div class="welcome">

            <div class="welcome-icon">✦</div>

            <h1>How can I help you?</h1>

            <p>
                Ask me anything. I can answer questions, research documents,
                help with coding and interact with APIs.
            </p>

            <div class="suggestions">

                <button onclick="useSuggestion('Explain Python in simple words')">
                    <span></span>
                    Explain Python
                </button>

                <button onclick="useSuggestion('Write a Python program to check prime number')">
                    <span>💻</span>
                    Write Python code
                </button>

                <button onclick="useSuggestion('What are the features of Python according to the document?')">
                    <span>📚</span>
                    Ask from document
                </button>

                <button onclick="useSuggestion('Get information from GitHub API')">
                    <span>🔗</span>
                    Test API tool
                </button>

            </div>

        </div>
    `;

    input.focus();
}


// ================= EVENTS =================

button.addEventListener("click", sendMessage);


input.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }

});


// Auto-grow textarea
input.addEventListener("input", function() {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 130) + "px";

});