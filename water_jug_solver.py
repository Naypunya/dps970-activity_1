
from collections import deque
from dataclasses import dataclass


@dataclass
class Node:
    state: tuple
    parent: object = None
    action: str = None


class WaterJugProblem:
    capacities = (12, 8, 3)

    def __init__(self):
        self.initial = (0, 0, 0)

    def is_goal(self, state):
        return 1 in state

    def actions(self, state):
        possible = []

        for i, amount in enumerate(state):
            if amount < self.capacities[i]:
                possible.append(("fill", i))
            if amount > 0:
                possible.append(("empty", i))

        for i, amount in enumerate(state):
            if amount == 0:
                continue

            for j, target in enumerate(state):
                if i != j and target < self.capacities[j]:
                    possible.append(("pour", i, j))

        return possible

    def result(self, state, action):
        amounts = list(state)
        operation = action[0]
        i = action[1]

        if operation == "fill":
            amounts[i] = self.capacities[i]

        elif operation == "empty":
            amounts[i] = 0

        elif operation == "pour":
            j = action[2]
            quantity = min(
                amounts[i],
                self.capacities[j] - amounts[j],
            )
            amounts[i] -= quantity
            amounts[j] += quantity

        return tuple(amounts)

    def expand(self, node):
        children = []

        for action in self.actions(node.state):
            state = self.result(node.state, action)
            children.append(
                Node(state, node, self.describe(action))
            )

        return children

    @staticmethod
    def describe(action):
        names = ("12-gallon", "8-gallon", "3-gallon")
        if action[0] == "fill":
            return f"Fill {names[action[1]]} jug"
        if action[0] == "empty":
            return f"Empty {names[action[1]]} jug"
        return (
            f"Pour {names[action[1]]} jug into "
            f"{names[action[2]]} jug"
        )


def breadth_first_search(problem):
    node = Node(problem.initial)

    if problem.is_goal(node.state):
        return node

    frontier = deque([node])
    reached = {problem.initial}

    while frontier:
        node = frontier.popleft()

        for child in problem.expand(node):
            state = child.state

            if problem.is_goal(state):
                return child

            if state not in reached:
                reached.add(state)
                frontier.append(child)

    return None


def get_solution_path(node):
    path = []

    while node is not None:
        path.append(node)
        node = node.parent

    return list(reversed(path))


def main():
    problem = WaterJugProblem()
    goal = breadth_first_search(problem)

    if goal is None:
        print("No solution found.")
        return

    path = get_solution_path(goal)
    print(f"Solution found in {len(path) - 1} actions.")

    for index, node in enumerate(path):
        if index == 0:
            print(f"Start: {node.state}")
        else:
            print(f"{index}. {node.action} -> {node.state}")

    print("Goal reached:", problem.is_goal(goal.state))


if __name__ == "__main__":
    main()
