# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import io
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class ParameterSpecifierCreationWizard(Wizard):

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'parameter specifier creation wizard'

    ### PRIVATE METHODS ###

    def _run(
        self,
        cache=False,
        clear=True,
        head=None,
        pending_user_input=None,
        ):
        self.session.io_manager.assign_user_input(
            pending_user_input=pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        self.session.push_breadcrumb(self._breadcrumb)
        selector = \
            io.Selector.make_parameter_specifier_class_name_selector(
            session=self.session,
            )
        with self.backtracking:
            target_class_name = selector._run()
        if self.session.backtrack():
            self.session.pop_breadcrumb()
            self.session.restore_breadcrumbs(cache=cache)
            return
        target_editor = self.get_target_editor(target_class_name)
        with self.backtracking:
            target_editor._run()
        if self.session.backtrack():
            self.session.pop_breadcrumb()
            self.session.restore_breadcrumbs(cache=cache)
            return
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        self.target = target_editor.target
        return self.target

    ### PUBLIC METHODS ###

    # TODO: maybe abstract up to Wizard?
    def get_target_editor(self, target_class_name, target=None):
        target_editor_class_name = \
            target_class_name + self.target_editor_class_name_suffix
        command = 'from experimental.tools.scoremanagertools.editors'
        command += ' import {} as target_editor_class'
        command = command.format(target_editor_class_name)
        exec(command)
        target_editor = target_editor_class(
            session=self.session, target=target)
        return target_editor
