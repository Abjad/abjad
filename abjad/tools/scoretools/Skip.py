# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools.scoretools.Leaf import Leaf


class Skip(Leaf):
    r'''A LilyPond skip.

    ..  container:: example

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

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import lilypondparsertools
        if isinstance(arg, str):
            input = '{{ {} }}'.format(arg)
            parsed = lilypondparsertools.LilyPondParser()(input)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arg = parsed[0]
        if isinstance(arg, Leaf):
            written_duration = arg.written_duration
        elif not isinstance(arg, str):
            written_duration = arg
        elif len(args) == 0:
            written_duration = durationtools.Duration(1, 4)
        else:
            message = 'can not initialize skip from {!r}.'
            message = message.format(arg)
            raise ValueError(message)
        Leaf.__init__(self, written_duration)
        if isinstance(arg, Leaf):
            self._copy_override_and_set_from_leaf(arg)

    ### PRIVATE PROPERTIES ###

    @property
    def _body(self):
        result = []
        result.append('s%s' % self._formatted_duration)
        return result

    @property
    def _compact_representation(self):
        return 's%s' % self._formatted_duration
