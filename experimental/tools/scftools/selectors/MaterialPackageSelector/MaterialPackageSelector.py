from experimental.tools.scftools.selectors.Selector import Selector
import os


class MaterialPackageSelector(Selector):

	### CLASS ATTRIBUTES ###

    asset_subtree_package_importable_names = []
    target_human_readable_name = 'material package'

    ### PUBLIC METHODS ###

    def list_current_material_package_path_names(self):
        result = []
        for package_path_name in self.list_public_package_path_names_in_subtree(
            self.session.current_materials_package_path_name):
            if self.get_tag_from_path_name(package_path_name, 'generic_output_name') == \
                self.generic_output_name:
                result.append(package_path_name)
        return result

    def list_items(self):
        result = []
        for path_name in self.list_current_material_package_path_names():
            package_importable_name = self.path_name_to_package_importable_name(path_name)
            result.append(package_importable_name)
        return result
