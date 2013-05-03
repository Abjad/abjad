import os
from abjad.tools import stringtools
from experimental.tools import packagepathtools
from experimental.tools.scoremanagertools.proxies.ParsableFileProxy import ParsableFileProxy


class ModuleProxy(ParsableFileProxy):

    ### INITIALIZER ###

    def __init__(self, module_path=None, session=None):
        self._module_path = module_path
        file_path = packagepathtools.module_path_to_file_path(self.module_path, self.configuration)
        ParsableFileProxy.__init__(self, file_path=file_path, session=session)

    ### CLASS ATTRIBUTES ###

    extension = '.py'
    generic_class_name = 'module'
    temporary_asset_name = 'temporary_module.py'

    ### READ-ONLY PROPERTIES ###

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

    @property
    def module_path(self):
        return self._module_path

    @property
    def parent_directory_path(self):
        if self.module_path:
            return packagepathtools.package_path_to_directory_path(
                self.parent_package_path)

    @property
    def parent_package_initializer_file_name(self):
        if self.module_path:
            return os.path.join(self.parent_directory_path, '__init__.py')

    @property
    def parent_package_path(self):
        if self.module_path:
            return '.'.join(self.module_path.split('.')[:-1])

    @property
    def space_delimited_lowercase_name(self):
        return stringtools.string_to_space_delimited_lowercase(self.name_without_extension)

    ### PUBLIC METHODS ###

    def run_abjad(self, prompt=True):
        os.system('abjad {}'.format(self.file_path))
        self.io.proceed('file executed', is_interactive=prompt)

    def run_python(self, prompt=True):
        os.system('python {}'.format(self.file_path))
        self.io.proceed('file executed.', is_interactive=prompt)

    def space_delimited_lowercase_name_to_asset_name(self, space_delimited_lowercase_name):
        asset_name = ParsableFileProxy.space_delimited_lowercase_name_to_asset_name(
            self, space_delimited_lowercase_name)
        asset_name += '.py'
        return asset_name

    def unimport(self):
        self.remove_package_path_from_sys_modules(self.module_path)
