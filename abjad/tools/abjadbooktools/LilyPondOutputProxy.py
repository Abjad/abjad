import copy
import os
import subprocess
from abjad.tools import documentationtools
from abjad.tools import systemtools
from abjad.tools import lilypondfiletools
from abjad.tools.abjadbooktools.ImageOutputProxy import ImageOutputProxy


class LilyPondOutputProxy(ImageOutputProxy):
    r"""
    A LilyPond output proxy.

    ::

        >>> from abjad.tools import abjadbooktools
        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> proxy = abjadbooktools.LilyPondOutputProxy(staff)
        >>> print(format(proxy))
        abjad.abjadbooktools.LilyPondOutputProxy(
            abjad.LilyPondFile(
                comments=[],
                global_staff_size=12,
                includes=[],
                items=[
                    abjad.Block(
                        name='header',
                        ),
                    abjad.Block(
                        name='layout',
                        ),
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

    ::

        >>> proxy.as_latex(relative_output_directory='assets')
        ['\\noindent\\includegraphics{assets/lilypond-0b731cedacea34e85fbb92b66b42b40b.pdf}']

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
        ):
        from abjad.tools import abjadbooktools
        ImageOutputProxy.__init__(
            self,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            )
        payload = copy.deepcopy(payload)
        if image_render_specifier is None:
            image_render_specifier = abjadbooktools.ImageRenderSpecifier()
        if (
            not image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet
            ):
            payload = documentationtools.make_reference_manual_lilypond_file(
                payload)
        lilypond_file = payload
        assert isinstance(lilypond_file, lilypondfiletools.LilyPondFile)
        if (lilypond_file.layout_block and
            not len(lilypond_file.layout_block.items)):
            lilypond_file.items.remove(lilypond_file.layout_block)
        if (lilypond_file.paper_block and
            not len(lilypond_file.paper_block.items)):
            lilypond_file.items.remove(lilypond_file.paper_block)
        if lilypond_file.header_block is None:
            header_block = lilypondfiletools.Block(name='header')
            lilypond_file.items.insert(0, header_block)
        lilypond_file.header_block.tagline = False
        lilypond_file._date_time_token = None
        token = lilypondfiletools.LilyPondVersionToken("2.19.0")
        lilypond_file._lilypond_version_token = token
        if (
            image_render_specifier.stylesheet and
            not image_render_specifier.no_stylesheet
            ):
            if not lilypond_file.includes:
                lilypond_file._use_relative_includes = True
                includes = [image_render_specifier.stylesheet]
                lilypond_file._includes = tuple(includes)
        self._payload = lilypond_file

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

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
        ):
        r"""
        Creates a docutils node representation of the output proxy.

        ::

            >>> from abjad.tools import abjadbooktools
            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> proxy = abjadbooktools.LilyPondOutputProxy(staff)
            >>> for node in proxy.as_docutils():
            ...     print(node.pformat())
            ...
            <abjad_output_block image_layout_specifier... image_render_specifier... renderer="lilypond" xml:space="preserve">
                \version "2.19.0"
                \language "english"
            <BLANKLINE>
                #(set-global-staff-size 12)
            <BLANKLINE>
                \header {
                    tagline = ##f
                }
            <BLANKLINE>
                \layout {
                    indent = #0
                    ragged-right = ##t
                    \context {
                        \Score
                        \remove Bar_number_engraver
                        \override SpacingSpanner.strict-grace-spacing = ##t
                        \override SpacingSpanner.strict-note-spacing = ##t
                        \override SpacingSpanner.uniform-stretching = ##t
                        \override TupletBracket.bracket-visibility = ##t
                        \override TupletBracket.minimum-length = #3
                        \override TupletBracket.padding = #2
                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                        proportionalNotationDuration = #(ly:make-moment 1 24)
                        tupletFullLength = ##t
                    }
                }
            <BLANKLINE>
                \score {
                    \new Staff {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            <BLANKLINE>

        Returns list of docutils nodes.
        """
        from abjad.tools import abjadbooktools
        result = []
        try:
            code = format(self.payload)
            node = abjadbooktools.abjad_output_block(code, code)
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

    ### PUBLIC PROPERTIES ###

    @property
    def file_name_prefix(self):
        """
        Gets file name prefix of LilyPond output proxy.

        Returns string.
        """
        return 'lilypond'
