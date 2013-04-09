from abc import ABCMeta
from abc import abstractmethod
from scftools.wizards.Wizard import Wizard


class HandlerCreationWizard(Wizard):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### PUBLIC METHODS ###

    # TODO: abstract up to Wizard?
    def get_handler_editor(self, handler_class_name, target=None):
        handler_editor_class_name = handler_class_name + self.handler_editor_class_name_suffix
        command = 'from scftools.editors import {} as handler_editor_class'.format(handler_editor_class_name)
        exec(command)
        handler_editor = handler_editor_class(session=self.session, target=target)
        return handler_editor

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        selector = self.handler_class_name_selector(session=self.session)
        handler_class_name = selector.run()
        if not self.backtrack():
            handler_editor = self.get_handler_editor(handler_class_name)
            handler_editor.run(is_autoadvancing=True, is_autostarting=True)
            self.target = handler_editor.target
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
