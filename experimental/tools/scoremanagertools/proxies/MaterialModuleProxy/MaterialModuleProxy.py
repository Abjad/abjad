from experimental.tools.scoremanagertools.proxies.ModuleProxy import ModuleProxy


class MaterialModuleProxy(ModuleProxy):

    ### INITIALIZER ###
    
    def __init__(self, packagesystem_path=None, session=None):
        ModuleProxy.__init__(self, packagesystem_path=packagesystem_path, session=session)
