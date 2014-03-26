# -*- encoding: utf-8 -*-
from scoremanager.wizards.Wizard import Wizard
from scoremanager import iotools


class ReservoirStartHelperCreationWizard(Wizard):
    r'''Reservoir start helper creation wizard.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'reservoir start helpers creation wizard'

    ### PRIVATE METHODS ###

    def _get_function_arguments(self, function_name):
        arguments = []
        if function_name in ('start at index n'):
            getter = self._io_manager.make_getter(where=self._where)
            getter.append_integer('index')
            result = getter._run()
            if self._should_exit_io_method():
                return
            arguments.append(result)
        return tuple(arguments)

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(self)
        with context:
            while True:
                function_application_pairs = []
                items = []
                items.append('start at index 0')
                items.append('start at index n')
                items.append('start at next unused index')
                selector = iotools.Selector(
                    session=self._session,
                    items=items,
                    )
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
                break
            self.target = function_application_pairs
            return self.target