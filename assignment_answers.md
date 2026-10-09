# DPS970 Activity 1 — Assignment Answers

## Question 1: Spam Filter Email Agent (40%)

### 1.1 PEAS Description

PEAS stands for Performance Measure, Environment, Actuators, and Sensors. It describes the task environment of an intelligent agent.

| Component | Description |
|---|---|
| **Performance Measure** | Correctly classify emails as spam or not spam, follow the allow-list and blocked-list rules, and move emails into the correct folders. |
| **Environment** | Email files in `.eml` format, domain lists, spam-word lists, and the output folders named `spam` and `email`. |
| **Actuators** | Classify emails and move files to either the `spam` folder or the `email` folder. |
| **Sensors** | Read email headers, sender addresses, readable email bodies, and the allow-list, blocked-list, and spam-word files. |

### 1.2 Properties of the Task Environment

**Observability:** The environment may be partially observable if some email content is encrypted or encoded and cannot be read. The agent uses the readable information available in the email headers and body. Text attachments are assumed to be readable, as specified in the assignment.

**Deterministic:** The environment is deterministic because the same email and list files produce the same classification when the rules are applied in the same order.

**Episodic:** Each email can be classified independently. Processing one email does not require the classification of another email.

**Static:** An email being processed does not normally change while the agent examines it. However, the file system changes when emails are moved into output folders.

**Discrete:** The agent processes individual email files and produces one of two classifications: spam or not spam.

**Single-agent:** Only one filtering agent is required to perform the task.

### 1.3 Type of Intelligent Agent

The Spam Filter Email Agent is a **simple reflex agent** because it selects an action based on the current email's information and predefined condition-action rules. It does not learn from past emails or maintain an internal model of the environment.

The agent applies the rules in the following order:

1. If the sender's domain is on the allow list, classify the email as **not spam**, regardless of its contents.
2. Otherwise, if the sender's domain is on the blocked list, classify the email as **spam**.
3. Otherwise, count the occurrences of words from the spam-word list in the email body. If the count is greater than five, classify the email as **spam**.
4. Otherwise, classify the email as **not spam**.

The allow list takes priority over the other rules because emails from allow-listed domains must not be classified as spam, regardless of their contents.

### 1.4 Implementation

The agent is implemented in Python. It reads `.eml` files, extracts sender information and readable body text, loads the configured lists, applies the classification rules, and moves each processed email into the appropriate output folder.

The implementation uses the following files:

- `email_agent.py`: Implements the email filtering agent.
- `allow_domains.txt`: Contains trusted sender domains.
- `blocked_domains.txt`: Contains blocked sender domains.
- `spam_words.txt`: Contains words used to identify potential spam.
- `sample_spam.eml`: Provides a sample email for testing.
- `sample_trusted.eml`: Provides a sample email from a trusted sender.

Emails classified as spam are moved into the `spam` folder. Emails classified as not spam are moved into the `email` folder.

### 1.5 Testing

The agent is tested using Python's `unittest` framework.

The test cases include:

1. An email from an allow-listed domain is classified as not spam, even if its body contains many spam words.
2. An email from a blocked domain is classified as spam.
3. An email containing six occurrences of spam-list words is classified as spam when its sender is neither allow-listed nor blocked.
4. An email containing exactly five occurrences of spam-list words is not classified as spam by the spam-word rule alone.
5. The agent moves emails into the correct output folders.
6. The agent handles readable email bodies and multipart email messages appropriately.

GitHub Actions can automatically execute the tests whenever changes are pushed to the repository. This helps verify that the implementation continues to work correctly.

---

## Question 2: Water Jug Problem (60%)

### 2.1 Problem Description

The Water Jug Problem consists of three jugs with capacities of 12 gallons, 8 gallons, and 3 gallons. Initially, all three jugs are empty. The objective is to measure exactly one gallon using the permitted actions:

- Fill a jug completely.
- Empty a jug onto the ground.
- Pour water from one jug into another until the source jug is empty or the destination jug is full.

The jugs have no measurement markings, and no additional measuring equipment is used.

### 2.2 State Representation

Represent each state as a tuple:

\[
S=(x,y,z)
\]

where:

- \(x\) represents the amount of water in the 12-gallon jug.
- \(y\) represents the amount of water in the 8-gallon jug.
- \(z\) represents the amount of water in the 3-gallon jug.

The state must satisfy the following constraints:

\[
0\leq x\leq12
\]

\[
0\leq y\leq8
\]

\[
0\leq z\leq3
\]

Each state describes the current amount of water in all three jugs.

### 2.3 Initial State

Initially, all three jugs are empty.

\[
S_0=(0,0,0)
\]

### 2.4 Goal State

The objective is to obtain exactly one gallon in at least one jug.

The goal test is:

\[
\operatorname{Goal}(S)
\iff
(x=1)\lor(y=1)\lor(z=1)
\]

Examples of goal states include:

\[
(1,0,0),\quad(0,1,0),\quad(0,0,1)
\]

Any state with exactly one gallon in at least one jug satisfies the goal condition.

### 2.5 Actions

The agent can perform three types of actions.

**1. Fill**

Fill any jug to its maximum capacity:

- Fill the 12-gallon jug.
- Fill the 8-gallon jug.
- Fill the 3-gallon jug.

**2. Empty**

Empty any nonempty jug completely onto the ground:

- Empty the 12-gallon jug.
- Empty the 8-gallon jug.
- Empty the 3-gallon jug.

**3. Pour**

Pour water from one jug into another until the source jug is empty or the destination jug is full.

The six possible pouring directions are:

- 12-gallon jug to 8-gallon jug.
- 12-gallon jug to 3-gallon jug.
- 8-gallon jug to 12-gallon jug.
- 8-gallon jug to 3-gallon jug.
- 3-gallon jug to 12-gallon jug.
- 3-gallon jug to 8-gallon jug.

Only actions that change the current state need to be generated.

### 2.6 Transition Model

The transition model describes how an action changes the current state.

**Fill action:** If a jug has capacity \(c\) and currently contains \(v\) gallons, filling it results in:

\[
v'=c
\]

**Empty action:** Emptying a jug results in:

\[
v'=0
\]

**Pour action:** Suppose the source jug contains \(a\) gallons, the destination jug contains \(b\) gallons, and the destination has capacity \(c\). The amount transferred is:

\[
t=\min(a,c-b)
\]

The resulting amounts are:

\[
a'=a-t
\]

\[
b'=b+t
\]

The third jug remains unchanged.

For example, starting from the initial state:

\[
(0,0,0)\xrightarrow{\text{Fill 3-gallon jug}}(0,0,3)
\]

Pouring the water into the 8-gallon jug produces:

\[
(0,0,3)\xrightarrow{\text{Pour 3 into 8}}(0,3,0)
\]

These examples demonstrate how the transition model generates new states from actions.

### 2.7 State Space

The state space contains all possible combinations of water amounts in the three jugs.

The maximum number of possible states is:

\[
(12+1)(8+1)(3+1)
\]

\[
=13\times9\times4
\]

\[
=468
\]

Therefore, there are at most **468 possible states**. Not every state is necessarily reachable from the initial state using the permitted actions.

### 2.8 Search Algorithm: Breadth-First Search

Breadth-First Search (BFS) is used to find a solution. BFS explores states in order of increasing depth, using a first-in, first-out (FIFO) queue.

The algorithm follows the BFS pseudocode from Figure 3.9:

1. Create a node containing the initial state.
2. Check whether the initial state satisfies the goal condition.
3. Initialize a FIFO frontier queue with the initial node.
4. Initialize a reached set containing the initial state.
5. While the frontier is not empty, remove the next node from the queue.
6. Expand the node to generate its valid successor states.
7. If a successor satisfies the goal condition, return that successor.
8. If a successor has not been reached, add its state to the reached set and add the node to the frontier.
9. If the frontier becomes empty without finding a goal, return failure.

The reached set prevents the algorithm from exploring the same state repeatedly. Checking for a goal when a successor is generated follows the ordering shown in Figure 3.9.

### 2.9 Heuristic Function

A heuristic function estimates how close a state is to the goal.

One possible heuristic is:

\[
h(S)=\min(|x-1|,|y-1|,|z-1|)
\]

This function calculates the smallest difference between the current amount in any jug and the target amount of one gallon.

For example, for the state \((0,0,3)\):

\[
h(S)=\min(1,1,2)=1
\]

However, this heuristic does not necessarily estimate the actual number of actions remaining. A state that is numerically close to one gallon may still require several actions to reach the goal.

BFS does not require a heuristic because it explores states by depth rather than using heuristic estimates to select nodes. Therefore, the heuristic is discussed for comparison and is not used to guide the BFS implementation.

### 2.10 Completeness and Optimality

**Completeness:** BFS is complete for this problem because the state space is finite, each state has a finite number of possible actions, and the reached set prevents repeated exploration. If a goal state is reachable, BFS will eventually find it.

**Optimality:** BFS finds a solution with the minimum number of actions when all actions have equal cost. In this implementation, every fill, empty, or pour action counts as one step. Therefore, BFS returns a solution with the fewest actions among the available solutions.

### 2.11 Implementation

The water jug solver is implemented in Python using a state-space search approach.

The implementation includes:

- A state representation using a tuple \((x,y,z)\).
- A goal test that checks whether any jug contains exactly one gallon.
- Actions for filling, emptying, and pouring water.
- A transition model that generates valid successor states.
- A FIFO queue for the BFS frontier.
- A reached set to avoid repeated exploration.
- Parent-node information to reconstruct the solution path.

When a goal is found, the program displays the sequence of actions and states from the initial state to the goal.

### 2.12 Testing

The water jug solver is tested using Python's `unittest` framework.

The test cases include:

1. Confirming that the initial state is \((0,0,0)\).
2. Confirming that the goal test recognizes states containing exactly one gallon.
3. Verifying that fill actions produce the correct states.
4. Verifying that empty actions produce the correct states.
5. Verifying that pour actions transfer the correct amount of water.
6. Confirming that BFS finds a goal state.
7. Checking that each consecutive pair of states in the solution is connected by a valid action.
8. Confirming that the final state satisfies the goal condition.

These tests help verify that the transition model and search algorithm work as expected.

---

## Conclusion

The Spam Filter Email Agent demonstrates rule-based decision-making by classifying emails using sender domains and spam-word counts. The Water Jug Problem demonstrates state-space search using Breadth-First Search to find a sequence of actions that measures exactly one gallon.

Both programs are implemented in Python and can be tested using automated unit tests. GitHub Actions can be used to run the tests automatically whenever changes are pushed to the repository.