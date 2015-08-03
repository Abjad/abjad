# -*- encoding: utf-8 -*-
from abjad.tools.abctools import ContextManager


class ForbidUpdate(ContextManager):
    r'''A context manager for forbidding score updates.

    ..  container:: example

        ::

            >>> staff = Staff("c'32 d'2.. ~ d'16 e'32")
            >>> with systemtools.ForbidUpdate(component=staff):
            ...     for x in staff[:]:
            ...         mutate(x).replace(Chord(x))
            ...

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
        r'''Exist context manager.

        Returns none.
        '''
        if self.component is not None:
            self.component._is_forbidden_to_update = False
            if self.update_on_exit:
                self.component._update_now(offsets=True)

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''Component of context manager.

        Return component.
        '''
        return self._component

    @property
    def update_on_enter(self):
        r'''True if context manager updates offsets on enter.

        Returns boolean or none.
        '''
        return self._update_on_enter

    @property
    def update_on_exit(self):
        r'''True if context manager updates offsets on exit.

        Returns boolean or none.
        '''
        return self._update_on_exit