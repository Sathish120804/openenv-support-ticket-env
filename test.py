from env.environment import SupportEnv
from env.models import Action
from env.tasks import EasyTask, MediumTask, HardTask

print("---- EASY TASK ----")
env = SupportEnv(EasyTask())
obs = env.reset()
print(obs)

action = Action(action_type="classify", content="delivery")
obs, reward, done, _ = env.step(action)
print(reward)

print("\n---- MEDIUM TASK ----")
env = SupportEnv(MediumTask())
obs = env.reset()
print(obs)

action = Action(action_type="respond", content="Sorry for the issue")
obs, reward, done, _ = env.step(action)
print(reward)

print("\n---- HARD TASK ----")
env = SupportEnv(HardTask())
obs = env.reset()
print(obs)

action = Action(action_type="escalate", content=None)
obs, reward, done, _ = env.step(action)
print(reward)