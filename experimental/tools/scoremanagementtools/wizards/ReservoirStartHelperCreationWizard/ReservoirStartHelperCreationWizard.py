from experimental.tools.scoremanagementtools.wizards.Wizard import Wizard
from experimental.tools.scoremanagementtools import selectors


class ReservoirStartHelperCreationWizard(Wizard):

    ### READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'reservoir start helpers creation wizard'

    ### PUBLIC METHODS ###

    def get_function_arguments(self, function_name):
        arguments = []
        if function_name in ('start at index n'):
            getter = self.make_getter(where=self.where())
            getter.append_integer('index')
            result = getter.run()
            if self.backtrack():
                return
            arguments.append(result)
        return tuple(arguments)

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            function_application_pairs = []
            self.push_breadcrumb()
            selector = selectors.ReservoirStartHelperSelector(session=self.session)
            self.push_backtrack()
            function_name = selector.run(clear=clear)
            self.pop_backtrack()
            if self.backtrack():
                break
            elif not function_name:
                self.pop_breadcrumb()
                continue
            function_arguments = self.get_function_arguments(function_name)
            if self.backtrack():
                break
            elif function_arguments is None:
                self.pop_breadcrumb()
                continue
            function_application_pairs.append((function_name, function_arguments))
            break
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        self.target = function_application_pairs
        return self.target
