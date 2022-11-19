# Pancake

This project performs pancake sort on a chosen subset of stacks of size <= 10.

## AI Search

There are 3 different searches implemented in this project. IDS, BFS, and A\*.

In general, the steps to move from one state to the next are as follows:

1. Find all possible actions in the current state. Flipping only the first pancake is not allowed as it achieves nothing.
2. Expand the current state to add all possible resulting states to the search space.
3. Move to the next selected state as determined by the search type.

### A\*

A\* search is a heuristic based search that determines the next state as the one which minimized the following function.

$$ f(x) = h(x)+g(x) $$

$h(x)$ is the chosen heuristic for the given problem. In our case, we use either 0 for uniform cost, or the number of non-adjacent pairs of pancakes in the stack.

$g(x)$ is the number of nodes needed to reach the state, or the path cost.
