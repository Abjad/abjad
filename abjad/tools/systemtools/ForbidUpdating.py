# -*- encoding: utf-8 -*-
import time
from abjad.tools.abctools import ContextManager


class ForbidUpdating(ContextManager):
    r'''A context manager for forbidding score updates.

    ..  container:: example

        ::

            >>> staff = Staff("c'32 d'2.. ~ d'16 e'32")
            >>> with systemtools.ForbidUpdating(component=staff):
            ...     for x in staff[:]:
            ...         mutate(x).replace(Chord(x))
            ...

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        ):
        from abjad.tools import scoretools
        prototype = (scoretools.Component, type(None))
        assert isinstance(component, prototype)
        self._component = component

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

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''Component of context manager.

        Return component.
        '''
        return self._component
