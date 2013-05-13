import os
import sys
from abjad.tools import stringtools
from experimental.tools import packagepathtools
from experimental.tools.scoremanagertools.proxies.ParsableFileProxy import ParsableFileProxy


class ModuleProxy(ParsableFileProxy):

    ### INITIALIZER ###

    def __init__(self, module_path=None, session=None):
        self._module_path = module_path
        filesystem_path = packagepathtools.module_path_to_file_path(self.module_path, self.configuration)
        ParsableFileProxy.__init__(self, filesystem_path=filesystem_path, session=session)

    ### CLASS ATTRIBUTES ###

    extension = '.py'
    _generic_class_name = 'module'
    _temporary_asset_name = 'temporary_module.py'

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _space_delimited_lowercase_name(self):
        return stringtools.string_to_space_delimited_lowercase(self.name_without_extension)

    ### PRIVATE METHODS ###

    def _space_delimited_lowercase_name_to_asset_name(self, space_delimited_lowercase_name):
        asset_name = ParsableFileProxy._space_delimited_lowercase_name_to_asset_name(
            self, space_delimited_lowercase_name)
        asset_name += '.py'
        return asset_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def filesystem_directory_name(self):
        if self.module_path:
            return packagepathtools.package_path_to_directory_path(
                self.parent_package_path)

    @property
    def grandparent_directory_path(self):
        if self.module_path:
            return packagepathtools.package_path_to_directory_path(
                self.grandparent_package_path)

    @property
    def grandparent_package_initializer_file_name(self):
        if self.module_path:
            return os.path.join(self.grandparent_directory_path, '__init__.py')

    @property
    def grandparent_package_path(self):
        if self.module_path:
            return '.'.join(self.module_path.split('.')[:-2])

    @property
    def module_name(self):
        if self.module_path:
            return self.module_path.split('.')[-1]

    # TODO: remove and use only self.package_path instead
    @property
    def module_path(self):
        return self._module_path

    @property
    def package_path(self):
        return self.module_path

    @property
    def parent_package_initializer_file_name(self):
        if self.module_path:
            return os.path.join(self.filesystem_directory_name, '__init__.py')

    @property
    def parent_package_path(self):
        if self.module_path:
            return '.'.join(self.module_path.split('.')[:-1])

    ### PUBLIC METHODS ###

    # TODO: remove entirely
    def remove_package_path_from_sys_modules(self, package_path):
        '''Total hack. Should be eliminated entirely.
        '''
        command = "if '{}' in sys.modules: del(sys.modules['{}'])".format(
            package_path, package_path)
        exec(command)

    def run_abjad(self, prompt=True):
        os.system('abjad {}'.format(self.filesystem_path))
        self._io.proceed('file executed', is_interactive=prompt)

    def run_python(self, prompt=True):
        os.system('python {}'.format(self.filesystem_path))
        self._io.proceed('file executed.', is_interactive=prompt)

    # TODO: remove entirely
    def unimport(self):
        self.remove_package_path_from_sys_modules(self.module_path)
