"""
FastAPI backend for the Raj Kumar portfolio.
Handles terminal commands, GitHub project fetching, and Groq AI chat proxy.
Deployed as a Vercel serverless function.
"""

import os
import time
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(title="Portfolio API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Config ───────────────────────────────────────────────
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "RKG765")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
CACHE_TTL = 600  # 10 minutes

# ── In-Memory Cache ─────────────────────────────────────
_projects_cache: dict = {"data": None, "timestamp": 0}


# ── Pydantic Models ─────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

class ChatResponse(BaseModel):
    reply: str


# ── /api/projects — Cached GitHub Repos ─────────────────

@app.get("/api/projects")
async def get_projects():
    """
    Fetch featured GitHub repos with caching.
    Filters: no forks, no archived, sorted by recent update.
    Returns normalized project data.
    """
    now = time.time()

    # Serve from cache if fresh
    if _projects_cache["data"] and (now - _projects_cache["timestamp"]) < CACHE_TTL:
        return {"projects": _projects_cache["data"], "cached": True}

    # Fetch from GitHub API
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"https://api.github.com/users/{GITHUB_USERNAME}/repos",
                params={
                    "sort": "updated",
                    "direction": "desc",
                    "per_page": 30,
                    "type": "owner",
                },
                headers=headers,
            )
            resp.raise_for_status()
            repos = resp.json()

        # Filter: no forks, no archived
        filtered = [r for r in repos if not r.get("fork") and not r.get("archived")]

        # Normalize to clean project objects
        projects = []
        for repo in filtered[:10]:
            tech = []
            # Primary language
            if repo.get("language"):
                tech.append(repo["language"])
            # Topics as additional tech
            for topic in repo.get("topics", []):
                if topic not in [t.lower() for t in tech]:
                    tech.append(topic)

            projects.append({
                "name": repo.get("name", ""),
                "description": (repo.get("description") or "No description")[:120],
                "tech": tech[:5],
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url", ""),
                "updated": repo.get("updated_at", ""),
                "homepage": repo.get("homepage") or "",
            })

        # Update cache
        _projects_cache["data"] = projects
        _projects_cache["timestamp"] = now

        return {"projects": projects, "cached": False}

    except Exception as e:
        # If cache exists but expired, serve stale
        if _projects_cache["data"]:
            return {"projects": _projects_cache["data"], "cached": True, "stale": True}

        return {"projects": [], "error": str(e)}


# ── /api/chat — Groq LLaMA Chat Proxy ──────────────────

@app.post("/api/chat", response_model=ChatResponse)
async def chat_proxy(req: ChatRequest):
    """Proxy chat messages to Groq API (LLaMA 3)."""
    if not GROQ_API_KEY:
        return ChatResponse(
            reply="⚠️  GROQ_API_KEY not configured.\n"
                  "The AI chat feature requires a Groq API key."
        )

    system_prompt = (
        "You are the AI assistant inside Raj Kumar's portfolio terminal. "
        "Raj is a B.Tech CSE student at BML Munjal University who builds "
        "backend systems, DevOps pipelines, and AI/ML tools. "
        "Keep responses concise and technical."
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in req.history[-10:]:
        messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
    messages.append({"role": "user", "content": req.message})

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "max_tokens": 1024,
                    "temperature": 0.7,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
            return ChatResponse(reply=reply)
    except httpx.HTTPStatusError as e:
        return ChatResponse(reply=f"⚠️  Groq API error: {e.response.status_code}")
    except Exception as e:
        return ChatResponse(reply=f"⚠️  Gateway error: {str(e)}")


# ── /api/health ─────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "portfolio-api"}
