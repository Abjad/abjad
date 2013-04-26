import os
from experimental.tools.scoremanagertools.wranglers.AssetWrangler import AssetWrangler


class ImportableAssetWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def temporary_asset_package_importable_name(self):
        if self.current_asset_container_package_importable_name:
            return self.dot_join([
                self.current_asset_container_package_importable_name,
                self.temporary_asset_short_name])
        else:
            return self.temporary_asset_short_name

    ### PUBLIC METHODS ###

    def list_asset_package_importable_names(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_package_importable_names(head=head))
        result.extend(self.list_score_internal_asset_package_importable_names(head=head))
        result.extend(self.list_user_asset_package_importable_names(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for package_importable_name in self.list_asset_package_importable_names(head=head):
            asset_proxy = self.get_asset_proxy(package_importable_name)
            result.append(asset_proxy)
        return result

    def list_score_external_asset_package_importable_names(self, head=None):
        result = []
        for path in self.list_score_external_asset_container_paths(head=head):
            for name in os.listdir(path):
                package_importable_name = self.path_to_package_importable_name(path)
                if name[0].isalpha():
                    result.append(self.dot_join([package_importable_name, name]))
        return result

    def list_score_internal_asset_package_importable_names(self, head=None):
        result = []
        for asset_container_package_importable_name in \
            self.list_score_internal_asset_container_package_importable_names(head=head):
            if self.score_internal_asset_container_package_importable_name_infix:
                asset_path = self.package_importable_name_to_directory_path(
                    asset_container_package_importable_name)
                for name in os.listdir(asset_path):
                    if name[0].isalpha():
                        importable_base_name = self.strip_extension_from_base_name(name)
                        result.append('{}.{}'.format(
                            asset_container_package_importable_name, importable_base_name))
            else:
                result.append(asset_container_package_importable_name)
        return result

    def list_user_asset_package_importable_names(self, head=None):
        result = []
        for path in self.list_user_asset_container_paths(head=head):
            for name in os.listdir(path):
                if name[0].isalpha():
                    result.append(self.dot_join([self.configuration.user_makers_package_importable_name, name]))
        return result

    # TODO: try to reimplement without proxy instantiation
    def list_visible_asset_package_importable_names(self, head=None):
        result = []
        for asset_proxy in self.list_visible_asset_proxies(head=head):
            result.append(asset_proxy.package_importable_name)
        return result

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_package_importable_names(head=head)
        bodies = self.list_visible_asset_human_readable_names(head=head)
        return zip(keys, bodies)
