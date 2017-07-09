# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.scoretools.Leaf import Leaf


class Skip(Leaf):
    r'''LilyPond skip.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> skip = abjad.Skip((3, 16))
            >>> skip
            Skip('s8.')

        ..  docs::

            >>> f(skip)
            s8.

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *arguments):
        from abjad.tools.topleveltools import parse
        input_leaf = None
        written_duration = None
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = '{{ {} }}'.format(arguments[0])
            parsed = parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            input_leaf = parsed[0]
            written_duration = input_leaf.written_duration
        elif len(arguments) == 1 and isinstance(arguments[0], Leaf):
            written_duration = arguments[0].written_duration
            input_leaf = arguments[0]
        elif len(arguments) == 1 and not isinstance(arguments[0], str):
            written_duration = arguments[0]
        elif len(arguments) == 0:
            written_duration = durationtools.Duration(1, 4)
        else:
            message = 'can not initialize skip from {!r}.'
            message = message.format(arguments)
            raise ValueError(message)
        Leaf.__init__(self, written_duration)
        if input_leaf is not None:
            self._copy_override_and_set_from_leaf(input_leaf)

    ### PRIVATE METHODS ###

    def _get_body(self):
        result = []
        result.append('s%s' % self._get_formatted_duration())
        return result

    def _get_compact_representation(self):
        return 's%s' % self._get_formatted_duration()
