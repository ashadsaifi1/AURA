async function checkFastAPI() {
    const response = await fetch("https://aura-ycsn.onrender.com/");

    if (!response.ok) {
        throw new Error(`FastAPI error: ${response.status}`);
    }

    return await response.json();
}


async function sendMessage(message) {
    const response = await fetch("https://aura-ycsn.onrender.com/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || `FastAPI error: ${response.status}`
        );
    }

    return data;
}


module.exports = {
    checkFastAPI,
    sendMessage
};