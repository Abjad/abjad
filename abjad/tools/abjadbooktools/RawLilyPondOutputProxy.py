# -*- coding: utf-8 -*-
import os
import subprocess
from abjad.tools import systemtools
from abjad.tools.abjadbooktools.ImageOutputProxy import ImageOutputProxy


class RawLilyPondOutputProxy(ImageOutputProxy):
    """
    A raw LilyPond output proxy.

    ::

        >>> from abjad.tools import abjadbooktools
        >>> raw_lilypond = '{ c d e f }'
        >>> proxy = abjadbooktools.RawLilyPondOutputProxy(raw_lilypond)
        >>> print(format(proxy))
        abjadbooktools.RawLilyPondOutputProxy(
            '\\version "2.19.0"\n\n{ c d e f }'
            )

    ::

        >>> proxy.as_latex(relative_output_directory='assets')
        ['\\noindent\\includegraphics{assets/lilypond-678fb46ce202b3d770361f814e6e1946.pdf}']

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output Proxies'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        payload,
        image_layout_specifier=None,
        image_render_specifier=None,
        **options
        ):
        from abjad.tools import abjadbooktools
        ImageOutputProxy.__init__(
            self,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            **options
            )
        if image_render_specifier is None:
            image_render_specifier = abjadbooktools.ImageRenderSpecifier()
        preamble = []
        if not payload.startswith(r'\version'):
            preamble.extend([r'\version "2.19.0"', ''])
        if (
            image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet
            ):
            preamble.extend([
                "#(ly:set-option 'relative-includes #t)",
                '\include "{}"'.format(image_render_specifier.stylesheet),
                '',
                ])
        if preamble:
            payload = '\n'.join(preamble) + '\n' + payload
        self._payload = payload

    ### PRIVATE METHODS ###

    def _render_pdf_source(
        self,
        temporary_directory_path,
        ):
        from abjad import abjad_configuration
        log_file_path = abjad_configuration.lilypond_log_file_path
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
            with open(log_file_path) as file_pointer:
                print(file_pointer.read())
            raise AssertionError
        assert systemtools.IOManager.find_executable('pdfcrop')
        command = 'pdfcrop {path} {path}'.format(path=pdf_file_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            )
        stdout, stderr = process.communicate()
        if not process.returncode == 0:
            raise Exception(stdout)
        return pdf_file_path

    ### PUBLIC PROPERTIES ###

    @property
    def file_name_prefix(self):
        r'''Gets file name prefix of LilyPond output proxy.

        Returns string.
        '''
        return 'lilypond'
