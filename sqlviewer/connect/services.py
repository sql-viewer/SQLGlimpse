from sqlviewer.glimpse.models import Version, Table, ForeignKey

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'


def connect_tables(version: Version, source_table: str, target_table: str, depth: int = 5):
    search_graph = build_search_graph(version)
    results = breadth_first_search(search_graph, source_table, target_table, depth)
    return results


def build_search_graph(version: Version) -> dict:
    search_map = {}
    table_map = dict([(t.id, t.name) for t in Table.objects.filter(model_version=version)])
    foreign_keys = ForeignKey.objects.filter(model_version=version)

    for fk in foreign_keys:
        target_name = table_map[fk.target_table_id]
        source_name = table_map[fk.source_table_id]
        if target_name not in search_map:
            search_map[target_name] = set()
        if source_name not in search_map:
            search_map[source_name] = set()

        search_map[target_name].add(source_name)
        search_map[source_name].add(target_name)

    for key in search_map.keys():
        search_map[key] = list(search_map[key])

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
