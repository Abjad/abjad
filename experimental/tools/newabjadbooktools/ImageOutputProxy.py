# -*- encoding: utf-8 -*-
import abc
import os
from experimental.tools.newabjadbooktools.AssetOutputProxy \
    import AssetOutputProxy


class ImageOutputProxy(AssetOutputProxy):
    r'''Abstract base class of output proxies which represent images.
    '''

    ### PUBLIC METHODS ###

    def get_asset_output_absolute_file_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_path,
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

    def handle_pdf_image_format(self, document_handler):
        pass

    def handle_png_image_format(self, document_handler):
        pass

    @abc.abstractmethod
    def handle_rest_document_environment(self, document_handler):
        result = []
        directive = '.. image:: {}'.format(
            self.get_asset_output_relative_file_path(document_handler))
        result.append(directive)
        return result

    def handle_svg_image_format(self, document_handler):
        pass

    def write_asset_to_disk(self, document_handler):
        from experimental.tools import newabjadbooktools
        image_format = document_handler.image_format
        image_formats = {
            newabjadbooktools.PDFImageFormat: self.handle_pdf_image_format,
            newabjadbooktools.PNGImageFormat: self.handle_png_image_format,
            newabjadbooktools.SVGImageFormat: self.handle_svg_image_format,
        }
        if image_format in image_formats:
            image_formats[image_format](document_handler)
        raise Exception('Unsupported image format {!r}'.format(image_format))
        
