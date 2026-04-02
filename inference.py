import sys
import os

# 🔥 Fix path for Docker / Hugging Face
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from env.environment import SupportEnv
from env.models import Action
from env.tasks import EasyTask, MediumTask, HardTask


def simple_agent(obs):
    query = obs.customer_query.lower()

    if "delayed" in query:
        return Action(action_type="classify", content="delivery")

    if "damaged" in query:
        return Action(action_type="respond", content="Sorry for the issue")

    if "payment" in query:
        return Action(action_type="classify", content="payment_issue")

    return Action(action_type="classify", content="delivery")


def run_task(task, name):
    print(f"[START] {name}")

    env = SupportEnv(task)
    obs = env.reset()

    total_score = 0

    for step in range(3):
        action = simple_agent(obs)

        obs, reward, done, _ = env.step(action)

        print(f"[STEP] action={action.action_type} score={reward.score}")

        total_score += reward.score

        if done:
            break

    print(f"[END] {name} total_score={round(total_score, 2)}")


if __name__ == "__main__":
    run_task(EasyTask(), "Easy Task")
    run_task(MediumTask(), "Medium Task")
    run_task(HardTask(), "Hard Task")