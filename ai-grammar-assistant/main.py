"""FastAPI entry point for the AI Grammar Assistant."""

from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.orchestrator import GrammarAssistant
from app.schema import AskRequest, AskResponse

load_dotenv()

app = FastAPI(
    title="AI Grammar Assistant",
    description="A FastAPI service that corrects grammar and improves English writing.",
    version="1.0.0",
)

assistant = GrammarAssistant()


def run_assistant_pipeline(request: AskRequest) -> AskResponse:
    response = assistant.run(request.text)
    return AskResponse(answer=response["answer"])


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>AI Grammar Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; background: #f8fafc; }
            h1 { color: #111827; }
            textarea { width: 100%; height: 220px; padding: 1rem; font-family: Arial, sans-serif; font-size: 1rem; border: 1px solid #cbd5e1; border-radius: 0.75rem; box-sizing: border-box; }
            button { padding: 0.75rem 1.25rem; border-radius: 0.75rem; border: none; background: #2563eb; color: white; font-size: 1rem; cursor: pointer; }
            button:hover { background: #1d4ed8; }
            .response { margin-top: 1.5rem; padding: 1rem; background: white; border: 1px solid #cbd5e1; border-radius: 0.75rem; white-space: pre-wrap; min-height: 120px; }
        </style>
    </head>
    <body>
        <h1>AI Grammar Assistant</h1>
        <p>Paste your English text below and click <strong>Correct</strong> to improve grammar and style.</p>
        <form id="ask-form">
            <textarea id="text" placeholder="Enter text to correct and improve..."></textarea>
            <div style="margin-top: 1rem;">
                <button type="submit">Correct</button>
            </div>
        </form>
        <div class="response" id="answer">Your corrected text will appear here.</div>
        <script>
            const form = document.getElementById('ask-form');
            const answerDiv = document.getElementById('answer');

            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                answerDiv.textContent = 'Correcting...';

                const text = document.getElementById('text').value.trim();
                if (!text) {
                    answerDiv.textContent = 'Please enter some text.';
                    return;
                }

                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text }),
                    });
                    const result = await response.json();
                    if (!response.ok) {
                        answerDiv.textContent = 'Error: ' + (result.detail || 'Unknown error');
                        return;
                    }
                    answerDiv.textContent = result.answer;
                } catch (error) {
                    answerDiv.textContent = 'Request failed: ' + error.message;
                }
            });
        </script>
    </body>
    </html>
    """


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    try:
        return run_assistant_pipeline(request)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
