from collections import deque
import heapq


class Heap:
    """ Min heap for general objects, a sort criteria must be provided in the key parameter """

    def __init__(self, key):
        self.i = 0
        self.key = key
        self._heap = []

    def __len__(self):
        return len(self._heap)

    def popmin(self):
        return heapq.heappop(self._heap)[-1]

    def append(self, elem):
        self.i += 1  # Ensures that plain objects are not going to be compared when they have the same key
        return heapq.heappush(self._heap, (self.key(elem), self.i, elem))


def depth_first_search(grid):
    s0 = grid.start_pos
    visited = {s0}
    queue = deque([s0])
    while len(queue) != 0:
        u = queue.pop()
        for v in grid.neighbour_cells(u):
            if v in visited:
                continue
            v.parent = u
            if v.is_final:
                grid.mark_traceback(v)  # Grid related
                return v
            queue.append(v)
            visited.add(v)
            grid.mark_visited_cell(v)  # Grid related
        print(f"Queue size: {len(queue)}")


def breadth_first_search(grid):
    s0 = grid.start_pos
    visited = {s0}
    queue = deque([s0])
    while len(queue) != 0:
        u = queue.popleft()
        for v in grid.neighbour_cells(u):
            if v in visited:
                continue
            v.parent = u
            if v.is_final:
                grid.mark_traceback(v)  # Grid related
                return v
            queue.append(v)
            visited.add(v)
            grid.mark_visited_cell(v)  # Grid related
        print(f"Queue size: {len(queue)}")


def iterative_depth_first_search(grid):
    def _depth_first_seach(limit):
        s0 = grid.start_pos
        visited = {s0}
        queue = deque([s0])
        while len(queue) != 0:
            u = queue.pop()
            for v in grid.neighbour_cells(u):
                # Because of the second condition, a node v can enter the queue multiple times,
                # but every time with a shorter path from the start cell
                if v in visited and v.depth <= u.depth + 1:
                    continue
                v.parent = u
                v.depth = u.depth + 1
                if v.depth > limit:
                    continue
                if v.is_final:
                    grid.mark_traceback(v)  # Grid related
                    return v
                queue.append(v)
                visited.add(v)
                grid.mark_visited_cell(v)  # Grid related
            print(f"Queue size: {len(queue)}")

    limit = 1
    while _depth_first_seach(999) is None:
        grid.reset_grid()
        limit += 1


def best_first_search(grid):
    def h(cell):  # Heuristic function
        return grid.distance(cell, grid.end_pos)

    s0 = grid.start_pos
    visited = {s0}
    heap = Heap(key=h)
    heap.append(s0)
    while len(heap) != 0:
        u = heap.popmin()
        for v in grid.neighbour_cells(u):
            if v in visited:
                continue
            v.parent = u
            if v.is_final:
                grid.mark_traceback(v)  # Grid related
                return v
            heap.append(v)
            visited.add(v)
            grid.mark_visited_cell(v)  # Grid related
        print(f"Heap size: {len(heap)}")


def a_star(grid):
    def h(cell):  # Heuristic function
        return grid.distance(cell, grid.end_pos)

    def f(cell):  # Cost + Heuristic function
        return cell.depth + h(cell)

    s0 = grid.start_pos
    visited = {s0}
    heap = Heap(key=lambda c: (f(c), h(c)))
    heap.append(s0)
    while len(heap) != 0:
        u = heap.popmin()
        for v in grid.neighbour_cells(u):
            # Because of the second condition, a node v can enter the heap multiple times,
            # but every time with a shorter path from the start cell
            if v in visited and v.depth <= u.depth + 1:
                continue
            v.parent = u
            v.depth = u.depth + 1
            if v.is_final:
                grid.mark_traceback(v)  # Grid related
                return v
            heap.append(v)
            visited.add(v)
            grid.mark_visited_cell(v)  # Grid related
        print(f"Heap size: {len(heap)}")
