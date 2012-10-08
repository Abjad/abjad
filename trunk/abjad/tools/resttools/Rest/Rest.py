import copy
from abjad.tools.leaftools.Leaf import Leaf


class Rest(Leaf):
    '''Abjad model of a rest:

    ::

        >>> Rest((3, 16))
        Rest('r8.')

    '''

    ### CLASS ATTRIBUTES ###

    # TODO: add vertical positioning pitch only as needed #
    __slots__ = ('_vertical_positioning_pitch', )

    _default_mandatory_input_arguments = (repr('r4'), )

    ### INITIALIZER ###

    # TODO: use LilyPond parser for initialization
    def __init__(self, *args, **kwargs):
        from abjad.tools import lilypondparsertools

        if len(args) == 1 and isinstance(args[0], str):
            input = '{{ {} }}'.format(args[0])
            parsed = lilypondparsertools.LilyPondParser()(input)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            args = [parsed[0]]
            #written_duration = args[0].strip('r')
            #lilypond_multiplier = None

        if len(args) == 1 and isinstance(args[0], Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.duration_multiplier
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 1 and not isinstance(args[0], str):
            written_duration = args[0]
            lilypond_multiplier = None
        elif len(args) == 2:
            written_duration, lilypond_multiplier = args
        else:
            raise ValueError('can not initialize rest from "%s".' % str(args))

        Leaf.__init__(self, written_duration, lilypond_multiplier)
        self._initialize_keyword_values(**kwargs)

    ### PRIVATE PROPERTIES ###

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
        result += str(self._formatted_duration)
        if vertical_positioning_pitch:
            result += r' \rest'
        return [result]

    @property
    def _compact_representation(self):
        return 'r%s' % self._formatted_duration
