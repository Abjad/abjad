from experimental.tools.scoremanagertools.selectors.Selector import Selector
import os


class MaterialPackageSelector(Selector):

	### CLASS ATTRIBUTES ###

    asset_subtree_package_importable_names = []
    target_human_readable_name = 'material package'

    ### PUBLIC METHODS ###

    def list_current_material_directory_paths(self):
        result = []
        for directory_path in self.list_public_directory_paths_with_initializers_in_subtree(
            self.session.current_materials_directory_path):
            if self.get_tag_from_path(directory_path, 'generic_output_name') == \
                self.generic_output_name:
                result.append(directory_path)
        return result

    def list_items(self):
        result = []
        for path in self.list_current_material_directory_paths():
            package_importable_name = self.path_to_package_importable_name(path)
            result.append(package_importable_name)
        return result
