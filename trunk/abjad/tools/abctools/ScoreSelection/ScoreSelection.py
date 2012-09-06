import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class ScoreSelection(AbjadObject):
    '''.. versionadded:: 2.9

    Abstract base class from which selection classes inherit.

    Score selections are immutable and never change after instantiation.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    __slots__ = ()

    _default_mandatory_input_arguments = ([], )

    ### INITIALIZER ###

    @abc.abstractmethod
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
