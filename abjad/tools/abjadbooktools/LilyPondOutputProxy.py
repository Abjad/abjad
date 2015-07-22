# -*- encoding: utf-8 -*-
import copy
import os
import subprocess
from abjad.tools import documentationtools
from abjad.tools import systemtools
from abjad.tools import lilypondfiletools
from abjad.tools.abjadbooktools.ImageOutputProxy import ImageOutputProxy


class LilyPondOutputProxy(ImageOutputProxy):
    r'''A LilyPond output proxy.

    ::

        >>> from abjad.tools import abjadbooktools
        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> proxy = abjadbooktools.LilyPondOutputProxy(staff)
        >>> print(format(proxy))
        abjadbooktools.tools.LilyPondOutputProxy(
            lilypondfiletools.LilyPondFile()
            )

    ::

        >>> print(proxy.as_latex(relative_output_directory='assets'))
        ['\\noindent\\includegraphics{assets/lilypond-627153107d80c2ead680f5295be4d2db.pdf}']

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        '_stylesheet',
        )

    ### INITIALIZER ###

    def __init__(self, payload, stylesheet=None):
        #from abjad import abjad_configuration
        payload = copy.deepcopy(payload)
        if stylesheet is None:
            payload = documentationtools.make_reference_manual_lilypond_file(
                payload)
        manager = systemtools.IOManager
        lilypond_file = manager._insert_expr_into_lilypond_file(payload)
        lilypond_file.file_initial_system_comments[:] = []
        token = lilypondfiletools.LilyPondVersionToken(
            "2.19.0",
            )
        lilypond_file.file_initial_system_includes[0] = token
        self._stylesheet = stylesheet
        if stylesheet:
            lilypond_file.use_relative_includes = True
            lilypond_file.file_initial_user_includes[:] = [stylesheet]
        self._payload = lilypond_file

    ### PRIVATE METHODS ###

    def _render_pdf_source(
        self,
        temporary_directory_path,
        ):
        ly_file_path = os.path.join(
            temporary_directory_path,
            self.file_name_without_extension + '.ly',
            )
        source = format(self.payload)
        with open(ly_file_path, 'w') as file_pointer:
            file_pointer.write(source)
        systemtools.IOManager.run_lilypond(ly_file_path)
        pdf_file_path = os.path.join(
            temporary_directory_path,
            self.file_name_without_extension + '.pdf',
            )
        if not os.path.exists(pdf_file_path):
            print(format(self.payload))
            raise AssertionError
        assert systemtools.IOManager.find_executable('pdfcrop')
        command = 'pdfcrop {path} {path}'.format(path=pdf_file_path)
        exit_code = subprocess.call(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        assert exit_code == 0
        return pdf_file_path

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
        ):
        from abjad.tools import abjadbooktools
        code = format(self.payload)
        block = abjadbooktools.SphinxDocumentHandler.abjad_output_block(code, code)
        block['renderer'] = 'lilypond'
        return [block]

    ### PUBLIC PROPERTIES ###

    @property
    def file_name_prefix(self):
        return 'lilypond'

    @property
    def stylesheet(self):
        return self._stylesheet