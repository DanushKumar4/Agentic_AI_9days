from .agent import Agent
from .memory import store
from .demotool import campus_registry, CAMPUS_INSTRUCTIONS


# Create the agent with the campus tools.
agent = Agent(
    name="campus-assistant",
    instructions=CAMPUS_INSTRUCTIONS,
    registry=campus_registry(),
)


def chat(thread_id: str, user_message: str):
    history = store.load(thread_id)

    result = agent.run(
        user_message,
        history=history,
    )

    store.save(thread_id, result.messages)

    return result

def optimizer(task, previous_draft=None, feedback=None):
    """
    Creates or improves a draft based on evaluator feedback.
    """

    if previous_draft is None:
        return {
            "day1": "Arrays and Prefix Sums - 2 hours",
            "day2": "Binary Search - 2 hours",
            "day3": "Two Pointers and Sliding Window - 2 hours",
            "day4": "Stacks and Queues - 2 hours",
            "day5": "Trees and Binary Search Trees - 2 hours",
            "day6": "Graphs - 2 hours",
            "day7": "Revision + 3 timed problems - 2 hours",
        }

    # In a real agent, the LLM would use the feedback to rewrite the draft.
    # For this exercise, make the improvement explicit.
    improved = previous_draft.copy()

    if feedback:
        improved["day7"] = "Revision of all topics + 3 timed problems - 2 hours"

    return improved


def evaluator(draft, criteria):
    """
    Evaluates a draft against explicit, measurable criteria.
    """

    feedback = []

    # Criterion 1: exactly 7 days
    if len(draft) != 7:
        feedback.append("The plan must contain exactly 7 days.")

    # Criterion 2: every day must contain a DSA topic
    for day, plan in draft.items():
        if not plan.strip():
            feedback.append(f"{day} has no study topic.")

    # Criterion 3: realistic workload
    for day, plan in draft.items():
        if "hours" not in plan:
            feedback.append(f"{day} must specify the workload in hours.")

    # Criterion 4: revision/practice
    if "revision" not in draft["day7"].lower():
        feedback.append("Day 7 must include revision.")

    if "problem" not in draft["day7"].lower():
        feedback.append("Day 7 must include problem-solving practice.")

    return {
        "passed": len(feedback) == 0,
        "feedback": feedback,
    }


def evaluator_optimizer(task):
    criteria = [
        "Covers exactly 7 days",
        "Every day contains a specific DSA topic",
        "Every day specifies a realistic workload",
        "Includes revision",
        "Includes problem-solving practice",
    ]

    draft = optimizer(task)

    while True:
        evaluation = evaluator(draft, criteria)

        print("Evaluation:", evaluation)

        if evaluation["passed"]:
            return draft

        draft = optimizer(
            task,
            previous_draft=draft,
            feedback=evaluation["feedback"],
        )


if __name__ == "__main__":
    task = "Create a 7-day competitive programming study plan."

    final_plan = evaluator_optimizer(task)

    print("\nFinal Plan:")
    for day, plan in final_plan.items():
        print(f"{day}: {plan}")