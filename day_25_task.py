# https://adventofcode.com/2023/day/25
import itertools


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class SnowMachine:
    def __init__(self):
        self.adj_lst = {}
        self.set_of_nodes = set()
        self.capacity_graph = {}

    def convert_to_capacity_graph(self):
        for node, neighbors in self.adj_lst.items():
            for neighbor in neighbors:
                self.capacity_graph[(node, neighbor)] = 1
                self.capacity_graph[(neighbor, node)] = 1

    def convert_to_dot(self, adj_lst):
        dot_string = "graph G {\n"
        for node, edges in adj_lst.items():
            for edge in edges:
                dot_string += f'    "{node}" -- "{edge}";\n'
        dot_string += "}"
        return dot_string

    def ford_fulkerson(self, graph, source, sink):
        max_flow = 0
        residual_graph = graph.copy()

        def find_augmenting_path(residual_graph, start, end):
            visited = set()
            stack = [(start, [start], float("inf"))]

            while stack:
                current, path, path_flow = stack.pop()

                if current == end:
                    return path, path_flow

                for (u, v), capacity in residual_graph.items():
                    if capacity > 0 and u == current and v not in visited:
                        visited.add(v)
                        min_cap = min(path_flow, capacity)
                        stack.append((v, path + [v], min_cap))

            return None, 0

        while True:
            path, path_flow = find_augmenting_path(residual_graph, source, sink)

            if not path:
                break

            for u, v in zip(path, path[1:]):
                residual_graph[(u, v)] -= path_flow
                residual_graph[(v, u)] += path_flow

            max_flow += path_flow

        return max_flow

    def get_sum_of_two_disconnected_group(self, file_name):
        for line in FileReader().gen_file_reader(file_name):
            key_node, connected_nodes_str = line.split(": ")
            connected_nodes_lst = [i for i in connected_nodes_str.split()]
            if key_node not in self.adj_lst:
                self.adj_lst[key_node] = connected_nodes_lst
                self.set_of_nodes.add(key_node)
            else:
                for node in connected_nodes_lst:
                    self.adj_lst[key_node].append(node)

            for node in connected_nodes_lst:
                if node not in self.adj_lst:
                    self.adj_lst[node] = [key_node]
                    self.set_of_nodes.add(node)
                else:
                    self.adj_lst[node].append(key_node)

        dot_config = self.convert_to_dot(self.adj_lst)
        with open("mygraph.dot", "w") as writer:
            writer.write(dot_config)

        self.convert_to_capacity_graph()
        node_lst = list(self.set_of_nodes)
        node_pairs = list(itertools.combinations(self.set_of_nodes, 2))

        sum = 0
        for i in range(1, len(node_lst)):
            max_flow_nodes = self.ford_fulkerson(self.capacity_graph, node_lst[0], node_lst[i])
            if max_flow_nodes == 3:
                sum += 1

        return sum * (len(self.set_of_nodes) - sum)


if __name__ == "__main__":
    print("Day 25")
    show_machine_instance = SnowMachine()
    ans_part_1 = show_machine_instance.get_sum_of_two_disconnected_group("day_25.txt")
    print("Task 1 is = ", ans_part_1)
