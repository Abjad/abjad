from abjad.tools.musicxmltools._all_are_nodes_with_tag import _all_are_nodes_with_tag


def _note_nodes_contain_rests(nodes):
    assert _all_are_nodes_with_tag(nodes, 'note')
    if filter(lambda x: x.find('rest') is not None, nodes):
        return True
    return False
