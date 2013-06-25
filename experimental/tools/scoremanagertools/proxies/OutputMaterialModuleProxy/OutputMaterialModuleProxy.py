import os
from experimental.tools.scoremanagertools.proxies.ModuleProxy \
    import ModuleProxy
from experimental.tools.scoremanagertools.proxies.ParseableModuleMixin \
    import ParseableModuleMixin


class OutputMaterialModuleProxy(ModuleProxy, ParseableModuleMixin):
    '''Output material module proxy:

    ::

        >>> proxy = scoremanagertools.proxies.OutputMaterialModuleProxy(
        ...     'experimental.tools.scoremanagertools.materialpackages.red_numbers.output_material')
        >>> proxy
        OutputMaterialModuleProxy('.../materialpackages/red_numbers/output_material.py')

    Return output material module proxy.
    '''

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        ModuleProxy.__init__(self, packagesystem_path=packagesystem_path, session=session)
        ParseableModuleMixin.__init__(self)

    ### PUBLIC PROPERTIES ###

    @property
    def filesystem_basename(self):
        '''Output material module proxy filesystem basename:

        ::

            >>> proxy.filesystem_basename
            'output_material.py'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).filesystem_basename

    @property
    def filesystem_path(self):
        '''Output material module proxy filesystem path:

        ::

            >>> proxy.filesystem_path
            '.../materialpackages/red_numbers/output_material.py'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).filesystem_path

    @property
    def material_package_name(self):
        return self.packagesystem_path.split('.')[-2]

    @property
    def packagesystem_basename(self):
        '''Output material module proxy module name:

        ::

            >>> proxy.packagesystem_basename
            'output_material'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).packagesystem_basename

    @property
    def packagesystem_path(self):
        '''Output material module proxy module path:

        ::

            >>> proxy.packagesystem_path
            'experimental.tools.scoremanagertools.materialpackages.red_numbers.output_material'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).packagesystem_path

    @property
    def parent_directory_filesystem_path(self):
        '''Output material module proxy filesystem directory_name:

        ::

            >>> proxy.parent_directory_filesystem_path
            '.../materialpackages/red_numbers'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).parent_directory_filesystem_path

    ### PUBLIC METHODS ###

    def display_output_material(self):
        output_material = self.import_output_material_safely()
        self._io.display([repr(output_material), ''], capitalize_first_character=False)
        self.session.hide_next_redraw = True

    def import_output_material(self):
        # the next two lines actually matter
        self.unimport_materials_package()
        self.unimport_material_package()
        #self.unimport()
        if os.path.exists(self.filesystem_path):
            file_pointer = open(self.filesystem_path, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            exec(file_contents_string)
            material_package_name = self.packagesystem_path.split('.')[-2]
            result = locals().get(material_package_name)
            return result

    def import_output_material_safely(self):
        try:
            return self.import_output_material()
        except:
            pass

    def unimport_material_package(self):
        self.remove_package_path_from_sys_modules(
            self.parent_directory_packagesystem_path)

    def unimport_materials_package(self):
        self.remove_package_path_from_sys_modules(
            self.session.current_materials_package_path)
