"""FastAPI entry point for the AI Code Assistant."""

from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.orchestrator import CodeAssistant
from app.schema import AskRequest, AskResponse
from app.url_utils import fetch_url_content

load_dotenv()

app = FastAPI(
    title="AI Code Assistant",
    description="A FastAPI service that explains, debugs, and improves code requests.",
    version="1.0.0",
)

assistant = CodeAssistant()


def is_code_request(text: str) -> bool:
    lower = text.lower().strip()
    if lower.startswith("http://") or lower.startswith("https://"):
        return True

    language_keywords = [
        "python", "javascript", "java", "c#", "c\+\+", "cpp", "html", "css",
        "sql", "ruby", "php", "go", "golang", "typescript", "bash", "shell",
        "kotlin", "swift", "rust", "scala", "perl", "dart", "react",
        "angular", "vue", "node", "django", "flask", "spring", "android",
        "ios", "xcode", "mongodb", "firebase",
    ]
    code_markers = [
        "```", "`", "def ", "class ", "import ", "console.log", "printf(", "system.out",
        "function ", "=>", "var ", "let ", "const ", "#include", "#define", "#pragma",
        "//", "/*", "*/",
    ]
    programming_terms = [
        "programming", "syntax", "compile", "debug", "error", "exception",
        "loop", "function", "method", "variable", "script", "framework", "library",
        "package", "query", "algorithm", "git", "terminal",
    ]

    import re

    # Detect explicit programming language mention using whole words.
    for keyword in language_keywords:
        if re.search(rf"\b{re.escape(keyword)}\b", lower):
            return True

    # Detect explicit programming concepts using whole words.
    for term in programming_terms:
        if re.search(rf"\b{re.escape(term)}\b", lower):
            return True

    # Detect code-like content using common code markers.
    for marker in code_markers:
        if marker in text:
            return True

    return False


def build_request_text(request: AskRequest) -> str:
    parts = []
    if request.question and request.question.strip():
        parts.append(request.question.strip())

    if request.url and request.url.strip():
        try:
            fetched_content = fetch_url_content(request.url.strip())
            if fetched_content:
                parts.append(f"URL Content:\n{fetched_content}")
            else:
                parts.append(f"URL: {request.url.strip()}")
        except Exception:
            parts.append(f"URL: {request.url.strip()}")

    return "\n".join(parts) if parts else "Please analyze the provided request."


def run_assistant_pipeline(request: AskRequest) -> AskResponse:
    prompt = build_request_text(request)
    response = assistant.run(prompt)
    return AskResponse(intent=response["intent"], answer=response["answer"])


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>AI Code Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; background: #f4f6fb; }
            h1 { color: #111827; }
            textarea, input { width: 100%; padding: 0.75rem; font-family: Consolas, monospace; font-size: 0.95rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; box-sizing: border-box; }
            textarea { height: 220px; }
            input { margin-top: 0.75rem; }
            button { padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; font-size: 1rem; background: #2563eb; color: white; border-color: #2563eb; cursor: pointer; }
            button:hover { background: #1d4ed8; }
            .response { margin-top: 1.5rem; padding: 1rem; background: white; border: 1px solid #cbd5e1; border-radius: 0.75rem; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>AI Code Assistant</h1>
        <p>Paste your code, describe your issue, or enter a URL below, then click <strong>Explain</strong>.</p>
        <form id="ask-form">
            <textarea id="question" placeholder="Enter your code or question here..."></textarea>
            <input id="url" type="url" placeholder="Optional URL (for example: https://example.com)" />
            <div style="margin-top: 1rem;">
                <button type="submit">Explain</button>
            </div>
        </form>
        <div class="response" id="answer">Submit a request to see the explanation.</div>
        <script>
            const form = document.getElementById('ask-form');
            const answerDiv = document.getElementById('answer');

            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                answerDiv.textContent = 'Thinking...';

                const question = document.getElementById('question').value.trim();
                const url = document.getElementById('url').value.trim();
                if (!question && !url) {
                    answerDiv.textContent = 'Please enter some code, a programming-language request, or a URL.';
                    return;
                }

                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question, url }),
                    });
                    const result = await response.json();
                    if (!response.ok) {
                        answerDiv.textContent = 'Error: ' + (result.detail || 'Please enter the code or a programming language question.');
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
        combined_text = " ".join(
            part for part in [request.question or "", request.url or ""] if part
        )
        if not combined_text or not is_code_request(combined_text):
            raise ValueError(
                "Please enter code, a programming-language-related request, or a URL."
            )
        return run_assistant_pipeline(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
