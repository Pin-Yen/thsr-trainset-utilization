
class Graph(object):
    """docstring for Graph"""
    def __init__(self, matrix, s, t):
        self.matrix = matrix
        self.s = s
        self.t = t
        self.size = len(matrix[0])

    def link(self, u, v):
        self.matrix[u][v] = 1


def dfs(graph, current_node, parent_list, parent_set):
    if current_node == graph.t:
        return True

    for next_node in range(graph.size):
        if graph.matrix[current_node][next_node] > 0 and next_node not in parent_set:
            parent_list.append(next_node)
            parent_set.add(next_node)

            if dfs(graph, next_node, parent_list, parent_set):
                return True
            else:
                popped = parent_list.pop()
                # parent_set.remove(popped)

    return False

def ford_fulkerson(graph):
    # returns maximum flow of graph
    # Note: graph flow is modified to residual graph.

    parent_list = [graph.s]
    parent_set = {graph.s}
    flow = 0
    while dfs(graph, graph.s, parent_list, parent_set):
        augmented_flow = float('inf')
        for a, b in zip(parent_list[:-1], parent_list[1:]):
            augmented_flow = min(graph.matrix[a][b], augmented_flow)

        flow += augmented_flow

        # update residual graph
        for a, b in zip(parent_list[:-1], parent_list[1:]):
            graph.matrix[a][b] -= augmented_flow
            graph.matrix[b][a] += augmented_flow

        parent_list = [graph.s]
        parent_set = {graph.s}

    return flow


def main():
    #    s, a, b, c, y, z, a, b, c, y, z, t
    matrix = [
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], #s
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], #a
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], #b
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], #c
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #y
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #z
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #a
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #b
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #c
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #y
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #z
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #t
    ]

    graph = Graph(matrix, 0, len(matrix[0]) - 1)
    flow = ford_fulkerson(graph)
    print("Max flow:", flow)


if __name__ == '__main__':
    main()