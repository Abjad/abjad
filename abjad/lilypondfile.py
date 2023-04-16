import dataclasses

from . import _indentlib
from . import configuration as _configuration
from . import indicators as _indicators
from . import iterate as _iterate
from . import score as _score
from . import tag as _tag

configuration = _configuration.Configuration()


@dataclasses.dataclass
class Block:
    r'''
    LilyPond file block.

    ..  container:: example

        Use strings to add contents to a block:

        >>> string = r"""right-margin = 2\cm
        ...     left-margin = 2\cm"""
        >>> block = abjad.Block("paper", items=[string])
        >>> string = abjad.lilypond(block)
        >>> print(string)
        \paper
        {
            right-margin = 2\cm
            left-margin = 2\cm
        }

    ..  container:: example

        Define a context block like this:

        >>> string = r"""\Staff
        ...     \name FluteStaff
        ...     \type Engraver_group
        ...     \alias Staff
        ...     \remove Forbid_line_break_engraver
        ...     \consists Horizontal_bracket_engraver
        ...     \accepts FluteUpperVoice
        ...     \accepts FluteLowerVoice
        ...     \override Beam.positions = #'(-4 . -4)
        ...     \override Stem.stem-end-position = -6
        ...     autoBeaming = ##f
        ...     tupletFullLength = ##t
        ...     \accidentalStyle dodecaphonic"""
        >>> block = abjad.Block("context", items=[string])
        >>> string = abjad.lilypond(block)
        >>> print(string)
        \context
        {
            \Staff
            \name FluteStaff
            \type Engraver_group
            \alias Staff
            \remove Forbid_line_break_engraver
            \consists Horizontal_bracket_engraver
            \accepts FluteUpperVoice
            \accepts FluteLowerVoice
            \override Beam.positions = #'(-4 . -4)
            \override Stem.stem-end-position = -6
            autoBeaming = ##f
            tupletFullLength = ##t
            \accidentalStyle dodecaphonic
        }

    ..  container:: example

        Define an anonymous block like this:

        >>> string = r"""command-1
        ...     command-2
        ...     command-3"""
        >>> block = abjad.Block("", items=[string])
        >>> string = abjad.lilypond(block)
        >>> print(string)
        {
            command-1
            command-2
            command-3
        }

    ..  container:: example

        Markup formats like this:

        >>> block = abjad.Block("score", items=[abjad.Markup(r"\markup foo")])
        >>> string = abjad.lilypond(block)
        >>> print(string)
        \score
        {
            \markup foo
        }

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> block = abjad.Block("score")
        >>> block.items.append("<<")
        >>> block.items.append(r'{ \include "layout.ly" }')
        >>> block.items.append(staff)
        >>> block.items.append(">>")
        >>> lilypond_file = abjad.LilyPondFile(
        ...     lilypond_language_token=False,
        ...     lilypond_version_token=False,
        ... )
        >>> lilypond_file.items.append(block)
        >>> string = abjad.lilypond(lilypond_file)
        >>> print(string)
        \score
        {
            <<
            { \include "layout.ly" }
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }
            >>
        }

    '''

    name: str | None = None
    items: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        assert isinstance(self.items, list), repr(self.items)

    @staticmethod
    def _format_item(item, depth=1):
        indent = depth * _indentlib.INDENT
        result = []
        if isinstance(item, str):
            if item.isspace():
                string = ""
            else:
                string = indent + item
            result.append(string)
        elif hasattr(item, "_get_lilypond_format"):
            string = item._get_lilypond_format()
            pieces = string.split("\n")
            for piece in pieces:
                if piece.isspace():
                    piece = ""
                else:
                    piece = indent + piece
                result.append(piece)
        else:
            assert isinstance(item, _indicators.Markup), repr(item)
            string = indent + item.string
            result.append(string)
        return result

    def _get_lilypond_format(self, tag=None):
        result = []
        if not len(self.items):
            if self.name:
                string = rf"\{self.name} {{}}"
            else:
                string = "{}"
            return string
        strings = []
        if self.name:
            strings.append(rf"\{self.name}")
        strings.append("{")
        if tag is not None:
            strings = _tag.double_tag(strings, tag)
        result.extend(strings)
        for item in self.items:
            result.extend(self._format_item(item))
        string = "}"
        strings = [string]
        if tag is not None:
            strings = _tag.double_tag(strings, tag)
        result.extend(strings)
        string = "\n".join(result)
        return string


@dataclasses.dataclass(slots=True)
class LilyPondFile:
    r"""
    LilyPond file.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> lilypond_file = abjad.LilyPondFile(
        ...     items=[
        ...         r'\include "abjad.ily"',
        ...         '''#(set-default-paper-size "a5" 'portrait)''',
        ...         "#(set-global-staff-size 16)",
        ...         staff,
        ...     ],
        ... )

        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ::

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \version "..."
            \language "english"
            \include "abjad.ily"
            #(set-default-paper-size "a5" 'portrait)
            #(set-global-staff-size 16)
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }

    """

    items: list = dataclasses.field(default_factory=list)
    lilypond_language_token: bool | str = True
    lilypond_version_token: bool | str = True
    tag: _tag.Tag | None = None

    def __contains__(self, argument) -> bool:
        """
        Is true when LilyPond file contains ``argument``.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
            >>> lilypond_file = abjad.LilyPondFile([staff])

            >>> "Staff" in lilypond_file
            True

            >>> "Allegro" in lilypond_file
            False

            >>> 0 in lilypond_file
            False

        """
        try:
            self[argument]
            return True
        except (AssertionError, KeyError, ValueError, TypeError):
            return False

    def __getitem__(self, argument):
        r"""
        Gets item identified by ``argument``.

        ..  container:: example

            Searches score:

            >>> voice_1 = abjad.Voice("c''4 b' a' g'", name="Voice_1")
            >>> command = abjad.VoiceNumber(1)
            >>> abjad.attach(command, voice_1[0])
            >>> voice_2 = abjad.Voice("c'4 d' e' f'", name="Voice_2")
            >>> command = abjad.VoiceNumber(2)
            >>> abjad.attach(command, voice_2[0])
            >>> staff = abjad.Staff(
            ...     [voice_1, voice_2],
            ...     simultaneous=True,
            ...     name="Staff",
            ... )
            >>> score = abjad.Score([staff], name="Score")
            >>> block = abjad.Block("score")
            >>> block.items.append(score)
            >>> lilypond_file = abjad.LilyPondFile([block])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            c''4
                            b'4
                            a'4
                            g'4
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    >>
                >>

            >>> lilypond_file["score"]
            Block(name='score', items=[Score("{ { c''4 b'4 a'4 g'4 } { c'4 d'4 e'4 f'4 } }", name='Score', simultaneous=True)])

            >>> lilypond_file["Score"]
            Score("{ { c''4 b'4 a'4 g'4 } { c'4 d'4 e'4 f'4 } }", name='Score', simultaneous=True)

            >>> lilypond_file["Staff"]
            Staff("{ c''4 b'4 a'4 g'4 } { c'4 d'4 e'4 f'4 }", name='Staff', simultaneous=True)

            >>> lilypond_file["Voice_1"]
            Voice("c''4 b'4 a'4 g'4", name='Voice_1')

            >>> lilypond_file["Voice_2"]
            Voice("c'4 d'4 e'4 f'4", name='Voice_2')

        ..  container:: example

            Searches score:

            >>> voice_1 = abjad.Voice("c''4 b' a' g'", name="Voice_1")
            >>> command = abjad.VoiceNumber(1)
            >>> abjad.attach(command, voice_1[0])
            >>> voice_2 = abjad.Voice("c'4 d' e' f'", name="Voice_2")
            >>> command = abjad.VoiceNumber(2)
            >>> abjad.attach(command, voice_2[0])
            >>> staff = abjad.Staff(
            ...     [voice_1, voice_2],
            ...     simultaneous=True,
            ...     name="Staff",
            ... )
            >>> score = abjad.Score([staff], name="Score")
            >>> lilypond_file = abjad.LilyPondFile([score])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            c''4
                            b'4
                            a'4
                            g'4
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    >>
                >>

            >>> lilypond_file["Score"]
            Score("{ { c''4 b'4 a'4 g'4 } { c'4 d'4 e'4 f'4 } }", name='Score', simultaneous=True)

            >>> lilypond_file["Staff"]
            Staff("{ c''4 b'4 a'4 g'4 } { c'4 d'4 e'4 f'4 }", name='Staff', simultaneous=True)

            >>> lilypond_file["Voice_1"]
            Voice("c''4 b'4 a'4 g'4", name='Voice_1')

            >>> lilypond_file["Voice_2"]
            Voice("c'4 d'4 e'4 f'4", name='Voice_2')

        ..  container:: example

            REGRESSION. Works when score block contains parallel container:

            >>> include_container = abjad.Container()
            >>> string = r'\include "layout.ly"'
            >>> literal = abjad.LilyPondLiteral(string, site="opening")
            >>> abjad.attach(literal, include_container)
            >>> staff = abjad.Staff("c'4 d' e' f'", name="Staff")
            >>> container = abjad.Container(
            ...     [include_container, staff],
            ...     simultaneous=True,
            ... )
            >>> block = abjad.Block("score")
            >>> block.items.append(container)
            >>> lilypond_file = abjad.LilyPondFile(
            ...     items=[block],
            ...     lilypond_language_token=False,
            ...     lilypond_version_token=False,
            ... )
            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \score
            {
                <<
                    {
                        \include "layout.ly"
                    }
                    \context Staff = "Staff"
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                >>
            }

            >>> lilypond_file['Staff']
            Staff("c'4 d'4 e'4 f'4", name='Staff')

        ..  container:: example

            Finds blocks by name:

            >>> blocks = [abjad.Block("header"), abjad.Block("score")]
            >>> lilypond_file = abjad.LilyPondFile(items=blocks)
            >>> lilypond_file["score"]
            Block(name='score', items=[])

            >>> score = abjad.Score([abjad.Staff("c'4 d' e' f'")], name="Score")
            >>> lilypond_file["score"].items.append(score)
            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \version "..."
            \language "english"
            \header {}
            \score
            {
                \context Score = "Score"
                <<
                    \new Staff
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                >>
            }

        Returns block or component.
        """
        assert isinstance(argument, str), repr(argument)
        for item in self.items:
            if getattr(item, "name", None) == argument:
                return item
            elif hasattr(item, "items"):
                for item_ in item.items:
                    if getattr(item_, "name", None) == argument:
                        return item_
                    if isinstance(item_, _score.Component):
                        for component in _iterate.components(item_):
                            if getattr(component, "name", None) == argument:
                                return component
            elif isinstance(item, _score.Component):
                for component in _iterate.components(item):
                    if getattr(component, "name", None) == argument:
                        return component
        raise KeyError(f"no block or component with name {argument!r}.")

    def _get_lilypond_format(self):
        result = []
        strings = []
        if self.lilypond_version_token is True:
            string = configuration.get_lilypond_version_string()
            string = rf'\version "{string}"'
            strings.append(string)
        elif isinstance(self.lilypond_version_token, str):
            strings.append(self.lilypond_version_token)
        if self.lilypond_language_token is True:
            string = r'\language "english"'
            strings.append(string)
        # TODO: change to abjad.LilyPondFile._get_lilypond_format()
        tag = _tag.Tag("abjad.LilyPondFile._get_format_pieces()")
        tag = self.get_tag(tag)
        strings = _tag.double_tag(strings, tag)
        result.extend(strings)
        for item in self.items:
            if isinstance(item, str):
                result.append(item)
            else:
                try:
                    string = item._get_lilypond_format(tag=tag)
                except TypeError:
                    string = item._get_lilypond_format()
                assert isinstance(string, str), repr(string)
                result.append(string)
        strings = result
        string = "\n".join(strings)
        lines = []
        for line in string.split("\n"):
            if line.isspace():
                lines.append("")
            else:
                lines.append(line)
        return "\n".join(lines)

    def get_tag(self, site=None):
        """
        Gets tag.
        """
        if self.tag:
            tag = _tag.Tag(self.tag.string)
        else:
            tag = _tag.Tag()
        tag = tag.append(site)
        return tag
