# -*- coding: utf-8 -*-
from abjad.tools.abctools import ContextManager


class ForbidUpdate(ContextManager):
    r'''A context manager for forbidding score updates.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 ~ d'2 e'4")
            >>> with systemtools.ForbidUpdate(component=staff):
            ...     for note in staff[:]:
            ...         pitch_1 = note.written_pitch
            ...         pitch_2 = pitch_1 + pitchtools.NamedInterval('M3')
            ...         pitches = [pitch_1, pitch_2]
            ...         chord = Chord(pitches, note.written_duration)
            ...         mutate(note).replace(chord)
            ...

        ::

            >>> inspect_(staff).is_well_formed()
            True

        ::

            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' e'>8
                <d' fs'>8 ~
                <d' fs'>2
                <e' gs'>4
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_component',
        '_update_on_enter',
        '_update_on_exit',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        update_on_enter=True,
        update_on_exit=None,
        ):
        from abjad.tools import scoretools
        prototype = (scoretools.Component, type(None))
        assert isinstance(component, prototype)
        self._component = component
        if update_on_enter is not None:
            update_on_enter = bool(update_on_enter)
        self._update_on_enter = update_on_enter
        if update_on_exit is not None:
            update_on_exit = bool(update_on_exit)
        self._update_on_exit = update_on_exit

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager.

        Returns context manager.
        '''
        if self.component is not None:
            self.component._update_now(offsets=True)
            self.component._is_forbidden_to_update = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager.

        Returns none.
        '''
        if self.component is not None:
            self.component._is_forbidden_to_update = False
            if self.update_on_exit:
                self.component._update_now(offsets=True)

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''Gets component.

        Set to component or none.

        Returns component or none.
        '''
        return self._component

    @property
    def update_on_enter(self):
        r'''Is true when context manager should update offsets on enter.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._update_on_enter

    @property
    def update_on_exit(self):
        r'''Is true when context manager should update offsets on exit.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._update_on_exit