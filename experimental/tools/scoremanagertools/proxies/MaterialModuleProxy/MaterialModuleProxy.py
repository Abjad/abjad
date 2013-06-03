from experimental.tools.scoremanagertools.proxies.ModuleProxy import ModuleProxy
from experimental.tools.scoremanagertools.proxies.ParseableFileMixin import ParseableFileMixin


class MaterialModuleProxy(ModuleProxy, ParseableFileMixin):

    ### INITIALIZER ###
    
    def __init__(self, packagesystem_path=None, session=None):
        ModuleProxy.__init__(self, packagesystem_path=packagesystem_path, session=session)
        ParseableFileMixin.__init__(self)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def material_package_name(self):
        return self.packagesystem_path.split('.')[-2]

    @property
    def material_package_path(self):
        return self.parent_directory_packagesystem_path

    @property
    def space_delimited_material_package_name(self):
        return self.material_package_name.replace('_', ' ')

    ### PUBLIC METHODS ###

    def unimport_material_package(self):
        self.remove_package_path_from_sys_modules(self.material_package_path)

    def unimport_materials_package(self):
        self.remove_package_path_from_sys_modules(
            self._session.current_materials_package_path)
