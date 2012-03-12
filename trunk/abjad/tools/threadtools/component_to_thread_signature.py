from abjad.tools.componenttools._ContainmentSignature import _ContainmentSignature


def component_to_thread_signature(component):
    '''Return _ContainmentSignature giving the root and
    first voice, staff and score in parentage of component.
    '''
    from abjad.tools.scoretools.Score import Score
    from abjad.tools.stafftools.Staff import Staff
    from abjad.tools.voicetools.Voice import Voice
    from abjad.tools import componenttools
    from abjad.tools.scoretools import StaffGroup

    signature = _ContainmentSignature()
    signature._self = component._ID
    for component in componenttools.get_improper_parentage_of_component(component):
        if isinstance(component, Voice) and signature._voice is None:
            signature._voice = component._ID
        elif isinstance(component, Staff) and signature._staff is None:
            numeric_id = '%s-%s' % (component.__class__.__name__, id(component))
            signature._staff = numeric_id
        elif isinstance(component, StaffGroup) and signature._staffgroup is None:
            signature._staffgroup = component._ID
        elif isinstance(component, Score) and signature._score is None:
            signature._score = component._ID
    else:
        '''Root components must be manifestly equal to compare True.'''
        signature._root = id(component)
        signature._root_str = component._ID
    return signature
