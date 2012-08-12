from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools.rhythmtreetools.RhythmTreeNode import RhythmTreeNode


class RhythmTreeLeaf(RhythmTreeNode):
    '''A leaf node in a rhythm tree:

    ::

        >>> leaf = rhythmtreetools.RhythmTreeLeaf(duration=5, pitched=True)
        >>> leaf
        RhythmTreeLeaf(
            duration=5,
            pitched=True,
            )
    
    Call with a pulse duration to generate Abjad leaf objects:

    ::

        >>> result = leaf((1, 8))
        >>> result
        [Note("c'2"), Note("c'8")]

    Generates rests when called, if `pitched` is False:

    ::

        >>> rhythmtreetools.RhythmTreeLeaf(duration=7, pitched=False)((1, 16))
        [Rest('r4..')]

    Return `RhythmTreeLeaf`.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_offset', '_offsets_are_current', '_parent', '_pitched')

    ### INITIALIZER ###

    def __init__(self, duration=1, pitched=True):
        RhythmTreeNode.__init__(self, duration)
        self.pitched = pitched

    ### SPECIAL METHODS ###

    def __call__(self, pulse_duration):
        '''Generate Abjad score components:

        ::

            >>> leaf = rhythmtreetools.RhythmTreeLeaf(5)
            >>> leaf((1, 4))
            [Note("c'1"), Note("c'4")]

        Return sequence of components.
        '''
        pulse_duration = durationtools.Duration(pulse_duration)
        total_duration = pulse_duration * self.duration
        if self.pitched:
            return notetools.make_notes(0, total_duration)
        return resttools.make_rests(total_duration)

    def __deepcopy__(self, memo):
        return type(self)(*self.__getnewargs__())

    def __eq__(self, other):
        if type(self) == type(other):
            if self.duration == other.duration:
                if self.pitched == other.pitched:
                    return True
        return False

    def __getnewargs__(self):
        return (self.duration, self.pitched)

    def __repr__(self):
        result = ['{}('.format(self._class_name)]
        result.extend(self._get_tools_package_qualified_keyword_argument_repr_pieces())
        result.append('\t)')
        return '\n'.join(result)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _pretty_rtm_format_pieces(self):
        return [str(self.duration)]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        '''The node's RTM format:

        Return string.
        '''
        if self.pitched:
            return '{}'.format(self.duration)
        return '-{}'.format(self.duration)

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def pitched():
        def fget(self):
            '''True if leaf is pitched.'''
            return self._pitched
        def fset(self, arg):
            self._pitched = bool(arg)
        return property(**locals())

