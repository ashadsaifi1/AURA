async function checkFastAPI() {
    const response = await fetch("http://127.0.0.1:8000/");

    if (!response.ok) {
        throw new Error(`FastAPI error: ${response.status}`);
    }

    return await response.json();
}


async function sendMessage(message) {
    const response = await fetch("http://127.0.0.1:8000/chat", {
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