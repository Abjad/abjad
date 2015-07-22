# -*- encoding: utf-8 -*-
from __future__ import print_function
import abc
import hashlib
import os
from abjad.tools import abctools


class ImageOutputProxy(abctools.AbjadValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        )

    ### PRIVATE METHODS ###

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

    def render_for_latex(
        self,
        absolute_output_directory,
        ):
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
        raise NotImplementedError

    @property
    def payload(self):
        return self._payload

    @property
    def file_name_without_extension(self):
        payload = '\n'.join(format(self.payload))
        md5 = hashlib.md5(payload.encode()).hexdigest()
        return '-'.join((self.file_name_prefix, md5))