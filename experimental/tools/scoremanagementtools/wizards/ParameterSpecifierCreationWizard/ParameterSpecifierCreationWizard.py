from experimental.tools.scoremanagementtools import selectors
from experimental.tools.scoremanagementtools.wizards.Wizard import Wizard


class ParameterSpecifierCreationWizard(Wizard):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'parameter specifier creation wizard'

    ### PUBLIC METHODS ###

    # TODO: maybe abstract up to Wizard?
    def get_target_editor(self, target_class_name, target=None):
        target_editor_class_name = target_class_name + self.target_editor_class_name_suffix
        command = 'from experimental.tools.scoremanagementtools.editors import {} as target_editor_class'.format(target_editor_class_name)
        exec(command)
        target_editor = target_editor_class(session=self.session, target=target)
        return target_editor

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        selector = selectors.ParameterSpecifierClassNameSelector(session=self.session)
        self.push_backtrack()
        target_class_name = selector.run()
        self.pop_backtrack()
        if self.backtrack():
            self.pop_breadcrumb()
            self.restore_breadcrumbs(cache=cache)
            return
        target_editor = self.get_target_editor(target_class_name)
        self.push_backtrack()
        target_editor.run()
        self.pop_backtrack()
        if self.backtrack():
            self.pop_breadcrumb()
            self.restore_breadcrumbs(cache=cache)
            return
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        self.target = target_editor.target
        return self.target
