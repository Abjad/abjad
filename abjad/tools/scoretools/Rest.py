# -*- coding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools.scoretools.Leaf import Leaf
from abjad.tools.topleveltools import detach


class Rest(Leaf):
    r'''A rest.

    ..  container:: example

        ::

            >>> rest = Rest('r8.')
            >>> measure = Measure((3, 16), [rest])
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> print(format(measure))
            {
                \time 3/16
                r8.
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, written_duration=None):
        from abjad.tools.topleveltools import parse
        original_input = written_duration
        if isinstance(written_duration, str):
            string = '{{ {} }}'.format(written_duration)
            parsed = parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            written_duration = parsed[0]
        if isinstance(written_duration, Leaf):
            written_duration = written_duration.written_duration
        elif written_duration is None:
            written_duration = durationtools.Duration(1, 4)
        else:
            written_duration = durationtools.Duration(written_duration)
        Leaf.__init__(self, written_duration)
        if isinstance(original_input, Leaf):
            self._copy_override_and_set_from_leaf(original_input)

    ### PRIVATE METHODS ###

    def _divide(self, pitch=None):
        from abjad.tools import markuptools
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

    ### PRIVATE PROPERTIES ###

    @property
    def _body(self):
        return [self._compact_representation]

    @property
    def _compact_representation(self):
        return 'r{}'.format(self._formatted_duration)
