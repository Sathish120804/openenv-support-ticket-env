from env.grader import Grader

grader = Grader()

class EasyTask:
    def get_ticket(self):
        return {
            "query": "My order is delayed, where is it?",
            "label": "delivery",
            "type": "easy"
        }

    def evaluate(self, action, ticket):
        score, feedback = grader.grade_easy(ticket, action)
        return score, True, feedback


class MediumTask:
    def get_ticket(self):
        return {
            "query": "I received a damaged product",
            "label": "refund",
            "type": "medium"
        }

    def evaluate(self, action, ticket):
        score, feedback = grader.grade_medium(ticket, action)
        return score, True, feedback


class HardTask:
    def get_ticket(self):
        return {
            "query": "Payment deducted but order not confirmed",
            "label": "payment_issue",
            "type": "hard"
        }

    def evaluate(self, action, ticket):
        score, feedback = grader.grade_hard(ticket, action)
        return score, True, feedback