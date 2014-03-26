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
            if self._should_exit_io_method():
                return
            arguments.append(result)
        return tuple(arguments)

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        function_application_pairs = []
        context = iotools.ControllerContext(self)
        with context:
            while True:
                breadcrumb = self._function_application_pairs_to_breadcrumb(
                    function_application_pairs)
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
                with self._backtrack:
                    function_name = selector._run()
                if self._should_exit_io_method():
                    break
                elif not function_name:
                    continue
                function_arguments = self._get_function_arguments(
                    function_name)
                if self._should_exit_io_method():
                    break
                elif function_arguments is None:
                    continue
                function_application_pairs.append(
                    (function_name, function_arguments))
            self.target = function_application_pairs
            return self.target