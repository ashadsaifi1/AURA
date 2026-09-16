const express = require("express");
const path = require("path");
const { checkFastAPI, sendMessage } = require("./services/fastapi");

const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.get("/api/test", async (req, res) => {
    try {
        const data = await checkFastAPI();
        res.json(data);
    } catch (error) {
        res.status(500).json({
            error: "FastAPI connection failed"
        });
    }
});

app.post("/api/chat", async (req, res) => {
    try {
        const data = await sendMessage(req.body.message);
        res.json(data);
    } catch (error) {
        res.status(500).json({
            error: "Chat request failed"
        });
    }
});

app.listen(3000, () => {
    console.log("AURA server running on http://localhost:3000");
});