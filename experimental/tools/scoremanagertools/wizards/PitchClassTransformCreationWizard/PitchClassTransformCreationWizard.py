from experimental.tools.scoremanagertools.wizards.Wizard import Wizard
from experimental.tools.scoremanagertools import selectors


class PitchClassTransformCreationWizard(Wizard):

    ### PRIVATE METHODS ###

    def _run(self, cache=False, clear=True, head=None, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        function_application_pairs = []
        while True:
            breadcrumb = self.function_application_pairs_to_breadcrumb(function_application_pairs)
            self._session.push_breadcrumb(breadcrumb=breadcrumb)
            selector = selectors.PitchClassTransformSelector(session=self._session)
            selector.explicit_breadcrumb = self.get_explicit_breadcrumb(function_application_pairs)
            self._session.push_backtrack()
            function_name = selector._run(clear=clear)
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
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)
        self.target = function_application_pairs
        return self.target
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
            getter = self._io.make_getter(where=self._where)
            getter.append_integer_in_range('index', start=0, stop=11)
            result = getter._run()
            if self._session.backtrack():
                return
            arguments.append(result)
        return tuple(arguments)
