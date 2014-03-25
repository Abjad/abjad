# -*- encoding: utf-8 -*-
import abc
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Wizard(ScoreManagerObject):
    r'''Wizard.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta


    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        ScoreManagerObject.__init__(self, session=session)
        self.target = target
        self.target_editor_class_name_suffix = 'Editor'

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _breadcrumb(self):
        pass

    ### PRIVATE METHODS ###

    def _get_target_editor(self, target_class_name, target=None):
        target_editor_class_name = target_class_name
        target_editor_class_name += self.target_editor_class_name_suffix
        command = 'from scoremanager.editors'
        command += ' import {} as target_editor_class'
        command = command.format(target_editor_class_name)
        exec(command)
        target_editor = target_editor_class(
            session=self._session, 
            target=target,
            )
        return target_editor

    def _run(
        self,
        clear=True,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        if hasattr(self, 'selector'):
            selector = self.selector
        else:
            selector = self.handler_class_name_selector(session=self._session)
        handler_class_name = selector._run()
        if not self._exit_io_method():
            handler_editor = self._get_target_editor(handler_class_name)
            handler_editor._run(is_autoadvancing=True, is_autostarting=True)
            self.target = handler_editor.target