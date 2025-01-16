using DataStructures
using Combinatorics


max_flips = [0,1,3,4,5,7,8,9,10,11,13,14,15,16,17,18,19,20,22]

stack_0 = [1,3,5,2,4,6]
stack_1 = [8,2,1,7,5,4,6,3,9,10]
stack_2 = [9,5,2,8,4,1,10,6,7,3]
stack_3 = [2,8,10,5,7,3,4,6,1,9]
stack_4 = [3,6,8,10,7,1,5,4,2,9]
stack_5 = [6,9,4,8,1,3,2,7,10,5]
stack_6 = [8,5,10,6,2,9,3,4,1,7]
stack_7 = [8,1,10,5,3,7,4,9,2,6]
starting_depth = 1


stacks_req_max = Dict{Vector{Int}, String}()


function is_goal(stack::Vector)
    return stack == [i for i ∈ 1:length(stack)]
end


function possible_actions(stack::Vector)
    return ["flip:$(i)" for i ∈ 2:length(stack)]
end


function result(stack::Vector, action::Int)
    to_flip = stack[begin:action]
    result_stack = [reverse(to_flip) ; stack[(action+1):end]]
    return result_stack 
end


function expand(stack::Vector)
    return [result(stack, action) for action ∈ 2:length(stack)]
end


function iterative_deepening_wrapper(stack::Vector)
    found = false
    depth_limit = 1
    while !found
        path = iterative_deepening_search(stack, depth_limit, "")
        if path !== nothing
            found = true
            return path
        end
        depth_limit += 1
    end
end


function iterative_deepening_search(stack::Vector, depth_limit::Int, action::String)
    if is_goal(stack)
        return action
    end
    if depth_limit == 0
        return nothing
    end

    expansion = expand(stack)

    for (i,child) ∈ enumerate(expansion)
        actions = possible_actions(stack)
        if action != ""
            action_str = "$(action) $(actions[i])"
        else
            action_str = actions[i]
        end
        out = iterative_deepening_search(child, depth_limit-1, action_str)
        if out !== nothing    
            return out
        end
    end
end


function bfs(stack::Vector)
    queue = Queue{Any}()
    enqueue!(queue, (stack, ""))

    while !isempty(queue)
        item = dequeue!(queue)
        if is_goal(item[1])
            return item[2]
        end
        expansion = expand(item[1])
        actions = possible_actions(item[1])
        for (i,child) ∈ enumerate(expansion)
            if item[2] != ""
                action_str = "$(item[2]) $(actions[i])"
            else
                action_str = actions[i]
            end
            enqueue!(queue, (child, action_str))
        end
    end
end


function α(stack::Vector, γ::Function)
    pq = PriorityQueue()
    enqueue!(pq, [stack,""], [γ(stack),0])
    state_key = 0

    while !isempty(pq)
        item = dequeue!(pq)
        if is_goal(item[1])
            return item[2]
        end
        expansion = expand(item[1])
        actions = possible_actions(item[1])
        for (i,child) ∈ enumerate(expansion)
            state_key += 1
            if item[2] != ""
                action_str = "$(item[2]) $(actions[i])"
            else
                action_str = actions[i]
            end
            enqueue!(pq, [child, action_str], [γ(child) + δ(item[2]) + 1, state_key])
        end
    end
end


function δ(path::String)
    return count(==(':'), path)
end


function uniform_cost(stack::Vector)
    return 0
end


function non_adjacent_pairs(stack::Vector)
    pairs = 0
    for i ∈ 1:length(stack)
        if i == 1
            continue
        end
        if abs(stack[i] - stack[i-1]) != 1
            pairs += 1
        end
    end
    return pairs
end


function print_path(stack::Vector, path::String)
    regex = r"\d+"
    flips = parse.(Int,[match.match for match ∈ eachmatch(regex, path)])
    out = stack
    println(path)
    println(out)
    for flip ∈ flips
        out = result(out, flip)
        println(out)
    end
    println("Path Cost: $(length(flips))")
end


function test()
    path = α(stack_0, non_adjacent_pairs)
    print_path(stack_0, path)
    path = α(stack_1, non_adjacent_pairs)
    print_path(stack_1, path)
    path = α(stack_2, non_adjacent_pairs)
    print_path(stack_2, path)
    path = α(stack_3, non_adjacent_pairs)
    print_path(stack_3, path)
    path = α(stack_4, non_adjacent_pairs)
    print_path(stack_4, path)
    path = α(stack_5, non_adjacent_pairs)
    print_path(stack_5, path)
    path = α(stack_6, non_adjacent_pairs)
    print_path(stack_6, path)
    path = α(stack_7, non_adjacent_pairs)
    print_path(stack_7, path)
end


function find_maxes(len::Int)
    default = [i for i ∈ 1:len]
    perms = permutations(default)

    max = 0
    for p ∈ perms
        path = α(p, non_adjacent_pairs)
        cost = δ(path)
        if cost > max
            max = cost
            empty!(stacks_req_max)
        end
        if cost == max
            stacks_req_max[p] = path
        end
    end
    ps = pairs(stacks_req_max)
    for (k,v) in ps
        println("$(k):$(v)")
    end
    println("Total: $(length(stacks_req_max))")
    empty!(stacks_req_max)
end
