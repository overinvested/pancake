from collections import deque
from heapq import heappush, heappop
import cProfile
import re


goal = [1,2,3,4,5,6,7,8,9,10]
stack_0 = [1,3,5,2,4,6]
stack_1 = [8,2,1,7,5,4,6,3,9,10]
stack_2 = [9,5,2,8,4,1,10,6,7,3]
stack_3 = [2,8,10,5,7,3,4,6,1,9]
stack_4 = [3,6,8,10,7,1,5,4,2,9]
stack_5 = [6,9,4,8,1,3,2,7,10,5]
stack_6 = [8,5,10,6,2,9,3,4,1,7]
stack_7 = [8,1,10,5,3,7,4,9,2,6]
starting_depth = 1

def main():
    path = a_star(stack_7, non_adjacent_pairs)
    # path = bfs(stack_7, non_adjacent_pairs)
    # print_path(stack_0, iterative_deepening_wrapper(stack_0))
    print_path(stack_7, path[0])
    print('Max queue size: %s' % path[1]) # only for bfs and a*
    

def possible_actions(stack: list) -> list:
    """
    possible_actions
    @param {list} stack: the current stack of pancakes
    @return {list} out: a list representation of the possible actions in a given state
    Does not include flipping only the first pancake as that would accomplish nothing
    """
    out = ['flip:%s' % (i+1) for i in range(1, len(stack))]
    return out


def result(stack: list, action: int) -> list:
    """
    result
    @param {list} stack: the current stack of pancakes
    @param {int} action: the number of pancakes we want to flip
    @return {list} result_stack: a list representation of a single stack of pancakes after a flip of some integer number of pancakes
    """
    to_flip = stack[0:action]
    result_stack = to_flip[::-1] + stack[action:]
    return result_stack


def expand(stack: list) -> list:
    """
    expand
    @param {list} stack: the current stack of pancakes
    @return {list} out: a list representation of all possible stacks of pancakes after one flip
    """
    out = [result(stack, i+1) for i in range(1, len(stack))]
    return out


def iterative_deepening_wrapper(stack: list) -> str:
    """
    iterative_deepening_wrapper
    @param {list} stack: the current stack of pancakes
    @return {str} out: a string representation of actions taken to get to an optimal goal
    Wrapper function for the iterative deepening search
    Specifies and increments the depth limit
    """
    found = 0
    depth_limit = starting_depth
    while(not found):
        out = iterative_deepening(stack, depth_limit, '')
        if out:
            found = 1
            return out
        else:
            depth_limit += 1


def iterative_deepening(stack: list, depth_limit: int, action: str) -> str:
    """
    iterative_deepening
    @param {list} stack: the current stack of pancakes
    @param {int} depth_limit: the current depth limit for IDS
    @param {str} action: string representation of the action(s) taken to reach the current state
    @return {str} out: a string representation of actions taken to get to an optimal goal
    Recursive implementation of iterative deepening search
    """
    if stack == goal[:len(stack)]:
        return action
    if depth_limit == 0:
        return 0

    expansion = expand(stack)

    for i, child in enumerate(expansion):
        actions = possible_actions(child)
        out = iterative_deepening(child, depth_limit-1, (action + ' ' + actions[i]) if action else (action + actions[i]))
        if out:
            return out


def bfs(stack: list) -> str:
    """
    bfs
    @param {list} stack: the initial stack of pancakes
    @return {str} item[1]: a string representation of actions taken to get to an optimal goal
    Implementation of breadth-frist search using a simple FIFO queue
    """
    queue = deque()
    visited = {}
    max_size = 0
    queue.append([stack, ''])
    key = ''
    key = key.join(str(x) for x in stack)
    visited.update({key: ''})

    while queue:
        current_size = len(queue) + len(visited)
        if (current_size > max_size):
            max_size = current_size
        item = list(queue.popleft())
        if item[0] == goal[:len(stack)]:
            return item[1], max_size
        expansion = expand(item[0])
        actions = possible_actions(item[0])
        for i, child in enumerate(expansion):
            key = ''
            key = key.join(map(str,child))
            try:
                visited[key]
            except:
                queue.append([child, item[1] + ' ' + actions[i] if item[1] else item[1] + actions[i]])
                visited.update({key:'exists'})


def a_star(stack: list, heuristic) -> str:
    """
    a_star
    @param {list} stack: the initial stack of pancakes
    @param {function} heuristic: the heuristic function with which we estimate distance from the goal
    @return {str} item[1][1]: a string representation of actions taken to get to an optimal goal
    Implementation of a* search using a priority queue developed with python native heapq functions
    """
    queue = []
    heappush(queue, [[heuristic(stack),0], [stack, '']])
    state_key = 0
    max_length = 0

    while queue:
        current_length = len(queue)
        if (current_length > max_length):
            max_length = current_length
        item = heappop(queue)
        if item[1][0] == goal[:len(stack)]:
            return item[1][1], max_length
        expansion = expand(item[1][0])
        actions = possible_actions(item[1][0])
        for i, child in enumerate(expansion):
            state_key+=1
            heappush(queue, [[heuristic(child) + item[1][1].count(':') + 1, state_key], [child, item[1][1] + ' ' + actions[i]] if item[1][1] else [child, item[1][1] + actions[i]]])


def uniform_cost(stack: list) -> int:
    """
    uniform_cost
    @param {list} stack: the current stack of pancakes (redundant)
    Always returns 0
    """
    return 0


def non_adjacent_pairs(stack: list) -> int:
    """
    non_adjacent_pairs
    @param {list} stack: the current stack of pancakes
    @return {int} out: the number of non-adjacent pairs
    Calculates the number of non-adjacent pairs in a list
    """
    out = 0
 
    for i in range(0,len(stack)):
        if i == 0: continue
        if abs(stack[i]-stack[i-1]) != 1:
            out += 1
    return out


def print_path(stack: list, flip_sequence: str) -> None:
    """
    print_path
    @param {list} stack: the initial stack of pancakes
    @param {str} flip_sequence: the sequence of flips that reaches the goal
    Prints the stacks on the path to the goal stack
    """
    flips = [int(x) for x in re.findall(r'\d+', flip_sequence)]
    out = stack
    print(flip_sequence)
    print(out)
    for flip in flips:
        out = result(out, flip)
        print(out)
    print('Path Cost: %d' % len(flips))


if __name__ == "__main__":
    cProfile.run('main()')