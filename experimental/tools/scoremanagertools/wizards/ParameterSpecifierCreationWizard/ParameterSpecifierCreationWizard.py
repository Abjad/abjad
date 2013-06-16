from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.wizards.Wizard import Wizard


class ParameterSpecifierCreationWizard(Wizard):

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'parameter specifier creation wizard'

    ### PRIVATE METHODS ###

    def _run(self, cache=False, clear=True, head=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        self._session.push_breadcrumb(self._breadcrumb)
        selector = selectors.ParameterSpecifierClassNameSelector(session=self._session)
        with self.backtracking:
            target_class_name = selector._run()
        if self._session.backtrack():
            self._session.pop_breadcrumb()
            self._session.restore_breadcrumbs(cache=cache)
            return
        target_editor = self.get_target_editor(target_class_name)
        with self.backtracking:
            target_editor._run()
        if self._session.backtrack():
            self._session.pop_breadcrumb()
            self._session.restore_breadcrumbs(cache=cache)
            return
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        self.target = target_editor.target
        return self.target

    ### PUBLIC METHODS ###

    # TODO: maybe abstract up to Wizard?
    def get_target_editor(self, target_class_name, target=None):
        target_editor_class_name = target_class_name + self.target_editor_class_name_suffix
        command = 'from experimental.tools.scoremanagertools.editors import {} as target_editor_class'.format(target_editor_class_name)
        exec(command)
        target_editor = target_editor_class(session=self._session, target=target)
        return target_editor
