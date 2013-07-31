# -*- encoding: utf-8 -*-
import os
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class MaterialPackageSelector(Selector):

	### CLASS VARIABLES ###

    asset_subtree_package_paths = []

    space_delimited_lowercase_target_name = 'material package'

    ### PUBLIC METHODS ###

    def list_current_material_directory_paths(self):
        result = []
        for directory_path in \
            self.list_public_directory_paths_with_initializers_in_subtree(
            self.session.current_materials_directory_path):
            if self.get_tag_from_directory_path(
                directory_path, 'generic_output_name') == \
                self.generic_output_name:
                result.append(directory_path)
        return result

    def list_items(self):
        result = []
        for directory_path in self.list_current_material_directory_paths():
            package_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                    directory_path)
            result.append(package_path)
        return result

    def list_public_directory_paths_in_subtree(self, subtree_path):
        result = []
        for subtree_path, directory_names, file_names in os.walk(subtree_path):
            if '.svn' not in subtree_path:
                for directory_name in directory_names:
                    if '.svn' not in directory_name:
                        if directory_name[0].isalpha():
                            result.append(
                                os.path.join(subtree_path, directory_name))
        return result

    def list_public_directory_paths_with_initializers_in_subtree(
        self, subtree_path):
        result = []
        for directory_path in \
            self.list_public_directory_paths_in_subtree(subtree_path):
            if '__init__.py' in os.listdir(directory_path):
                result.append(directory_path)
        return result
