# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools.scoretools.Leaf import Leaf


class Skip(Leaf):
    r'''A LilyPond skip.

    ..  container:: example

        **Example.**

        ::

            >>> skip = scoretools.Skip((3, 16))
            >>> skip
            Skip('s8.')

        ..  doctest::

            >>> print format(skip)
            s8.

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _default_positional_input_arguments = (
        repr('s4'),
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import lilypondparsertools
        lilypond_duration_multiplier = None
        if isinstance(arg, str):
            input = '{{ {} }}'.format(arg)
            parsed = lilypondparsertools.LilyPondParser()(input)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arg = parsed[0]
        if isinstance(arg, Leaf):
            leaf = arg
            written_duration = leaf.written_duration
            multipliers = leaf._get_attached_items(durationtools.Multiplier)
            if 1 < len(multipliers):
                raise ValueError('too many multipliers')
            elif len(multipliers) == 1:
                lilypond_duration_multiplier = multipliers[0]
            self._copy_override_and_set_from_leaf(leaf)
        elif not isinstance(arg, str):
            written_duration = arg
        else:
            message = 'can not initialize skip from {!r}.'
            message = message.format(arg)
            raise ValueError(message)
        Leaf.__init__(self, written_duration)
        if lilypond_duration_multiplier is not None:
            assert isinstance(
                lilypond_duration_multiplier, 
                durationtools.Multiplier), repr(lilypond_duration_multiplier)
            attach(lilypond_duration_multiplier, self)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        return (self.written_duration,)

    ### PRIVATE PROPERTIES ###

    @property
    def _body(self):
        result = []
        result.append('s%s' % self._formatted_duration)
        return result

    @property
    def _compact_representation(self):
        return 's%s' % self._formatted_duration
