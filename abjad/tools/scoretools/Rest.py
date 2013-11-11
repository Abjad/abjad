# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools.scoretools.Leaf import Leaf
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach


class Rest(Leaf):
    r'''A rest.

    ..  container:: example

        **Example.**

        ::

            >>> rest = Rest('r8.')
            >>> measure = Measure((3, 16), [rest])
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> print format(measure)
            {
                \time 3/16
                r8.
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _default_positional_input_arguments = (
        repr('r4'),
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import lilypondparsertools
        lilypond_duration_multiplier = None
        if isinstance(arg, str):
            string = '{{ {} }}'.format(arg)
            parsed = lilypondparsertools.LilyPondParser()(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arg = parsed[0]
        if isinstance(arg, Leaf):
            leaf = arg
            written_duration = leaf.written_duration
            lilypond_duration_multiplier = leaf.lilypond_duration_multiplier
            if lilypond_duration_multiplier is None:
                multipliers = leaf._get_attached_items(
                    durationtools.Multiplier)
                if 1 < len(multipliers):
                    raise ValueError('too many multipliers')
                elif len(multipliers) == 1:
                    lilypond_duration_multiplier = multipliers[0]
            self._copy_override_and_set_from_leaf(leaf)
        elif not isinstance(arg, str):
            written_duration = arg
        else:
            message = 'can not initialize rest from {!r}.'
            message = message.format(arg)
            raise ValueError(message)
        Leaf.__init__(self, written_duration)
        if lilypond_duration_multiplier is not None:
            assert isinstance(
                lilypond_duration_multiplier, 
                durationtools.Multiplier), repr(lilypond_duration_multiplier)
            attach(lilypond_duration_multiplier, self)

    ### SPECIAL METHODS ###

    # TODO: remove after deprecating lilypond_duration_multiplier
    def __getnewargs__(self):
        return (self.written_duration,)

    ### PRIVATE PROPERTIES ###

    @property
    def _body(self):
        return [self._compact_representation]

    @property
    def _compact_representation(self):
        return 'r{}'.format(self._formatted_duration)

    ### PRIVATE METHODS ###

    def _divide(self, pitch=None):
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        treble = copy.copy(self)
        bass = copy.copy(self)
        detach(markuptools.Markup, treble)
        detach(markuptools.Markup, bass)
        up_markup = self._get_markup(direction=Up)
        up_markup = [copy.copy(markup) for markup in up_markup]
        down_markup = self._get_markup(direction=Down)
        down_markup = [copy.copy(markup) for markup in down_markup]
        for markup in up_markup:
            markup(treble)
        for markup in down_markup:
            markup(bass)
        return treble, bass
