__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


def build_search_map(data: dict) -> dict:
    search_map = {}

    return search_map


def breadth_first_search(graph, start, goal, depth=5, excluded_tables=None):
    # These are mostly not connecting tables, or have low relevance for connecting
    excluded_tables = excluded_tables or [
        "CMN_Units",
        "DOC_Documents"
    ]

    return list(bread_first_search_path(graph, start, goal, depth, excluded_tables))


def bread_first_search_path(graph, start, goal, max_depth, excluded=None):
    """
    Breadth first search with a maximum depth and excluded connecting tables.

    :param excluded: list of excluded tables
    :type excluded: dict
    :param graph: graph which is analyzed
    :type graph: dict
    :param start: start nsode (Table Name)
    :param goal: goal node (Table Name)
    :param max_depth: maximum depth to search for
    :return: list of connections
    """
    if not excluded:
        excluded = []

    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        if len(path) >= max_depth:
            return

        for next in set(graph[vertex]) - set(path):
            if next == goal:
                yield path + [next]
            elif next in excluded:
                continue
            else:
                queue.append((next, path + [next]))
