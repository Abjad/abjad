# -*- encoding: utf-8 -*-
from scoremanager.wizards.Wizard import Wizard
from scoremanager import iotools


class PitchClassTransformCreationWizard(Wizard):

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'pitch class transform creation wizard'

    ### PRIVATE METHODS ###

    def _run(
        self,
        cache=False,
        clear=True,
        head=None,
        pending_user_input=None,
        ):
        self._session.io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        function_application_pairs = []
        while True:
            breadcrumb = self.function_application_pairs_to_breadcrumb(
                function_application_pairs)
            self._session._push_breadcrumb(breadcrumb=breadcrumb)
            selector = iotools.Selector(session=self._session)
            items = []
            items.append('transpose')
            items.append('invert')
            items.append('multiply')
            selector.items = items
            selector.explicit_breadcrumb = self.get_explicit_breadcrumb(
                function_application_pairs)
            with self.backtracking:
                function_name = selector._run(clear=clear)
            if self._session._backtrack():
                break
            elif not function_name:
                self._session._pop_breadcrumb()
                continue
            function_arguments = self.get_function_arguments(function_name)
            if self._session._backtrack():
                break
            elif function_arguments is None:
                self._session._pop_breadcrumb()
                continue
            function_application_pairs.append(
                (function_name, function_arguments))
            self._session._pop_breadcrumb()
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)
        self.target = function_application_pairs
        return self.target

    ### PUBLIC METHODS ###

    def function_application_pairs_to_breadcrumb(
        self, function_application_pairs):
        if function_application_pairs:
            result = []
            for function_name, function_arguments in \
                function_application_pairs:
                string = function_name[0].upper()
                if string in ('T', 'M'):
                    string = string + str(function_arguments[0])
                result.append(string)
            result = ''.join(result)
            return '{} - {}'.format(self._breadcrumb, result)
        else:
            return self._breadcrumb

    def get_explicit_breadcrumb(self, function_application_pairs):
        if function_application_pairs:
            return 'append pitch-class transform:'

    def get_function_arguments(self, function_name):
        arguments = []
        if function_name in ('transpose', 'multiply'):
            getter = self._session.io_manager.make_getter(where=self._where)
            getter.append_integer_in_range('index', start=0, stop=11)
            result = getter._run()
            if self._session._backtrack():
                return
            arguments.append(result)
        return tuple(arguments)
