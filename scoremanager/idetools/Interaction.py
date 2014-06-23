# -*- encoding: utf-8 -*-
from abjad.tools.abctools.ContextManager import ContextManager


class Interaction(ContextManager):
    r'''Interation context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_confirm',
        '_controller',
        '_display',
        '_dry_run',
        '_original_confirm',
        '_original_display',
        '_task',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        confirm=True,
        controller=None, 
        display=True, 
        dry_run=False,
        task=True,
        ):
        self._confirm = confirm
        self._controller = controller
        self._display = display
        self._dry_run = dry_run
        self._original_confirm = None
        self._original_display = None
        self._task = task

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters interaction manager.

        Returns none.
        '''
        if self.task:
            self._controller._session._task_depth += 1
        self._original_confirm = self._controller._session.confirm
        self._original_display = self._controller._session.display
        self._controller._session._confirm = self.confirm
        self._controller._session._display = self.display

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Exits interaction manager.

        Returns none.
        '''
        if self.task:
            self._controller._session._task_depth -= 1
        if self.display and not self.dry_run:
            if self.task:
                if 0 < len(self._controller._transcript.entries):
                    if not self._controller._transcript[-1][-1] == '':
                        self.controller._io_manager._display('')
        self._controller._session._confirm = self._original_confirm
        self._controller._session._display = self._original_display

    ### PUBLIC PROPERTIES ###

    @property
    def confirm(self):
        r'''Is true when interaction should display confirmation messaging.
        Otherwise false.

        Returns boolean.
        '''
        return self._confirm

    @property
    def controller(self):
        r'''Gets controller of interaction.

        Returns controller.
        '''
        return self._controller

    @property
    def display(self):
        r'''Is true when blank line should display at end of interaction.
        Otherwise false.

        Returns boolean.
        '''
        return self._display

    @property
    def dry_run(self):
        r'''Is true when interaction is dry run. Otherwise false.

        Nothing will be displayed during dry run.

        Inputs and outputs will be returned from dry run.

        Returns boolean.
        '''
        return self._dry_run

    @property
    def task(self):
        r'''Is true when interaction is a task. Otherwise false.

        Main menus are not tasks; public methods are tasks.

        Tasks are not implemented around a while-true loop; main menus are
        implemented around a while-true loop.

        Returns boolean.
        '''
        return self._task