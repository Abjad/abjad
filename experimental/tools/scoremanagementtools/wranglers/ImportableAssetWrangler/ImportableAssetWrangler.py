from experimental.tools.scoremanagementtools.wranglers.AssetWrangler import AssetWrangler
import os


class ImportableAssetWrangler(AssetWrangler):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def temporary_asset_importable_name(self):
        if self.current_asset_container_importable_name:
            return self.dot_join([
                self.current_asset_container_importable_name,
                self.temporary_asset_short_name])
        else:
            return self.temporary_asset_short_name

    ### PUBLIC METHODS ###

    def list_asset_importable_names(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_importable_names(head=head))
        result.extend(self.list_score_internal_asset_importable_names(head=head))
        result.extend(self.list_user_asset_importable_names(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for package_importable_name in self.list_asset_importable_names(head=head):
            asset_proxy = self.get_asset_proxy(package_importable_name)
            result.append(asset_proxy)
        return result

    def list_score_external_asset_importable_names(self, head=None):
        result = []
        for path_name in self.list_score_external_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                importable_name = self.path_name_to_package_importable_name(path_name)
                if name[0].isalpha():
                    result.append(self.dot_join([importable_name, name]))
        return result

    def list_score_internal_asset_importable_names(self, head=None):
        result = []
        for asset_container_importable_name in \
            self.list_score_internal_asset_container_importable_names(head=head):
            if self.score_internal_asset_container_importable_name_infix:
                asset_path_name = self.package_importable_name_to_path_name(
                    asset_container_importable_name)
                for name in os.listdir(asset_path_name):
                    if name[0].isalpha():
                        importable_base_name = self.strip_extension_from_base_name(name)
                        result.append('{}.{}'.format(
                            asset_container_importable_name, importable_base_name))
            else:
                result.append(asset_container_importable_name)
        return result

    def list_user_asset_importable_names(self, head=None):
        result = []
        for path_name in self.list_user_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                if name[0].isalpha():
                    result.append(self.dot_join([self.user_makers_package_importable_name, name]))
        return result

    # TODO: try to reimplement without proxy instantiation
    def list_visible_asset_importable_names(self, head=None):
        result = []
        for asset_proxy in self.list_visible_asset_proxies(head=head):
            result.append(asset_proxy.importable_name)
        return result

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_importable_names(head=head)
        bodies = self.list_visible_asset_human_readable_names(head=head)
        return zip(keys, bodies)
