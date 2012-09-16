from abjad.tools.stafftools.Staff import Staff


class RhythmicStaff(Staff):
    '''Abjad model of a rhythmic staff.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='RhythmicStaff', name=None):
        Staff.__init__(self, music=music, context_name=context_name, name=name)
