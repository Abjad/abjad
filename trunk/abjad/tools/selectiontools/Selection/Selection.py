from abjad.tools.abctools.AbjadObject import AbjadObject


class Selection(AbjadObject):
    '''.. versionadded:: 2.9

    Selection taken from a single score.

    Selection objects will eventually pervade the system and model all user selections.

    This means that selection objects will eventually serve as input
    to most functions in the API. Selection objects will also
    eventually be returned as output from most functions in the API.

    Selections are immutable and never change after instantiation.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_music',)

    _default_mandatory_input_arguments = ([], )

    ### INITIALIZER ###

    def __init__(self, music):
        if music is None:
            music = ()
        elif isinstance(music, (tuple, list)):
            music = tuple(music)
        else:
            music = (music, )
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        return expr in self.music

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self.music == expr.music

    def __getitem__(self, expr):
        return self.music.__getitem__(expr)

    def __len__(self):
        return len(self.music)

    def __ne__(self, expr):
        return not self == expr
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def music(self):
        '''Read-only tuple of components in selection.
        '''
        return self._music

    @property
    def start_offset(self):
        '''Read-only start offset of earliest component in selection.'''
        return min(x.start_offset for x in self)

    @property
    def stop_offset(self):
        '''Read-only stop offset of earliest component in selection.'''
        return max(x.stop_offset for x in self)
