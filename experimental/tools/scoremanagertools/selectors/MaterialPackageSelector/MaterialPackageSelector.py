from experimental.tools.scoremanagertools.selectors.Selector import Selector
import os


class MaterialPackageSelector(Selector):

	### CLASS ATTRIBUTES ###

    asset_subtree_package_importable_names = []
    target_human_readable_name = 'material package'

    ### PUBLIC METHODS ###

    def list_current_material_package_directory_paths(self):
        result = []
        for package_directory_path in self.list_public_package_directory_paths_in_subtree(
            self.session.current_materials_package_directory_path):
            if self.get_tag_from_path(package_directory_path, 'generic_output_name') == \
                self.generic_output_name:
                result.append(package_directory_path)
        return result

    def list_items(self):
        result = []
        for path in self.list_current_material_package_directory_paths():
            package_importable_name = self.path_to_package_importable_name(path)
            result.append(package_importable_name)
        return result
