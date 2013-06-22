import abc
import os
from experimental.tools.newabjadbooktools.AssetOutputProxy import AssetOutputProxy


class ImageOutputProxy(AssetOutputProxy):
    '''Abstract base class of output proxies which represent images.
    '''

    ### PUBLIC METHODS ###

    def get_asset_output_absolute_file_path(self, document_handler):
        return os.path.join(
            document_handler.output_directory_path,
            document_handler.asset_output_directory_name,
            self.get_image_file_name(document_handler),
            )

    def get_asset_output_relative_file_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_name,
            self.get_image_file_name(document_handler),
            )

    def get_image_file_name(self, document_handler):
        return '{}.{}'.format(
            self.file_name_without_extension,
            document_handler.image_format.file_extension,
            )

    @abc.abstractmethod
    def handle_html_document_environment(self, document_handler):
        result = []
        directive = '<img alt="" src="{}"/>'.format(
            self.get_asset_output_relative_file_path(document_handler))
        result.append(directive)
        return result

    @abc.abstractmethod
    def handle_latex_document_environment(self, document_handler):
        result = []
        directive = '\\includegraphics{{{}}}'.format(
            self.get_asset_output_relative_file_path(document_handler))
        result.append(directive)
        return result

    @abc.abstractmethod
    def handle_rest_document_environment(self, document_handler):
        result = []
        directive = '.. image:: {}'.format(
            self.get_asset_output_relative_file_path(document_handler))
        result.append(directive)
        return result

