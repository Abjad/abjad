from experimental.tools.scoremanagertools.proxies.ModuleProxy import ModuleProxy


class MaterialModuleProxy(ModuleProxy):

    ### READ-ONLY PROPERTIES ###

    @property
    def material_package_path(self):
        return self.parent_package_path

    @property
    def material_spaced_name(self):
        return self.material_package_name.replace('_', ' ')

    @property
    def material_package_name(self):
        return self.module_path.split('.')[-2]

    ### PUBLIC METHODS ###

    def unimport_material_package(self):
        self.remove_package_path_from_sys_modules(self.material_package_path)

    def unimport_materials_package(self):
        self.remove_package_path_from_sys_modules(
            self.session.current_materials_package_path)
