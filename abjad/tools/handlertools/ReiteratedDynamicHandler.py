# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.Handler import Handler


class ReiteratedDynamicHandler(Handler):
    r'''Reiterated dynamic handler.

    ..  container:: example

        **Example 1.** With one dynamic:

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

    ..  container:: example

        **Example 2.** With multiple dynamics:

        ::

            >>> handler = handlertools.ReiteratedDynamicHandler(
            ...     dynamic_name='f p',
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
                d'4 \p
                e'4 \f
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_dynamic_name',
        '_dynamic_names',
        '_minimum_duration',
        )

    ### INITIALIZER ###

    def __init__(self, dynamic_name=None, minimum_duration=None):
        self._dynamic_name = dynamic_name
        dynamic_names = ()
        if dynamic_name is not None:
            assert isinstance(dynamic_name, str), repr(dynamic_name)
            dynamic_names = dynamic_name.split()
        for dynamic_name in dynamic_names:
            assert indicatortools.Dynamic.is_dynamic_name(dynamic_name)
        dynamic_names = datastructuretools.CyclicTuple(dynamic_names)
        self._dynamic_names = dynamic_names
        if minimum_duration is not None:
            minimum_duration = durationtools.Duration(minimum_duration)
        self._minimum_duration = minimum_duration

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        note_or_chords = []
        prototype = (scoretools.Note, scoretools.Chord)
        logical_ties = iterate(expr).by_logical_tie()
        logical_ties = [
            _ for _ in logical_ties if isinstance(_.head, prototype)]
        for i, logical_tie in enumerate(logical_ties):
            #indicatortools.Dynamic(self.dynamic_name)(note_or_chord)
            dynamic_name = self._dynamic_names[i]
            command = indicatortools.LilyPondCommand(
                dynamic_name,
                'right',
                )
            attach(command, logical_tie.head)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic_name(self):
        r'''Gets dynamic name.

        Returns string or none.
        '''
        return self._dynamic_name

    @property
    def minimum_duration(self):
        r'''Gets minimum duration of duration handler.

        Returns duration or none.
        '''
        return self._minimum_duration