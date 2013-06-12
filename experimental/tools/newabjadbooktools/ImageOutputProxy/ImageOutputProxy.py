import os
from experimental.tools.newabjadbooktools.AssetOutputProxy import AssetOutputProxy


class ImageOutputProxy(AssetOutputProxy):

    def get_absolute_asset_output_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_name,
            self.get_image_file_name(document_handler),
            )

    def get_image_file_name(self, document_handler):
        return '{}.{}'.format(
            self.file_name_without_extension,
            document_handler.image_format.file_extension,
            )

    def get_relative_asset_output_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_name,
            self.get_image_file_name(document_handler),
            )

