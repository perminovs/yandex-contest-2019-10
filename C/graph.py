def build_minimum_spanning_tree(graph):
    minimum_spanning_tree = set()
    groups = {}

    for v in sorted(graph):
        _, e1, e2 = v
        g1 = groups.get(e1)
        g2 = groups.get(e2)
        if g1 is not None and g2 is not None and g1 == g2:
            # got edges from the same connect group,
            # can't add this vertex, it will make e1 cycle
            continue
        elif g1 is not None and g2 is not None:
            # got edges from different connect groups, need to union it
            for k in groups:
                if groups[k] == g2:
                    groups[k] = g1
        elif g1 is not None and g2 is None:
            # see edge `e2` for the first time, mark it
            groups[e2] = g1
        elif g1 is None and g2 is not None:
            # see edge `e1` for the first time, mark it
            groups[e1] = g2
        else:
            # see both edges for the first time
            groups[e2] = groups[e1] = min(e1, e2)

        minimum_spanning_tree.add(v)

    return minimum_spanning_tree
