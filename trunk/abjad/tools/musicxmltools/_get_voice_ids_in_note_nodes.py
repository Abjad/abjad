from abjad.tools.musicxmltools._all_are_nodes_with_tag import _all_are_nodes_with_tag
from abjad.tools.musicxmltools._get_voice_id_in_note_node import _get_voice_id_in_note_node


def _get_voice_ids_in_note_nodes(nodes):
    assert _all_are_nodes_with_tag(nodes, 'note')
    ids = []
    for node in nodes:
        id = _get_voice_id_in_note_node(node)
        if id is not None and id not in ids:
            ids.append(id)
    return tuple(ids)
