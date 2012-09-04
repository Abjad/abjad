def component_to_containment_signature(component):
    '''.. versionadded:: 1.1

    Change `component` to containment signature::

        >>> score = Score(
        ... r"""\context Staff = "CustomStaff" { """
        ...     r"""\context Voice = "CustomVoice" { c' d' e' f' } }""")
        >>> score.name = 'CustomScore'

    ::

        >>> f(score)
        \context Score = "CustomScore" <<
            \context Staff = "CustomStaff" {
                \context Voice = "CustomVoice" {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }
        >>

    ::

        >>> componenttools.component_to_containment_signature(score.leaves[0])
        ContainmentSignature(Note-..., Voice-'CustomVoice', Staff-..., Score-'CustomScore')

    Containment signature gives first voice, staff, staff group and score in parentage.

    .. versionchanged:: 2.9
        renamed ``threadtools.component_to_thread_signature()`` to
        ``componenttools.component_to_containment_signature()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import scoretools
    from abjad.tools import stafftools
    from abjad.tools import voicetools

    signature = componenttools.ContainmentSignature()
    signature._self = component._id_string
    for component in componenttools.get_improper_parentage_of_component(component):
        if isinstance(component, voicetools.Voice) and signature._voice is None:
            signature._voice = component._id_string
        elif isinstance(component, stafftools.Staff) and signature._staff is None:
            # leaves inside different staves have different containment signatures regardless of staff name
            signature._staff = '{}-{}'.format(component._class_name, id(component))
        elif isinstance(component, scoretools.StaffGroup) and signature._staff_group is None:
            signature._staff_group = component._id_string
        elif isinstance(component, scoretools.Score) and signature._score is None:
            signature._score = component._id_string
    else:
        # root components must be the same object for containment signatures to compare true
        signature._root = id(component)
        signature._root_str = component._id_string
    return signature
