# -*- encoding: utf-8 -*-
import abc
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


# TODO: extend repr to show target, if any
class Wizard(ScoreManagerObject):
    r'''Wizard.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    target_editor_class_name_suffix = 'Editor'

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        ScoreManagerObject.__init__(self, session=session)
        self.target = target

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
            session=self.session, 
            target=target,
            )
        return target_editor

    def _run(
        self,
        cache=False,
        clear=True,
        head=None,
        pending_user_input=None,
        ):
        self.session.io_manager._assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        self.session.push_breadcrumb(self._breadcrumb)
        if hasattr(self, 'selector'):
            selector = self.selector
        else:
            selector = self.handler_class_name_selector(session=self.session)
        handler_class_name = selector._run()
        if not self.session.backtrack():
            handler_editor = self._get_target_editor(handler_class_name)
            handler_editor._run(is_autoadvancing=True, is_autostarting=True)
            self.target = handler_editor.target
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
