class Grader:

    def grade_easy(self, ticket, action):
        if action.action_type == "classify":
            if action.content == ticket["label"]:
                return 1.0, "Correct classification"
        return 0.0, "Incorrect classification"


    def grade_medium(self, ticket, action):
        score = 0.0

        if action.action_type == "classify":
            if action.content == ticket["label"]:
                score += 0.5

        if action.action_type == "respond":
            if action.content and "sorry" in action.content.lower():
                score += 0.5

        return score, "Medium grading complete"


    def grade_hard(self, ticket, action):
        score = 0.0

        if action.action_type == "classify":
            if action.content == ticket["label"]:
                score += 0.3

        if action.action_type == "respond":
            if action.content and "check" in action.content.lower():
                score += 0.4

        if action.action_type == "escalate":
            score += 0.3

        return score, "Hard grading complete"