# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.wizards.Wizard import Wizard


class PitchClassTransformCreationWizard(Wizard):
    r'''Pitch-class transform creation wizard.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'pitch class transform creation wizard'

    ### PRIVATE METHODS ###

    def _function_application_pairs_to_breadcrumb(
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

    def _get_explicit_breadcrumb(self, function_application_pairs):
        if function_application_pairs:
            return 'append pitch-class transform:'

    def _get_function_arguments(self, function_name):
        arguments = []
        if function_name in ('transpose', 'multiply'):
            getter = self._io_manager.make_getter(where=self._where)
            getter.append_integer_in_range('index', start=0, stop=11)
            result = getter._run()
            if self._session._backtrack():
                return
            arguments.append(result)
        return tuple(arguments)

    def _run(
        self,
        cache=False,
        clear=True,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        self._session._cache_breadcrumbs(cache=cache)
        function_application_pairs = []
        while True:
            breadcrumb = self._function_application_pairs_to_breadcrumb(
                function_application_pairs)
            self._session._push_breadcrumb(breadcrumb=breadcrumb)
            items = []
            items.append('transpose')
            items.append('invert')
            items.append('multiply')
            selector = iotools.Selector(
                session=self._session,
                items=items,
                )
            selector.explicit_breadcrumb = self._get_explicit_breadcrumb(
                function_application_pairs)
            with self._backtracking:
                function_name = selector._run(clear=clear)
            if self._session._backtrack():
                break
            elif not function_name:
                self._session._pop_breadcrumb()
                continue
            function_arguments = self._get_function_arguments(function_name)
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
