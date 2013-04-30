import os
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject
from experimental.tools.scoremanagertools.menuing.UserInputGetter import UserInputGetter
from experimental.tools.scoremanagertools.proxies.AssetProxy import AssetProxy
#from experimental.tools.scoremanagertools.proxies.ImportableAssetProxy import ImportableAssetProxy
from experimental.tools.scoremanagertools.proxies.ParsableFileProxy import ParsableFileProxy


#class ModuleProxy(ParsableFileProxy, ImportableAssetProxy):
#class ModuleProxy(ParsableFileProxy, ImportableAssetProxy, ScoreManagerObject):
class ModuleProxy(ParsableFileProxy, AssetProxy, ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, module_path=None, session=None):
        ScoreManagerObject.__init__(self, session=session)
        module_path = self.strip_py_extension(module_path)
        file_path = self.module_path_to_file_path(module_path)
        ParsableFileProxy.__init__(self, file_path=file_path, session=self.session)
        #ImportableAssetProxy.__init__(self, asset_path=file_path, session=self.session)
        AssetProxy.__init__(self, asset_path=file_path, session=self.session)
        self._module_path = module_path

    ### SPECIAL METHODS ###

    def __repr__(self):
        #return ImportableAssetProxy.__repr__(self)
        return AssetProxy.__repr__(self)

    ### CLASS ATTRIBUTES ###

    extension = '.py'
    generic_class_name = 'module'
    temporary_asset_name = 'temporary_module.py'

    ### READ-ONLY PROPERTIES ###

    @property
    def grandparent_directory_path(self):
        if self.module_path:
            return self.package_path_to_directory_path(self.grandparent_package_path)

    @property
    def grandparent_package_initializer_file_name(self):
        if self.module_path:
            return os.path.join(self.grandparent_directory_path, '__init__.py')

    @property
    def grandparent_package_path(self):
        if self.module_path:
            return self.dot_join(self.module_path.split('.')[:-2])

    @property
    def human_readable_name(self):
        return stringtools.string_to_space_delimited_lowercase(self.name_without_extension)

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
            return self.package_path_to_directory_path(self.parent_package_path)

    @property
    def parent_package_initializer_file_name(self):
        if self.module_path:
            return os.path.join(self.parent_directory_path, '__init__.py')

    @property
    def parent_package_path(self):
        if self.module_path:
            return self.dot_join(self.module_path.split('.')[:-1])

    ### PUBLIC METHODS ###

    def human_readable_name_to_asset_name(self, human_readable_name):
        asset_name = ParsableFileProxy.human_readable_name_to_asset_name(
            self, human_readable_name)
        asset_name += '.py'
        return asset_name

    def run_abjad(self, prompt=True):
        os.system('abjad {}'.format(self.file_path))
        self.proceed('file executed', is_interactive=prompt)

    def run_python(self, prompt=True):
        os.system('python {}'.format(self.file_path))
        self.proceed('file executed.', is_interactive=prompt)

    def unimport(self):
        self.remove_package_path_from_sys_modules(self.module_path)
