# -*- encoding: utf-8 -*-
import abc
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Wizard(ScoreManagerObject):
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
        ScoreManagerObject.__init__(self, session=session)
        self._selector = None
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
            class_name = selector._run()
            if self._should_backtrack():
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
            if hasattr(target, '_attribute_manifest'):
                editor = editors.Editor(
                    session=self._session,
                    target=target,
                    )
            else:
                editor = self._get_target_editor(class_name)
            editor._is_autoadvancing = True
            editor._is_autostarting = True
            editor._run()
            self._target = editor.target

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