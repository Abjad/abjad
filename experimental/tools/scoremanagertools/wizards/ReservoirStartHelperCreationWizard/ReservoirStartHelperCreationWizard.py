from experimental.tools.scoremanagertools.wizards.Wizard import Wizard
from experimental.tools.scoremanagertools import selectors


class ReservoirStartHelperCreationWizard(Wizard):

    ### READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'reservoir start helpers creation wizard'

    ### PUBLIC METHODS ###

    def get_function_arguments(self, function_name):
        arguments = []
        if function_name in ('start at index n'):
            getter = self._io.make_getter(where=self.where())
            getter.append_integer('index')
            result = getter.run()
            if self._session.backtrack():
                return
            arguments.append(result)
        return tuple(arguments)

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        while True:
            function_application_pairs = []
            self._session.push_breadcrumb(self.breadcrumb)
            selector = selectors.ReservoirStartHelperSelector(session=self._session)
            self._session.push_backtrack()
            function_name = selector.run(clear=clear)
            self._session.pop_backtrack()
            if self._session.backtrack():
                break
            elif not function_name:
                self._session.pop_breadcrumb()
                continue
            function_arguments = self.get_function_arguments(function_name)
            if self._session.backtrack():
                break
            elif function_arguments is None:
                self._session.pop_breadcrumb()
                continue
            function_application_pairs.append((function_name, function_arguments))
            break
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        self.target = function_application_pairs
        return self.target
