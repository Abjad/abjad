# -*- encoding: utf-8 -*-
import abc
from scoremanager.wizards.Wizard import Wizard


class HandlerCreationWizard(Wizard):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### PRIVATE METHODS ###

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
