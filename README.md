# DPS970 Activity 1 — Intelligent Agents and Search

## Project Overview

This project implements two problems using Python for DPS970 Activity 1:

1. **Spam Filter Email Agent:** A simple reflex agent that classifies email files as spam or non-spam based on sender domains and bad-word occurrences.
2. **Water Jug Search Problem:** A Breadth-First Search (BFS) algorithm that finds a solution to the water jug problem using 12-gallon, 8-gallon, and 3-gallon jugs.

The project includes written answers, test data, automated unit tests, and a GitHub Actions workflow.

## Project Structure

```text
DPS970_Activity1_Submission/
├── email_agent.py
├── water_jug_solver.py
├── assignment_answers.md
├── README.md
├── test_data/
│   ├── allow_domains.txt
│   ├── blocked_domains.txt
│   ├── spam_words.txt
│   ├── sample_spam.eml
│   └── sample_trusted.eml
├── tests/
│   ├── test_email_agent.py
│   └── test_water_jug.py
└── .github/
    └── workflows/
        └── python_tests.yml
```

The `spam/` and `email/` output directories are created automatically when the email agent runs.

## Requirements

- Python 3.10 or newer
- Visual Studio Code or another Python-compatible editor
- No third-party Python packages are required

## Question 1: Spam Filter Email Agent

The email agent classifies email files using the following rules:

1. If the sender's domain is on the allow list, classify the email as non-spam.
2. Otherwise, if the sender's domain is on the blocked list, classify the email as spam.
3. Otherwise, if more than five occurrences of words from the spam-word list appear in the readable email body, classify the email as spam.
4. Otherwise, classify the email as non-spam.

The allow-list rule takes priority over the blocked-list rule. Word matching is case-insensitive, and repeated occurrences count separately.

### Run the Email Agent

From the project root directory, run:

```bash
python email_agent.py
```

The agent reads `.eml` files from `test_data/` and moves them into the appropriate output directory:

- `spam/` — emails classified as spam
- `email/` — emails classified as non-spam

**Note:** The agent moves the sample files instead of copying them. Restore the `.eml` files to `test_data/` before running the demonstration again.

## Question 2: Water Jug Search Problem

The water jug problem uses three jugs with capacities of 12, 8, and 3 gallons.

A state is represented as `(x, y, z)`, where each value represents the amount of water in the corresponding jug.

- **Initial state:** `(0, 0, 0)`
- **Goal condition:** At least one jug contains exactly one gallon.
- **Actions:** Fill a jug, empty a jug, or pour water from one jug into another.

The BFS implementation follows the structure of Figure 3.9. It uses a FIFO queue for the frontier and a reached set to prevent repeated exploration of states.

### Run the Water Jug Solver

From the project root directory, run:

```bash
python water_jug_solver.py
```

The program displays the solution path, including the sequence of actions and the resulting states.

## Automated Testing

The project uses Python's built-in `unittest` framework.

### Run the Email Agent Tests

```bash
python -m unittest discover -s tests -p "test_email_agent.py" -v
```

### Run the Water Jug Tests

```bash
python -m unittest discover -s tests -p "test_water_jug.py" -v
```

### Run All Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

All tests should pass before submission.

The email tests check sender-domain rules, the bad-word threshold, and file movement. The water jug tests check the initial state, goal detection, state transitions, BFS goal detection, and solution-path validity.

## GitHub Actions

The workflow file is located at:

```text
.github/workflows/python_tests.yml
```

The workflow automatically runs the unit tests when changes are pushed or a pull request is opened. It also runs the water jug solver.

To check the workflow results:

1. Push the project to GitHub.
2. Open the repository.
3. Select the **Actions** tab.
4. Open the latest workflow run and confirm that it succeeds.

## Submission Checklist

- [ ] Both Python implementations are included.
- [ ] Written answers are included in `assignment_answers.md`.
- [ ] Test data is included in `test_data/`.
- [ ] Both test files run successfully.
- [ ] The combined test command passes.
- [ ] The README contains the correct run instructions.
- [ ] The GitHub Actions workflow is included.
- [ ] All required files are included in the final ZIP archive.

## Conclusion

This project demonstrates a rule-based intelligent agent for email classification and an uninformed search algorithm for solving a state-space problem. Both implementations include automated tests to verify their behaviour.