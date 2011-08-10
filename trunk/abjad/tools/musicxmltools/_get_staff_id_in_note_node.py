from abjad.tools.musicxmltools._all_are_nodes_with_tag import _all_are_nodes_with_tag


def _get_staff_id_in_note_node(node):
    assert _all_are_nodes_with_tag([node], 'note')
    if node.find('staff') is not None:
        return int(node.find('staff').text)
    return None
