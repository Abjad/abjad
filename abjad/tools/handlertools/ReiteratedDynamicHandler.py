# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class ReiteratedDynamicHandler(DynamicHandler):
    r'''Reiterated dynamic handler.

    ..  container:: example

        ::

            >>> handler = handlertools.ReiteratedDynamicHandler(
            ...     dynamic_name='f',
            ...     )
            >>> staff = Staff("c'4. ~ c'8 d'4 e'4")
            >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
            >>> logical_ties = list(logical_ties)
            >>> logical_ties = handler(logical_ties)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'4. \f ~
                c'8
                d'4 \f
                e'4 \f
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_dynamic_name',
        )

    ### INITIALIZER ###

    def __init__(self, dynamic_name=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if dynamic_name is not None:
            assert indicatortools.Dynamic.is_dynamic_name(dynamic_name)
        self._dynamic_name = dynamic_name

    ### SPECIAL METHODS ###

    def __call__(self, expr, timespan=None):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        prototype = (scoretools.Note, scoretools.Chord)
        for note_or_chord in iterate(expr).by_class(prototype):
            #indicatortools.Dynamic(self.dynamic_name)(note_or_chord)
            command = indicatortools.LilyPondCommand(
                self.dynamic_name,
                'right',
                )
            logical_tie = inspect_(note_or_chord).get_logical_tie()
            if note_or_chord is logical_tie.head:
                attach(command, note_or_chord)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic_name(self):
        r'''Gets dynamic name of handler.

        Returns string or none.
        '''
        return self._dynamic_name