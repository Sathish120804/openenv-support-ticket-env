from fastapi import FastAPI
import uvicorn
import os
import json

from openai import OpenAI

from env.environment import SupportEnv
from env.models import Action
from env.tasks import EasyTask, MediumTask, HardTask

# 🔥 FastAPI app (Phase 1)
app = FastAPI()


# 🔥 API ENDPOINTS
@app.get("/")
def root():
    return {"message": "OpenEnv API running"}


@app.post("/reset")
def reset():
    env = SupportEnv(EasyTask())
    obs = env.reset()

    return {
        "ticket_id": obs.ticket_id,
        "customer_query": obs.customer_query,
        "history": obs.history
    }


@app.get("/state")
def state():
    return {"status": "running"}


# 🔥 LLM AGENT (Phase 2 REQUIREMENT)
def simple_agent(obs):
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )

    prompt = f"""
You are a customer support assistant.

Classify or respond to the query.

Allowed actions:
- classify → delivery / payment_issue / damaged
- respond → apology or resolution

Query: {obs.customer_query}

Return ONLY JSON:
{{
  "action_type": "classify or respond",
  "content": "value"
}}
"""

    try:
        response = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content.strip()

        parsed = json.loads(output)
        return Action(**parsed)

    except:
        # 🔥 fallback (MANDATORY)
        return Action(action_type="classify", content="delivery")


# 🔥 TASK RUNNER (Phase 2 logs)
def run_task(task, name):
    print(f"[START] task={name}", flush=True)

    env = SupportEnv(task)
    obs = env.reset()

    total_score = 0

    for step in range(3):
        action = simple_agent(obs)
        obs, reward, done, _ = env.step(action)

        print(f"[STEP] step={step+1} reward={reward.score}", flush=True)

        total_score += reward.score

        if done:
            break

    print(f"[END] task={name} score={round(total_score,2)} steps={step+1}", flush=True)


# 🔥 MAIN ENTRY (RUN EVERYTHING)
def main():
    # Phase 2 execution
    run_task(EasyTask(), "Easy")
    run_task(MediumTask(), "Medium")
    run_task(HardTask(), "Hard")

    # Phase 1 API
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# 🔥 REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()