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
            getter = self.io.make_getter(where=self.where())
            getter.append_integer('index')
            result = getter.run()
            if self.session.backtrack():
                return
            arguments.append(result)
        return tuple(arguments)

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.io.assign_user_input(user_input=user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            function_application_pairs = []
            self.session.push_breadcrumb(self.breadcrumb)
            selector = selectors.ReservoirStartHelperSelector(session=self.session)
            self.session.push_backtrack()
            function_name = selector.run(clear=clear)
            self.session.pop_backtrack()
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
