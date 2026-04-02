from env.models import Observation, Action, Reward
from env.tasks import EasyTask

class SupportEnv:

    def __init__(self, task=None):
        self.task = task if task else EasyTask()
        self.ticket = None
        self.done = False
        self.history = []
        self.steps = 0

    def reset(self):
        self.ticket = self.task.get_ticket()
        self.done = False
        self.history = []
        self.steps = 0

        return Observation(
            ticket_id=1,
            customer_query=self.ticket["query"],
            history=[]
        )

    def step(self, action: Action):

        self.steps += 1
        self.history.append(action.content if action.content else "")

        score, _, feedback = self.task.evaluate(action, self.ticket)

        reward = score

        if self.steps > 3:
            reward -= 0.2

        if self.steps >= 3:
            self.done = True

        obs = Observation(
            ticket_id=1,
            customer_query=self.ticket["query"],
            history=self.history
        )

        return obs, Reward(score=reward, feedback=feedback), self.done, {}

    def state(self):
        return {
            "ticket": self.ticket,
            "steps": self.steps,
            "history": self.history,
            "done": self.done
        }