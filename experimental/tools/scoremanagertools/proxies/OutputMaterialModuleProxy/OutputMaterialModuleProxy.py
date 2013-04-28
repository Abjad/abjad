import os
from experimental.tools.scoremanagertools.proxies.BasicModuleProxy import BasicModuleProxy
from experimental.tools.scoremanagertools.helpers import safe_import


class OutputMaterialModuleProxy(BasicModuleProxy):

    ### PUBLIC METHODS ###

    def display_output_material(self):
        output_material = self.import_output_material_safely()
        self.display([repr(output_material), ''], capitalize_first_character=False)
        self.session.hide_next_redraw = True

    def import_output_material(self):
        # the next two lines actually matter
        self.unimport_materials_package()
        self.unimport_material_package()
        #self.unimport()
        if os.path.exists(self.file_path):
            file_pointer = open(self.file_path, 'r')
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

    def remove(self):
        from experimental.tools import scoremanagertools
        parent_package_initializer_file_proxy = scoremanagertools.proxies.InitializerFileProxy(
            self.parent_package_initializer_file_name)
        parent_package_initializer_file_proxy.remove_safe_import_statement(
            'output_material', self.material_package_name)
        grandparent_package_initializer = scoremanagertools.proxies.InitializerFileProxy(
            self.grandparent_package_initializer_file_name)
        grandparent_package_initializer.remove_safe_import_statement(
            self.material_package_name, self.material_package_name)
        BasicModuleProxy.remove(self)
