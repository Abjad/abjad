from experimental.tools.scoremanagertools.wizards.Wizard import Wizard
from experimental.tools.scoremanagertools import selectors


class ReservoirStartHelperCreationWizard(Wizard):

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'reservoir start helpers creation wizard'

    ### PRIVATE METHODS ###

    def _run(self, cache=False, clear=True, head=None, pending_user_input=None):
        self.session.io_manager.assign_user_input(pending_user_input=pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            function_application_pairs = []
            self.session.push_breadcrumb(self._breadcrumb)
            selector = selectors.ReservoirStartHelperSelector(session=self.session)
            with self.backtracking:
                function_name = selector._run(clear=clear)
            if self.session.backtrack():
                break
            elif not function_name:
                self.session.pop_breadcrumb()
                continue
            function_arguments = self.get_function_arguments(function_name)
            if self.session.backtrack():
                break
            elif function_arguments is None:
                self.session.pop_breadcrumb()
                continue
            function_application_pairs.append((function_name, function_arguments))
            break
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        self.target = function_application_pairs
        return self.target

    ### PUBLIC METHODS ###

    def get_function_arguments(self, function_name):
        arguments = []
        if function_name in ('start at index n'):
            getter = self.session.io_manager.make_getter(where=self._where)
            getter.append_integer('index')
            result = getter._run()
            if self.session.backtrack():
                return
            arguments.append(result)
        return tuple(arguments)
