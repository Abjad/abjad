from abjad.tools.musicxmltools._all_are_nodes_with_tag import _all_are_nodes_with_tag
from abjad.tools.musicxmltools._note_nodes_contain_chords import _note_nodes_contain_chords


def _group_note_nodes_by_chord(nodes):
    assert _all_are_nodes_with_tag(nodes, 'note')
    if not _note_nodes_contain_chords(nodes):
        return [[node] for node in nodes]
    groups = []
    group = [nodes[0]]
    for node in nodes[1:]:
        if node.find('chord') is not None:
            group.append(node)
        else:
            groups.append(group)
            group = [node]
    groups.append(group)
    return groups
