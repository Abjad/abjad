#from abjad.interfaces.ParentageInterface.containment import _ContainmentSignature
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
        if isinstance(component, Voice) and not signature._voice:
            signature._voice = component._ID
        elif isinstance(component, Staff) and not signature._staff:
            numeric_id = '%s-%s' % (component.__class__.__name__, id(component))
            signature._staff = numeric_id
        elif isinstance(component, StaffGroup) and not signature._staffgroup:
            signature._staffgroup = component._ID
        elif isinstance(component, Score) and not signature._score:
            signature._score = component._ID
    else:
        '''Root components must be manifestly equal to compare True.'''
        signature._root = id(component)
        signature._root_str = component._ID
    return signature
