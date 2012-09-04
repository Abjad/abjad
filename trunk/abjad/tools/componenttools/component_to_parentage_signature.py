# TODO: where is this being used? same as containment signature?
def component_to_parentage_signature(component):
    '''.. versionadded:: 1.1

    Change `component` to parentage signature::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> staff = Staff([tuplet])
        >>> note = staff.leaves[0]
        >>> print componenttools.component_to_parentage_signature(note)
            staff: Staff-...
            self: Note-...

    Return parentage signature.
    '''
    from abjad.tools import componenttools
    from abjad.tools import scoretools
    from abjad.tools import stafftools
    from abjad.tools import voicetools

    signature = componenttools.ContainmentSignature()
    signature._self = component._id_string
    for component in componenttools.get_improper_parentage_of_component(component):
        if isinstance(component, voicetools.Voice) and not signature._voice:
            signature._voice = component._id_string
        elif isinstance(component, stafftools.Staff) and not signature._staff:
            signature._staff = component._id_string
        elif isinstance(component, scoretools.StaffGroup) and not signature._staff_group:
            signature._staff_group = component._id_string
        elif isinstance(component, scoretools.Score) and not signature._score:
            signature._score = component._id_string
    else:
        '''Root components must be manifestly equal to compare True.'''
        signature._root = id(component)
        signature._root_str = component._id_string
    return signature
