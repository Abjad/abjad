# -*- encoding: utf-8 -*-
import abc
from scoremanager.core.Controller import Controller


class Wizard(Controller):
    r'''Wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_selector',
        '_target',
        '_target_editor_class_name_suffix',
        )

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        Controller.__init__(self, session=session)
        self._selector = None
        self._target = target
        self._target_editor_class_name_suffix = 'Autoeditor'

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _breadcrumb(self):
        pass

    ### PRIVATE METHODS ###

    def _run(self, pending_input=None):
        from scoremanager import iotools
        if pending_input:
            self._session._pending_input = pending_input
        context = iotools.ControllerContext(controller=self)
        with context:
            selector = self._selector
            class_name = selector._run()
            if self._session.is_backtracking:
                return
            exec('from abjad import *')
            if class_name.endswith('Handler'):
                statement = 'target = handlertools.{}()'
                statement = statement.format(class_name)
                exec('from experimental.tools import handlertools')
                exec(statement)
            elif class_name.endswith('RhythmMaker'):
                statement = 'target = rhythmmakertools.{}()'
                statement = statement.format(class_name)
                exec(statement)
            else:
                raise ValueError(class_name)
            assert target
            autoeditor = iotools.Autoeditor(
                session=self._session,
                target=target,
                )
            autoeditor._is_autoadvancing = True
            autoeditor._is_autostarting = True
            autoeditor._run()
            self._target = autoeditor.target

    ### PUBLIC PROPERTIES ###

    @property
    def target(self):
        r'''Gets wizard target.

        Returns object or none.
        '''
        return self._target