from abjad.tools.leaftools._Leaf import _Leaf
import copy


class Rest(_Leaf):
    '''Abjad model of a rest:

    ::

        abjad> Rest((3, 16))
        Rest('r8.')

    '''

    # TODO: add vertical positioning pitch only as needed #
    __slots__ = ('_vertical_positioning_pitch', )

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], _Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.duration_multiplier
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 1 and isinstance(args[0], str):
            written_duration = args[0].strip('r')
            lilypond_multiplier = None
        elif len(args) == 1 and not isinstance(args[0], str):
            written_duration = args[0]
            lilypond_multiplier = None
        elif len(args) == 2:
            written_duration, lilypond_multiplier = args
        else:
            raise ValueError('can not initialize rest from "%s".' % str(args))
        _Leaf.__init__(self, written_duration, lilypond_multiplier)
        self._initialize_keyword_values(**kwargs)

    # OVERRIDES #

    #__deepcopy__ = __copy__

    ### PRIVATE ATTRIBUTES ###

    @property
    def _body(self):
        '''Read-only body of rest.
        '''
        result = ''
        vertical_positioning_pitch = getattr(self, '_vertical_positioning_pitch', None)
        if vertical_positioning_pitch:
            result += str(vertical_positioning_pitch)
        else:
            result += 'r'
        #result += str(self.duration)
        result += str(self._formatted_duration)
        if vertical_positioning_pitch:
            result += r' \rest'
        return [result]

    @property
    def _compact_representation(self):
        #return 'r%s' % self.duration
        return 'r%s' % self._formatted_duration
