from fastapi import FastAPI
import uvicorn

from env.environment import SupportEnv
from env.models import Action
from env.tasks import EasyTask

app = FastAPI()

env = SupportEnv(EasyTask())


@app.get("/")
def root():
    return {"message": "OpenEnv API running"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "ticket_id": obs.ticket_id,
        "customer_query": obs.customer_query,
        "history": obs.history
    }


@app.post("/step")
def step(action: dict):
    act = Action(**action)
    obs, reward, done, _ = env.step(act)

    return {
        "observation": {
            "ticket_id": obs.ticket_id,
            "customer_query": obs.customer_query,
            "history": obs.history
        },
        "reward": {
            "score": reward.score,
            "feedback": reward.feedback
        },
        "done": done
    }


@app.get("/state")
def state():
    return {"status": "running"}


# 🔥 REQUIRED MAIN FUNCTION
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# 🔥 REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()