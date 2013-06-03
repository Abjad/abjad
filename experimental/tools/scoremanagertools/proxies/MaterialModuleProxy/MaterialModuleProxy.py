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
    def space_delimited_material_package_name(self):
        material_package_name = self.packagesystem_path.split('.')[-2]
        return material_package_name.replace('_', ' ')
