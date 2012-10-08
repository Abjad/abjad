import copy
from abjad.tools.leaftools.Leaf import Leaf


class Skip(Leaf):
    '''Abjad model of a LilyPond skip:

    ::

        >>> skiptools.Skip((3, 16))
        Skip('s8.')

    Return skip.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    _default_mandatory_input_arguments = (repr('s4'), )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import lilypondparsertools

        if len(args) == 1 and isinstance(args[0], str):
            input = '{{ {} }}'.format(args[0])
            parsed = lilypondparsertools.LilyPondParser()(input)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            args = [parsed[0]]
            #written_duration = args[0].strip('s')
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

    # SPECIAL METHODS #

    #__deepcopy__ = __copy__

    ### PRIVATE PROPERTIES ###

    @property
    def _body(self):
        result = []
        result.append('s%s' % self._formatted_duration)
        return result

    @property
    def _compact_representation(self):
        return 's%s' % self._formatted_duration
