# -*- encoding: utf-8 -*-
import copy
from abjad.tools.scoretools.Leaf import Leaf


class Rest(Leaf):
    r'''A rest.

    ..  container:: example

        **Example.**

        ::

            >>> rest = Rest('r8.')
            >>> measure = Measure((3, 16), [rest])
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
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

    def __init__(self, *args):
        from abjad.tools import lilypondparsertools
        if len(args) == 1 and isinstance(args[0], str):
            string = '{{ {} }}'.format(args[0])
            parsed = lilypondparsertools.LilyPondParser()(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            args = [parsed[0]]
        if len(args) == 1 and isinstance(args[0], Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.lilypond_duration_multiplier
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 1 and not isinstance(args[0], str):
            written_duration = args[0]
            lilypond_multiplier = None
        elif len(args) == 2:
            written_duration, lilypond_multiplier = args
        else:
            message = 'can not initialize rest from {!r}.'
            raise ValueError(message.format(args))
        Leaf.__init__(self, written_duration, lilypond_multiplier)

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
        for mark in treble._get_marks(mark_classes=markuptools.Markup):
            mark.detach()
        for mark in bass._get_marks(mark_classes=markuptools.Markup):
            mark.detach()
        up_markup = self._get_markup(direction=Up)
        up_markup = [copy.copy(markup) for markup in up_markup]
        down_markup = self._get_markup(direction=Down)
        down_markup = [copy.copy(markup) for markup in down_markup]
        for markup in up_markup:
            markup(treble)
        for markup in down_markup:
            markup(bass)
        return treble, bass
