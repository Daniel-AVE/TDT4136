from Map import Map_Obj


class Node:
    def __init__(self, pos, parent, map_obj):
        self.pos = pos
        self.parent = parent

        # Calculate the cost, heuristic, and total upon initialization
        self.heuristic(map_obj.get_goal_pos())
        self.calculate_cost(map_obj)

    def calculate_cost(self, map_obj):
        """Calculates the node's cost and its total (cost + heuristic)."""
        if self.parent:
            self.cost = map_obj.get_cell_value(self.pos) + self.parent.cost
        else:
            self.cost = map_obj.get_cell_value(self.pos)
        self.total = self.cost + self.heur

    def heuristic(self, goal):
        """Calculates the Manhattan distance from this node to the goal."""
        self.heur = abs(self.pos[0] - goal[0]) + abs(self.pos[1] - goal[1])


class Astar:
    def __init__(self, map_obj):
        self.map_obj = map_obj
        self.openList = []
        self.closedList = []

    def find_successors(self, parent_node):
        """Finds and processes the successors of the given node."""
        successors = self.get_adjacent_positions(parent_node.pos)
        for succ_pos in successors:
            if self.map_obj.get_cell_value(succ_pos) > 0:
                curr_node = Node(succ_pos, parent_node, self.map_obj)
                self.append_and_check_for_equal(curr_node)

        # Move node to closed list after processing
        self.closedList.append(parent_node)
        self.openList.remove(parent_node)

    @staticmethod
    def get_adjacent_positions(pos):
        """Returns positions adjacent to the given position."""
        x, y = pos
        return [[x + 1, y], [x, y + 1], [x - 1, y], [x, y - 1]]

    def sort_openList(self):
        """Sorts openList based on the total (cost + heuristic) value."""
        self.openList.sort(key=lambda x: x.total)

    def append_and_check_for_equal(self, current_node):
        """Add a node to openList. If node with same position exists, compare costs."""
        for node in self.openList:
            if current_node.pos == node.pos:
                if current_node.total < node.total:
                    self.openList.remove(node)
                    self.openList.append(current_node)
                return
        self.openList.append(current_node)

    def recover_path(self, current_node):
        """Tracks the path from the current node back to the start."""
        path = [current_node.pos]
        while current_node.pos != self.map_obj.get_start_pos():
            current_node = current_node.parent
            path.append(current_node.pos)
        return path


if __name__ == "__main__":
    # Get task input and initialize map and algorithm
    inputTask = int(input('Choose a task from 1 - 4: '))
    map_obj = Map_Obj(task=inputTask)

    aStar = Astar(map_obj)
    aStar.current = Node(map_obj.get_start_pos(), None, map_obj)
    aStar.openList.append(aStar.current)

    # Process nodes until goal is found
    while aStar.current.pos != map_obj.get_goal_pos():
        aStar.find_successors(aStar.current)
        aStar.sort_openList()
        aStar.current = aStar.openList[0]

    # Mark the path on the map
    path = aStar.recover_path(aStar.current)
    for position in path:
        map_obj.replace_map_values(position, 5, map_obj.get_goal_pos())

    map_obj.show_map()
