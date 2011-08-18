from abjad.tools.componenttools._ContainmentSignature import _ContainmentSignature


def component_to_parentage_signature(component):
    '''.. versionadded:: 1.1

    Change `component` to parentage signature::

        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        abjad> staff = Staff([tuplet])
        abjad> note = staff.leaves[0]
        abjad> print componenttools.component_to_parentage_signature(note)
                root: Staff-... (...)
                score:
        staffgroup:
                staff: Staff-...
                voice:
                self: Note-...

    Return parentage signature.
    '''
    from abjad.tools.scoretools.Score import Score
    from abjad.tools.stafftools.Staff import Staff
    from abjad.tools.voicetools.Voice import Voice
    from abjad.tools import componenttools
    from abjad.tools.scoretools import StaffGroup

    signature = _ContainmentSignature()
    signature._self = component._ID
    for component in componenttools.get_improper_parentage_of_component(component):
        if isinstance(component, Voice) and not signature._voice:
            signature._voice = component._ID
        elif isinstance(component, Staff) and not signature._staff:
            signature._staff = component._ID
        elif isinstance(component, StaffGroup) and not signature._staffgroup:
            signature._staffgroup = component._ID
        elif isinstance(component, Score) and not signature._score:
            signature._score = component._ID
    else:
        '''Root components must be manifestly equal to compare True.'''
        signature._root = id(component)
        signature._root_str = component._ID
    return signature
