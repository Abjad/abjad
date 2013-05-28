import os
from experimental.tools.scoremanagertools.proxies.BasicModuleProxy import BasicModuleProxy


class OutputMaterialModuleProxy(BasicModuleProxy):
    '''Output material module proxy:

    ::

        >>> proxy = scoremanagertools.proxies.OutputMaterialModuleProxy(
        ...     'experimental.tools.scoremanagertools.built_in_materials.red_numbers.output_material')
        >>> proxy
        OutputMaterialModuleProxy('.../built_in_materials/red_numbers/output_material.py')

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
        return super(type(self), self).file_sections

    @property
    def filesystem_basename(self):
        '''Output material module proxy filesystem basename:

        ::

            >>> proxy.filesystem_basename
            'output_material.py'

        Return string.
        '''
        return super(type(self), self).filesystem_basename

    @property
    def filesystem_directory_name(self):
        '''Output material module proxy filesystem directory_name:

        ::

            >>> proxy.filesystem_directory_name
            '.../built_in_materials/red_numbers'

        Return string.
        '''
        return super(type(self), self).filesystem_directory_name

    @property
    def filesystem_path(self):
        '''Output material module proxy filesystem path:

        ::

            >>> proxy.filesystem_path
            '.../built_in_materials/red_numbers/output_material.py'

        Return string.
        '''
        return super(type(self), self).filesystem_path

    @property
    def material_package_name(self):
        '''Output material module proxy material package name:

        ::

            >>> proxy.material_package_name
            'red_numbers'

        Return string.
        '''
        return super(type(self), self).material_package_name

    @property
    def material_package_path(self):
        '''Output material module proxy material package path:

        ::

            >>> proxy.material_package_path
            'experimental.tools.scoremanagertools.built_in_materials.red_numbers'

        Return string.
        '''
        return super(type(self), self).material_package_path

    @property
    def module_name(self):
        '''Output material module proxy module name:

        ::

            >>> proxy.module_name
            'output_material'

        Return string.
        '''
        return super(type(self), self).module_name

    @property
    def module_path(self):
        '''Output material module proxy module path:

        ::

            >>> proxy.module_path
            'experimental.tools.scoremanagertools.built_in_materials.red_numbers.output_material'

        Return string.
        '''
        return super(type(self), self).module_path

    @property
    def package_path(self):
        '''Output material package proxy package path:

        ::

            >>> proxy.package_path
            'experimental.tools.scoremanagertools.built_in_materials.red_numbers.output_material'

        Return string.
        '''
        return super(type(self), self).package_path

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

#    def remove(self):
#        from experimental.tools import scoremanagertools
#        parent_package_initializer_file_proxy = scoremanagertools.proxies.InitializerFileProxy(
#            self.parent_package_initializer_file_name)
#        parent_package_initializer_file_proxy.remove_safe_import_statement(
#            'output_material', self.material_package_name)
#        grandparent_package_initializer = scoremanagertools.proxies.InitializerFileProxy(
#            self.grandparent_package_initializer_file_name)
#        grandparent_package_initializer.remove_safe_import_statement(
#            self.material_package_name, self.material_package_name)
#        BasicModuleProxy.remove(self)
