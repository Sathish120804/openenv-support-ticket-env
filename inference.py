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
    print(f"[START] task={name}", flush=True)

    env = SupportEnv(task)
    obs = env.reset()

    total_score = 0

    for step in range(3):
        action = simple_agent(obs)

        obs, reward, done, _ = env.step(action)

        print(
            f"[STEP] step={step+1} reward={reward.score}",
            flush=True
        )

        total_score += reward.score

        if done:
            break

    print(
        f"[END] task={name} score={round(total_score,2)} steps={step+1}",
        flush=True
    )


if __name__ == "__main__":
    run_task(EasyTask(), "Easy")
    run_task(MediumTask(), "Medium")
    run_task(HardTask(), "Hard")