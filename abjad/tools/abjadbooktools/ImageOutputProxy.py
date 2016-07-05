# -*- coding: utf-8 -*-
from __future__ import print_function
import abc
import hashlib
import os
from abjad.tools import abctools


class ImageOutputProxy(abctools.AbjadValueObject):
    r'''Abstract base class for image output proxies.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_image_layout_specifier',
        '_image_render_specifier',
        '_payload',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        image_layout_specifier=None,
        image_render_specifier=None,
        ):
        self._image_layout_specifier = image_layout_specifier
        self._image_render_specifier = image_render_specifier

    ### PRIVATE METHODS ###

    def _include_graphics(
        self,
        latex_configuration,
        options,
        page_number,
        relative_file_path,
        ):
        result = []
        if page_number:
            page_number = 'page={}'.format(page_number)
            if not options:
                options = page_number
            else:
                options = options.strip()
                if not options.endswith(','):
                    options += ', '
                options += page_number
        if options:
            string = '\\noindent\\includegraphics[{}]{{{}}}'.format(
                options,
                relative_file_path,
                )
        else:
            string = '\\noindent\\includegraphics{{{}}}'.format(
                relative_file_path,
                )
        before = latex_configuration.get('before-includegraphics', ())
        after = latex_configuration.get('after-includegraphics', ())
        result.extend(before)
        result.append(string)
        result.extend(after)
        return result

    def _render_pdf_source(
        self,
        temporary_directory_path,
        ):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def as_latex(
        self,
        configuration=None,
        output_directory=None,
        relative_output_directory=None,
        ):
        r'''Creates a LaTeX representation of the image output proxy.
        '''
        import PyPDF2
        configuration = configuration or {}
        latex_configuration = configuration.get('latex', {})
        options_key = '{}-options'.format(self.file_name_prefix)
        options = latex_configuration.get(options_key, ())
        options = ''.join(options)
        file_extension = '.pdf'
        file_name = self.file_name_without_extension + file_extension
        output_directory = output_directory or relative_output_directory
        absolute_file_path = os.path.join(
            output_directory,
            file_name,
            )
        relative_file_path = os.path.join(
            relative_output_directory,
            file_name,
            )
        # Windows hack for test suite.
        relative_file_path = relative_file_path.replace(os.path.sep, '/')
        page_count = 1
        if os.path.exists(absolute_file_path):
            with open(absolute_file_path, 'rb') as file_pointer:
                pdf_reader = PyPDF2.PdfFileReader(file_pointer)
                page_count = pdf_reader.getNumPages()
        result = []
        if page_count == 1:
            result.extend(self._include_graphics(
                latex_configuration,
                options,
                None,
                relative_file_path,
                ))
        else:
            result.extend(self._include_graphics(
                latex_configuration,
                options,
                1,
                relative_file_path,
                ))
            for page_number in range(2, page_count + 1):
                result.append(r'\newline')
                result.append(r'\newline')
                result.extend(self._include_graphics(
                    latex_configuration,
                    options,
                    page_number,
                    relative_file_path,
                    ))
        return result

    def render_for_latex(
        self,
        absolute_output_directory,
        ):
        r'''Renders the image output proxy payload for LaTeX inclusion.
        '''
        target_pdf_path = os.path.join(
            absolute_output_directory,
            self.file_name_without_extension + '.pdf',
            )
        if os.path.exists(target_pdf_path):
            return
        self._render_pdf_source(absolute_output_directory)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def file_name_prefix(self):
        r'''Gets image output proxy file name prefix.

        Returns string.
        '''
        raise NotImplementedError

    @property
    def file_name_without_extension(self):
        r'''Gets image output proxy filename without file extension.

        Returns string.
        '''
        payload = '\n'.join(format(self.payload))
        md5 = hashlib.md5(payload.encode()).hexdigest()
        return '-'.join((self.file_name_prefix, md5))

    @property
    def image_layout_specifier(self):
        r'''Gets image specifier.
        '''
        return self._image_layout_specifier

    @property
    def image_render_specifier(self):
        r'''Gets image specifier.
        '''
        return self._image_render_specifier

    @property
    def payload(self):
        r'''Gets images output proxy payload.

        Returns string.
        '''
        return self._payload
