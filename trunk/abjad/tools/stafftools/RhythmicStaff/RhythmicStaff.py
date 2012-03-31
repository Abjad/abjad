from abjad.tools.stafftools.Staff import Staff


class RhythmicStaff(Staff):
    '''Abjad model of a rhythmic staff.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    # TODO: do not use list in initializer! use none instead!
    def __init__(self, music=[], **kwargs):
        Staff.__init__(self, music, **kwargs)
        self.context_name = 'RhythmicStaff'
