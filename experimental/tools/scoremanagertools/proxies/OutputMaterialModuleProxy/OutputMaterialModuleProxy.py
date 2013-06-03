import os
from experimental.tools.scoremanagertools.proxies.BasicModuleProxy import BasicModuleProxy


class OutputMaterialModuleProxy(BasicModuleProxy):
    '''Output material module proxy:

    ::

        >>> proxy = scoremanagertools.proxies.OutputMaterialModuleProxy(
        ...     'experimental.tools.scoremanagertools.materialpackages.red_numbers.output_material')
        >>> proxy
        OutputMaterialModuleProxy('.../materialpackages/red_numbers/output_material.py')

    Return output material module proxy.
    '''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def file_sections(self):
        '''Output material module proxy file sections:

        ::

            >>> for x in proxy.file_sections: x
            ... 
            ([], False, 0)
            ([], False, 1)
            ([], True, 2)
            (['red_numbers = [1, 2, 3, 4, 5]'], False, 0)
    
        Return tuple.
        '''
        return super(OutputMaterialModuleProxy, self).file_sections

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
    def parent_directory_filesystem_path(self):
        '''Output material module proxy filesystem directory_name:

        ::

            >>> proxy.parent_directory_filesystem_path
            '.../materialpackages/red_numbers'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).parent_directory_filesystem_path

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
        '''Output material module proxy material package name:

        ::

            >>> proxy.material_package_name
            'red_numbers'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).material_package_name

    @property
    def material_package_path(self):
        '''Output material module proxy material package path:

        ::

            >>> proxy.material_package_path
            'experimental.tools.scoremanagertools.materialpackages.red_numbers'

        Return string.
        '''
        return super(OutputMaterialModuleProxy, self).material_package_path

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

    ### PUBLIC METHODS ###

    def display_output_material(self):
        output_material = self.import_output_material_safely()
        self._io.display([repr(output_material), ''], capitalize_first_character=False)
        self._session.hide_next_redraw = True

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
            result = locals().get(self.material_package_name)
            return result

    def import_output_material_safely(self):
        try:
            return self.import_output_material()
        except:
            pass
