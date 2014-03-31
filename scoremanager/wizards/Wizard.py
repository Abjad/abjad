# -*- encoding: utf-8 -*-
import abc
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Wizard(ScoreManagerObject):
    r'''Wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_target',
        '_target_editor_class_name_suffix',
        )

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        ScoreManagerObject.__init__(self, session=session)
        self._target = target
        self._target_editor_class_name_suffix = 'Editor'

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _breadcrumb(self):
        pass

    ### PRIVATE METHODS ###

    def _get_target_editor(self, target_class_name, target=None):
        target_editor_class_name = target_class_name
        target_editor_class_name += self._target_editor_class_name_suffix
        command = 'from scoremanager.editors'
        command += ' import {} as target_editor_class'
        command = command.format(target_editor_class_name)
        exec(command)
        target_editor = target_editor_class(
            session=self._session, 
            target=target,
            )
        return target_editor

    def _run(self, pending_user_input=None):
        from scoremanager import editors
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(self)
        with context:
            selector = self._selector
            handler_class_name = selector._run()
            if self._should_backtrack():
                return
            statement = 'target = handlertools.{}()'
            statement = statement.format(handler_class_name)
            exec('from abjad import *')
            exec('from experimental.tools import handlertools')
            exec(statement)
            assert target
            if hasattr(target, '_target_manifest'):
                handler_editor = editors.Editor(
                    session=self._session,
                    target=target,
                    )
            else:
                handler_editor = self._get_target_editor(handler_class_name)
            handler_editor._is_autoadvancing = True
            handler_editor._is_autostarting = True
            handler_editor._run()
            self._target = handler_editor.target

    def _should_backtrack(self):
        if self._session.is_complete:
            return True
        elif self._session.is_backtracking_to_score_manager:
            return True
        # keep on backtracking ... do not consume this backtrack
        elif self._session.is_backtracking_locally:
            return True
        elif self._session.is_backtracking_to_score:
            return True
        elif self._session.is_autonavigating_within_score:
            return True
        else:
            return False

    ### PUBLIC PROPERTIES ###

    @property
    def target(self):
        r'''Gets wizard target.

        Returns object or none.
        '''
        return self._target