
import unittest

from water_jug_solver import (
    WaterJugProblem,
    breadth_first_search,
    get_solution_path,
)


class TestWaterJugProblem(unittest.TestCase):

    def setUp(self):
        self.problem = WaterJugProblem()

    def test_initial_state(self):
        self.assertEqual(self.problem.initial, (0, 0, 0))

    def test_goal_detection(self):
        self.assertTrue(self.problem.is_goal((1, 0, 0)))
        self.assertTrue(self.problem.is_goal((0, 1, 0)))
        self.assertTrue(self.problem.is_goal((0, 0, 1)))
        self.assertFalse(self.problem.is_goal((0, 0, 0)))

    def test_fill_transition(self):
        self.assertEqual(
            self.problem.result((0, 0, 0), ("fill", 0)),
            (12, 0, 0),
        )

    def test_pour_transition(self):
        self.assertEqual(
            self.problem.result((12, 0, 0), ("pour", 0, 1)),
            (4, 8, 0),
        )

    def test_bfs_finds_goal(self):
        goal = breadth_first_search(self.problem)
        self.assertIsNotNone(goal)
        self.assertTrue(self.problem.is_goal(goal.state))

    def test_solution_path(self):
        goal = breadth_first_search(self.problem)
        path = get_solution_path(goal)

        self.assertEqual(path[0].state, (0, 0, 0))
        self.assertTrue(self.problem.is_goal(path[-1].state))

        for previous, current in zip(path, path[1:]):
            valid_states = [
                child.state for child in self.problem.expand(previous)
            ]
            self.assertIn(current.state, valid_states)


if __name__ == "__main__":
    unittest.main()
