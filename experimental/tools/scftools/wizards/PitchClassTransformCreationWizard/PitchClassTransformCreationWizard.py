from experimental.tools.scftools.wizards.Wizard import Wizard
from experimental.tools.scftools import selectors


class PitchClassTransformCreationWizard(Wizard):

    ### READ-ONLY PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'pitch class transform creation wizard'

    ### PUBLIC METHODS ###

    def function_application_pairs_to_breadcrumb(self, function_application_pairs):
        if function_application_pairs:
            result = []
            for function_name, function_arguments in function_application_pairs:
                string = function_name[0].upper()
                if string in ('T', 'M'):
                    string = string + str(function_arguments[0])
                result.append(string)
            result = ''.join(result)
            return '{} - {}'.format(self.breadcrumb, result)
        else:
            return self.breadcrumb

    def get_explicit_breadcrumb(self, function_application_pairs):
        if function_application_pairs:
            return 'append pitch-class transform:'

    def get_function_arguments(self, function_name):
        arguments = []
        if function_name in ('transpose', 'multiply'):
            getter = self.make_getter(where=self.where())
            getter.append_integer_in_range('index', start=0, stop=11)
            result = getter.run()
            if self.backtrack():
                return
            arguments.append(result)
        return tuple(arguments)

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        function_application_pairs = []
        while True:
            breadcrumb = self.function_application_pairs_to_breadcrumb(function_application_pairs)
            self.push_breadcrumb(breadcrumb=breadcrumb)
            selector = selectors.PitchClassTransformSelector(session=self.session)
            selector.explicit_breadcrumb = self.get_explicit_breadcrumb(function_application_pairs)
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
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        self.target = function_application_pairs
        return self.target
