import copy
import os
import subprocess
from abjad.tools import lilypondfiletools
from abjad.tools import systemtools
from .ImageOutputProxy import ImageOutputProxy
from .ImageRenderSpecifier import ImageRenderSpecifier
from .abjad_output_block import abjad_output_block


class LilyPondOutputProxy(ImageOutputProxy):
    r"""
    A LilyPond output proxy.

    >>> import abjad.book
    >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
    >>> proxy = abjad.book.LilyPondOutputProxy(staff)
    >>> print(format(proxy))
    abjad.book.LilyPondOutputProxy(
        abjad.LilyPondFile(
            comments=[],
            includes=[],
            items=[
                abjad.Block(
                    name='score',
                    ),
                ],
            lilypond_language_token=abjad.LilyPondLanguageToken(),
            lilypond_version_token=abjad.LilyPondVersionToken(
                version_string='2.19.0',
                ),
            )
        )

    >>> proxy.as_latex(relative_output_directory='assets')
    ['\\noindent\\includegraphics{assets/lilypond-d3ecbde01b2f252633e28953dae06eea.pdf}']

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_strict',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        payload,
        image_layout_specifier=None,
        image_render_specifier=None,
        strict=None,
        ):
        ImageOutputProxy.__init__(
            self,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            )
        payload = copy.deepcopy(payload)
        if image_render_specifier is None:
            image_render_specifier = ImageRenderSpecifier()
        if (not image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet):
            payload = lilypondfiletools.LilyPondFile.new(payload)
        lilypond_file = payload
        assert isinstance(lilypond_file, lilypondfiletools.LilyPondFile)
        if lilypond_file.header_block:
            if getattr(lilypond_file.header_block, 'tagline') is False:
                # default.ily stylesheet already sets tagline = ##f
                delattr(lilypond_file.header_block, 'tagline')
            if lilypond_file.header_block.empty():
                lilypond_file.items.remove(lilypond_file.header_block)
        if lilypond_file.layout_block and lilypond_file.layout_block.empty():
            lilypond_file.items.remove(lilypond_file.layout_block)
        if lilypond_file.paper_block and lilypond_file.paper_block.empty():
            lilypond_file.items.remove(lilypond_file.paper_block)
        lilypond_file._date_time_token = None
        token = lilypondfiletools.LilyPondVersionToken("2.19.0")
        lilypond_file._lilypond_version_token = token
        if (image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet):
            if not lilypond_file.includes:
                lilypond_file._use_relative_includes = True
                includes = [image_render_specifier.stylesheet]
                lilypond_file._includes = tuple(includes)
        self._payload = lilypond_file
        self._strict = strict

    ### PRIVATE METHODS ###

    def _render_pdf_source(
        self,
        temporary_directory,
        ):
        ly_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.ly',
            )
        source = format(self.payload)
        with open(ly_file_path, 'w') as file_pointer:
            file_pointer.write(source)
        systemtools.IOManager.run_lilypond(ly_file_path)
        pdf_file_path = os.path.join(
            temporary_directory,
            self.file_name_without_extension + '.pdf',
            )
        if not os.path.exists(pdf_file_path):
            print(format(self.payload))
            raise AssertionError
        assert systemtools.IOManager.find_executable('pdfcrop')
        command = f'pdfcrop {pdf_file_path} {pdf_file_path}'
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
        r"""
        Gets file name prefix of LilyPond output proxy.

        Returns string.
        """
        return 'lilypond'

    @property
    def strict(self):
        r"""
        Is true when LilyPond file should format strict.

        Returns true, false or none.
        """
        return self._strict

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
        ):
        r"""
        Creates a docutils node representation of the output proxy.

        >>> import abjad.book
        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> proxy = abjad.book.LilyPondOutputProxy(staff)
        >>> for node in proxy.as_docutils():
        ...     print(node.pformat())
        ...
        <abjad_output_block image_layout_specifier="True" image_render_specifier="True" renderer="lilypond" xml:space="preserve">
            \version "2.19.0"
            \language "english"
        <BLANKLINE>
            \score {
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }
        <BLANKLINE>

        Returns list of docutils nodes.
        """
        result = []
        assert self.strict is not False, repr(self.strict)
        try:
            code = format(self.payload, 'lilypond')
            if isinstance(self.strict, int):
                code = systemtools.LilyPondFormatManager.align_tags(
                    code,
                    self.strict,
                    )
            if self.strict:
                if isinstance(self.strict, int):
                    realign = self.strict
                else:
                    realign = None
                code = systemtools.LilyPondFormatManager.left_shift_tags(
                    code,
                    realign=realign,
                    )
            node = abjad_output_block(code, code)
            node['image_layout_specifier'] = self.image_layout_specifier
            node['image_render_specifier'] = self.image_render_specifier
            node['renderer'] = 'lilypond'
            result.append(node)
        except UnicodeDecodeError:
            print()
            print(type(self))
            for line in code.splitlines():
                print(repr(line))
        return result
