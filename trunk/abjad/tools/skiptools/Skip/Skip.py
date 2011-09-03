from abjad.tools.leaftools._Leaf import _Leaf
import copy


class Skip(_Leaf):
    '''Abjad model of a LilyPond skip:

    ::

        abjad> skiptools.Skip((3, 16))
        Skip('s8.')

    Return skip.
    '''

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], _Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.duration_multiplier
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 1 and isinstance(args[0], str):
            written_duration = args[0].strip('s')
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
        result = []
        result.append('s%s' % self._formatted_duration)
        return result

    @property
    def _compact_representation(self):
        return 's%s' % self._formatted_duration
