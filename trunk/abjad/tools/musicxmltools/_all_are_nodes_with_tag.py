from xml.etree import ElementTree


def _all_are_nodes_with_tag(nodes, tag):
    assert len(nodes)
    if all([ElementTree.iselement(node) for node in nodes]) and \
        all([node.tag == tag for node in nodes]):
        return True
    return False
