# -*- coding: utf-8 -*-
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

            >>> print(format(skip))
            s8.

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools.topleveltools import parse
        input_leaf = None
        written_duration = None
        if len(args) == 1 and isinstance(args[0], str):
            string = '{{ {} }}'.format(args[0])
            parsed = parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            input_leaf = parsed[0]
            written_duration = input_leaf.written_duration
        elif len(args) == 1 and isinstance(args[0], Leaf):
            written_duration = args[0].written_duration
            input_leaf = args[0]
        elif len(args) == 1 and not isinstance(args[0], str):
            written_duration = args[0]
        elif len(args) == 0:
            written_duration = durationtools.Duration(1, 4)
        else:
            message = 'can not initialize skip from {!r}.'
            message = message.format(args)
            raise ValueError(message)
        Leaf.__init__(self, written_duration)
        if input_leaf is not None:
            self._copy_override_and_set_from_leaf(input_leaf)

    ### PRIVATE PROPERTIES ###

    @property
    def _body(self):
        result = []
        result.append('s%s' % self._formatted_duration)
        return result

    @property
    def _compact_representation(self):
        return 's%s' % self._formatted_duration
