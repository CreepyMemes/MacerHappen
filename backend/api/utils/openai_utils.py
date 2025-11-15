import json
from typing import List, Dict
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

def rank_events_with_llm(user_profile: str, events: List[Dict]) -> List[int]:
    """
    Uses an LLM to rank events by relevance.
    :param user_profile: text describing the participant (preferences, liked events, etc.)
    :param events: list of dicts, each with at least id, title, description, price, categories
    :return: list of event_ids ordered from most to least relevant
    """
    if not events:
        return []

    system_prompt = (
        "You are a recommendation engine for events. "
        "Given a user profile and a list of events, you must return ONLY JSON with "
        "a single key 'ranked_event_ids', an array of event IDs ordered from most "
        "to least relevant for this user."
    )

    user_prompt = (
        "USER PROFILE:\n"
        f"{user_profile}\n\n"
        "EVENTS (as JSON list):\n"
        f"{json.dumps(events, ensure_ascii=False)}\n\n"
        "Return JSON like:\n"
        "{\"ranked_event_ids\": [1, 5, 2, ...]}\n"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-nano",  
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        ranked_ids = data.get("ranked_event_ids", [])
        return [int(eid) for eid in ranked_ids if isinstance(eid, (int, str))]
    except Exception:
        return [e["id"] for e in events]


def moderate_event_content(title: str, description: str) -> Dict[str, str]:
    """
    Uses an LLM to decide whether an event is allowed.
    Returns dict: {"approved": bool, "reason": str}
    """
    system_prompt = (
        "You are a strict content moderator for an events platform. "
        "You must decide if an event is safe and appropriate to show to the public.\n\n"
        "Reject content that includes ANY of the following:\n"
        "- explicit sexual content, pornography, sexual services\n"
        "- hate speech, harassment, threats, or incitement to violence\n"
        "- self-harm encouragement, suicide promotion\n"
        "- illegal activities (hard drugs, weapons trading, etc.)\n"
        "- highly graphic violence or gore\n\n"
        "If the content is borderline but mostly safe (e.g. nightlife, parties, clubs), approve it.\n"
        "Respond ONLY with JSON: {\"approved\": true/false, \"reason\": \"short explanation\"}."
    )

    user_prompt = (
        f"TITLE: {title}\n\n"
        f"DESCRIPTION: {description}\n"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",          # or your chosen model
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        approved = bool(data.get("approved", False))
        reason = data.get("reason", "")
        return {"approved": approved, "reason": reason}
    except Exception:
        # Fail-safe: if parsing fails, mark as not approved with generic reason
        return {"approved": False, "reason": "Automatic moderation failed; requires manual review."}