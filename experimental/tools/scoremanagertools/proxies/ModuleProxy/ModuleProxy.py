import os
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject
from experimental.tools.scoremanagertools.menuing.UserInputGetter import UserInputGetter
from experimental.tools.scoremanagertools.proxies.ImportableAssetProxy import ImportableAssetProxy
from experimental.tools.scoremanagertools.proxies.ParsableFileProxy import ParsableFileProxy


#class ModuleProxy(ParsableFileProxy, ImportableAssetProxy):
class ModuleProxy(ParsableFileProxy, ImportableAssetProxy, ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, module_importable_name=None, session=None):
        ScoreManagerObject.__init__(self, session=session)
        module_importable_name = self.strip_py_extension(module_importable_name)
        path = self.module_importable_name_to_path(module_importable_name)
        ParsableFileProxy.__init__(self, path=path, session=self.session)
        ImportableAssetProxy.__init__(self, asset_full_name=path, session=self.session)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return ImportableAssetProxy.__repr__(self)

    ### CLASS ATTRIBUTES ###

    extension = '.py'
    generic_class_name = 'module'
    temporary_asset_short_name = 'temporary_module.py'

    ### READ-ONLY PROPERTIES ###

    @property
    def grandparent_package_directory_path(self):
        if self.module_importable_name:
            return self.package_importable_name_to_package_directory_path(self.grandparent_package_importable_name)

    @property
    def grandparent_package_importable_name(self):
        if self.module_importable_name:
            return self.dot_join(self.module_importable_name.split('.')[:-2])

    @property
    def grandparent_package_initializer_file_name(self):
        if self.module_importable_name:
            return os.path.join(self.grandparent_package_directory_path, '__init__.py')

    @property
    def human_readable_name(self):
        return self.change_string_to_human_readable_string(
            self.short_name_without_extension)

    @property
    def module_importable_name(self):
        return self.importable_name

    @property
    def module_short_name(self):
        if self.module_importable_name:
            return self.module_importable_name.split('.')[-1]

    @property
    def parent_package_directory_path(self):
        if self.module_importable_name:
            return self.package_importable_name_to_package_directory_path(self.parent_package_importable_name)

    @property
    def parent_package_importable_name(self):
        if self.module_importable_name:
            return self.dot_join(self.module_importable_name.split('.')[:-1])

    @property
    def parent_package_initializer_file_name(self):
        if self.module_importable_name:
            return os.path.join(self.parent_package_directory_path, '__init__.py')

    ### PUBLIC METHODS ###

    def human_readable_name_to_asset_short_name(self, human_readable_name):
        asset_short_name = ParsableFileProxy.human_readable_name_to_asset_short_name(
            self, human_readable_name)
        asset_short_name += '.py'
        return asset_short_name

    def run_abjad(self, prompt=True):
        os.system('abjad {}'.format(self.path))
        self.proceed('file executed', is_interactive=prompt)

    def run_python(self, prompt=True):
        os.system('python {}'.format(self.path))
        self.proceed('file executed.', is_interactive=prompt)

    def unimport(self):
        self.remove_package_importable_name_from_sys_modules(self.module_importable_name)
