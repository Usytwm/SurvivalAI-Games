import random
from typing import List, Tuple, Dict
from collections import OrderedDict
from math import sqrt, log
from functools import reduce
from operator import mul

class NaiveMCTSNode:
    E_GREEDY = 0
    UCB1 = 1
    DEBUG = 0
    C = 0.05  # exploration constant for UCB1

    def __init__(self, maxplayer: int, minplayer: int, gs: GameState, parent: 'NaiveMCTSNode', evaluation_bound: float, a_creation_ID: int, fensa: bool) -> None:
        self.parent = parent
        self.gs = gs
        self.depth = 0 if parent is None else parent.depth + 1
        self.evaluation_bound = evaluation_bound
        self.creation_ID = a_creation_ID
        self.forceExplorationOfNonSampledActions = fensa
        self.childrenMap: Dict[int, NaiveMCTSNode] = OrderedDict()  # associates action codes with children
        self.unitActionTable: List[UnitActionTableEntry] = []
        self.multipliers: List[int] = []

        while gs.winner() == -1 and not gs.gameover() and not gs.canExecuteAnyAction(maxplayer) and not gs.canExecuteAnyAction(minplayer):
            gs.cycle()

        if gs.winner() != -1 or gs.gameover():
            self.type = -1
        elif gs.canExecuteAnyAction(maxplayer):
            self.type = 0
            self.moveGenerator = PlayerActionGenerator(gs, maxplayer)
            self.actions = []
            self.children = []
            self.initialize_unit_action_table(self.moveGenerator)
        elif gs.canExecuteAnyAction(minplayer):
            self.type = 1
            self.moveGenerator = PlayerActionGenerator(gs, minplayer)
            self.actions = []
            self.children = []
            self.initialize_unit_action_table(self.moveGenerator)
        else:
            self.type = -1
            print("NaiveMCTSNode: This should not have happened...")

    def initialize_unit_action_table(self, moveGenerator):
        self.unitActionTable = []
        self.multipliers = []
        baseMultiplier = 1
        for choice in moveGenerator.getChoices():
            ae = UnitActionTableEntry()
            ae.u, actions = choice
            ae.nactions = len(actions)
            ae.actions = actions
            ae.accum_evaluation = [0] * ae.nactions
            ae.visit_count = [0] * ae.nactions
            self.unitActionTable.append(ae)
            self.multipliers.append(baseMultiplier)
            baseMultiplier *= ae.nactions

    def select_leaf(self, maxplayer: int, minplayer: int, epsilon_l: float, epsilon_g: float, epsilon_0: float, global_strategy: int, max_depth: int, a_creation_ID: int) -> 'NaiveMCTSNode':
        if self.unitActionTable is None:
            return self
        if self.depth >= max_depth:
            return self

        if self.children and random.random() >= epsilon_0:
            selected = None
            if global_strategy == NaiveMCTSNode.E_GREEDY:
                selected = self.select_from_already_sampled_epsilon_greedy(epsilon_g)
            elif global_strategy == NaiveMCTSNode.UCB1:
                selected = self.select_from_already_sampled_ucb1(NaiveMCTSNode.C)
            return selected.select_leaf(maxplayer, minplayer, epsilon_l, epsilon_g, epsilon_0, global_strategy, max_depth, a_creation_ID)
        else:
            return self.select_leaf_using_local_mabs(maxplayer, minplayer, epsilon_l, epsilon_g, epsilon_0, global_strategy, max_depth, a_creation_ID)

    def select_from_already_sampled_epsilon_greedy(self, epsilon_g: float) -> 'NaiveMCTSNode':
        if random.random() >= epsilon_g:
            best = None
            for pate in self.children:
                if self.type == 0:  # max node
                    if best is None or pate.average_evaluation() > best.average_evaluation():
                        best = pate
                else:  # min node
                    if best is None or pate.average_evaluation() < best.average_evaluation():
                        best = pate
            return best
        else:
            return random.choice(self.children)

    def select_from_already_sampled_ucb1(self, C: float) -> 'NaiveMCTSNode':
        best = None
        best_score = 0
        for pate in self.children:
            exploitation = pate.average_evaluation()
            exploration = sqrt(log(self.visit_count) / pate.visit_count)
            if self.type == 0:  # max node
                exploitation = (self.evaluation_bound + exploitation) / (2 * self.evaluation_bound)
            else:  # min node
                exploitation = (self.evaluation_bound - exploitation) / (2 * self.evaluation_bound)
            tmp = C * exploitation + exploration
            if best is None or tmp > best_score:
                best = pate
                best_score = tmp
        return best

    def select_leaf_using_local_mabs(self, maxplayer: int, minplayer: int, epsilon_l: float, epsilon_g: float, epsilon_0: float, global_strategy: int, max_depth: int, a_creation_ID: int) -> 'NaiveMCTSNode':
        distributions = []
        not_sampled_yet = list(range(len(self.unitActionTable)))

        for ate in self.unitActionTable:
            dist = [epsilon_l / ate.nactions] * ate.nactions
            best_idx = -1
            best_evaluation = 0
            visits = 0
            for i in range(ate.nactions):
                if self.type == 0:  # max node
                    if best_idx == -1 or (visits != 0 and ate.visit_count[i] == 0) or (visits != 0 and (ate.accum_evaluation[i] / ate.visit_count[i]) > best_evaluation):
                        best_idx = i
                        if ate.visit_count[i] > 0:
                            best_evaluation = ate.accum_evaluation[i] / ate.visit_count[i]
                        else:
                            best_evaluation = 0
                        visits = ate.visit_count[i]
                else:  # min node
                    if best_idx == -1 or (visits != 0 and ate.visit_count[i] == 0) or (visits != 0 and (ate.accum_evaluation[i] / ate.visit_count[i]) < best_evaluation):
                        best_idx = i
                        if ate.visit_count[i] > 0:
                            best_evaluation = ate.accum_evaluation[i] / ate.visit_count[i]
                        else:
                            best_evaluation = 0
                        visits = ate.visit_count[i]
                dist[i] = epsilon_l / ate.nactions
            if ate.visit_count[best_idx] != 0:
                dist[best_idx] = (1 - epsilon_l) + (epsilon_l / ate.nactions)
            else:
                if self.forceExplorationOfNonSampledActions:
                    for j in range(len(dist)):
                        if ate.visit_count[j] > 0:
                            dist[j] = 0
            not_sampled_yet.append(len(distributions))
            distributions.append(dist)

        base_ru = ResourceUsage()
        for u in self.gs.getUnits():
            ua = self.gs.getUnitAction(u)
            if ua:
                ru = ua.resourceUsage(u, self.gs.getPhysicalGameState())
                base_ru.merge(ru)

        pa2 = PlayerAction()
        action_code = 0
        pa2.setResourceUsage(base_ru.clone())
        while not_sampled_yet:
            i = random.choice(not_sampled_yet)
            try:
                ate = self.unitActionTable[i]
                distribution = distributions[i]
                code = random.choices(range(len(distribution)), weights=distribution)[0]
                ua = ate.actions[code]
                r2 = ua.resourceUsage(ate.u, self.gs.getPhysicalGameState())
                if not pa2.getResourceUsage().consistentWith(r2, self.gs):
                    dist_l = [distribution[j] for j in range(len(distribution))]
                    dist_outputs = list(range(len(distribution)))
                    while code in dist_outputs:
                        idx = dist_outputs.index(code)
                        del dist_l[idx]
                        del dist_outputs[idx]
                        code = random.choices(dist_outputs, weights=dist_l)[0]
                        ua = ate.actions[code]
                        r2 = ua.resourceUsage(ate.u, self.gs.getPhysicalGameState())
                if not self.gs.getUnit(ate.u.getID()):
                    raise ValueError("Issuing an action to an inexisting unit!!!")
                pa2.getResourceUsage().merge(r2)
                pa2.addUnitAction(ate.u, ua)
                action_code += code * self.multipliers[i]
            except Exception as e:
                print(e)
        pate = self.childrenMap.get(action_code)
        if not pate:
            self.actions.append(pa2)
            gs2 = self.gs.cloneIssue(pa2)
            node = NaiveMCTSNode(maxplayer, minplayer, gs2.clone(), self, self.evaluation_bound, a_creation_ID, self.forceExplorationOfNonSampledActions)
            self.childrenMap[action_code] = node
            self.children.append(node)
            return node
        return pate.select_leaf(maxplayer, minplayer, epsilon_l, epsilon_g, epsilon_0, global_strategy, max_depth, a_creation_ID)

    def getActionTableEntry(self, u):
        for e in self.unitActionTable:
            if e.u == u:
                return e
        raise ValueError("Could not find Action Table Entry!")

    def propagateEvaluation(self, evaluation, child):
        self.accum_evaluation += evaluation
        self.visit_count += 1
        if child:
            idx = self.children.index(child)
            pa = self.actions[idx]
            for ua in pa.getActions():
                actionTable = self.getActionTableEntry(ua[0])
                idx = actionTable.actions.index(ua[1])
                actionTable.accum_evaluation[idx] += evaluation
                actionTable.visit_count[idx] += 1
        if self.parent:
            self.parent.propagateEvaluation(evaluation, self)

    def printUnitActionTable(self):
        for uat in self.unitActionTable:
            print("Actions for unit", uat.u)
            for i in range(uat.nactions):
                print("  ", uat.actions[i], "visited", uat.visit_count[i], "with average evaluation", (uat.accum_evaluation[i] / uat.visit_count[i]))


class PlayerAction:
    def __init__(self):
        self.actions = []
        self.resourceUsage = None

    def setResourceUsage(self, resourceUsage):
        self.resourceUsage = resourceUsage

    def getResourceUsage(self):
        return self.resourceUsage

    def addUnitAction(self, unit, action):
        self.actions.append((unit, action))

    def getActions(self):
        return self.actions


class ResourceUsage:
    def __init__(self):
        self.resources = {}

    def merge(self, other):
        for key, value in other.resources.items():
            if key in self.resources:
                self.resources[key] += value
            else:
                self.resources[key] = value

    def clone(self):
        new_ru = ResourceUsage()
        new_ru.resources = self.resources.copy()
        return new_ru

    def consistentWith(self, other, gs):
        for key, value in other.resources.items():
            if key in self.resources:
                if self.resources[key] + value > gs.getResourceMax(key):
                    return False
            else:
                if value > gs.getResourceMax(key):
                    return False
        return True


class UnitActionTableEntry:
    def __init__(self):
        self.u = None
        self.nactions = 0
        self.actions = []
        self.accum_evaluation = []
        self.visit_count = []

    def average_evaluation(self):
        return sum(self.accum_evaluation) / max(sum(self.visit_count), 1)

class GameState:
    def __init__(self):
        pass

class PlayerActionGenerator:
    def __init__(self, gs, player):
        pass