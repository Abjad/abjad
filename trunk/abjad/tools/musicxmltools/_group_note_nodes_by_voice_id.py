from abjad.tools.musicxmltools._all_are_nodes_with_tag import _all_are_nodes_with_tag
from abjad.tools.musicxmltools._get_voice_id_in_note_node import _get_voice_id_in_note_node
from abjad.tools.musicxmltools._get_voice_ids_in_note_nodes import _get_voice_ids_in_note_nodes

def _group_note_nodes_by_voice_id(nodes):
    assert _all_are_nodes_with_tag(nodes, 'note')
    ids = _get_voice_ids_in_note_nodes(nodes)
    if not ids:
        return [nodes]
    else:
        groups = []
        for id in ids:
            groups.append(filter(\
                lambda x: _get_voice_id_in_note_node(x) == id, nodes))
        return groups
