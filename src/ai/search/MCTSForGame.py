import math
import random

class MCTSNode:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []
        self.visits = 0
        self.value = 0
        
    def expand(self):
        # Expand the node by adding child nodes for all possible actions
        #Vienen dadas por la heuristica del personaje
        possible_actions = self.state.get_possible_actions()

        for action in possible_actions:
            new_state = self.state.perform_action(action)
            new_node = MCTSNode(new_state)
            new_node.parent = self
            self.children.append(new_node)

    def select_child(self):
        # Select a child node using the UCB1 formula
        exploration_constant = 1.4
        best_child = None
        best_score = -math.inf
        for child in self.children:
            score = child.value / (child.visits + 1) + exploration_constant * math.sqrt(math.log(self.visits + 1) / (child.visits + 1))
            if score > best_score:
                best_child = child
                best_score = score
        return best_child

    def backpropagate(self, value):
        # Update the value and visit count of the node and its ancestors
        self.visits += 1
        self.value += value
        if self.parent is not None:
            self.parent.backpropagate(value)

class MCTS:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def select_action(self, state):
        root = MCTSNode(state)
        for _ in range(self.iterations):
            node = root
            # Select
            while not node.state.is_terminal() and node.children:
                node = node.select_child()
            # Expand
            if not node.state.is_terminal():
                node.expand()
                node = random.choice(node.children)
            # Simulate
            simulated_value = self.simulate(node.state)
            # Backpropagate
            node.backpropagate(simulated_value)
        # Select the best action based on the most visited child
        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.state.last_action

    def simulate(self, state):
        # Simulate a random game from the current state and return the result
        while not state.is_terminal():
            action = random.choice(state.get_possible_actions())
            state = state.perform_action(action)
        return state.get_result()

