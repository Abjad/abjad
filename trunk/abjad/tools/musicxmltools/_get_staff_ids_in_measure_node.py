from abjad.tools.musicxmltools._all_are_nodes_with_tag import _all_are_nodes_with_tag
from abjad.tools.musicxmltools._get_staff_id_in_note_node import _get_staff_id_in_note_node


def _get_staff_ids_in_measure_node(node):
    assert _all_are_nodes_with_tag([node], 'measure')
    ids = []
    for note_node in node.findall('note'):
        id = _get_staff_id_in_note_node(note_node)
        if id is not None and id not in ids:
            ids.append(id)
    return tuple(ids)
