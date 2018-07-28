import collections
import copy
import inspect
import pathlib
from abjad.indicators.LilyPondLiteral import LilyPondLiteral
from abjad.system.AbjadObject import AbjadObject
from abjad.pitch.NamedPitch import NamedPitch
from abjad.core.Component import Component
from abjad.core.Container import Container
from abjad.core.Context import Context
from abjad.core.MeasureMaker import MeasureMaker
from abjad.core.Note import Note
from abjad.core.Score import Score
from abjad.core.Selection import Selection
from abjad.core.Staff import Staff
from abjad.core.Voice import Voice
from abjad.scheme import Scheme
from abjad.scheme import SpacingVector
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.attach import attach
from abjad.top.inspect import inspect as abjad_inspect
from abjad.top.iterate import iterate
from abjad.top.mutate import mutate
from abjad.top.override import override
from abjad.top.sequence import sequence
from .Block import Block
from .ContextBlock import ContextBlock
from .DateTimeToken import DateTimeToken
from .LilyPondLanguageToken import LilyPondLanguageToken
from .LilyPondVersionToken import LilyPondVersionToken


class LilyPondFile(AbjadObject):
    r"""
    A LilyPond file.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> comments = [
        ...     'File construct as an example.',
        ...     'Parts shown here for positioning.',
        ...     ]
        >>> includes = [
        ...     'external-settings-file-1.ily',
        ...     'external-settings-file-2.ily',
        ...     ]
        >>> lilypond_file = abjad.LilyPondFile.new(
        ...     music=staff,
        ...     default_paper_size=('a5', 'portrait'),
        ...     comments=comments,
        ...     includes=includes,
        ...     global_staff_size=16,
        ...     )

        >>> lilypond_file.header_block.composer = abjad.Markup('Josquin')
        >>> lilypond_file.header_block.title = abjad.Markup('Missa sexti tonus')
        >>> lilypond_file.layout_block.indent = 0
        >>> lilypond_file.layout_block.left_margin = 15
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ::

            >>> print(format(lilypond_file)) # doctest: +SKIP
            % 2004-01-14 17:29

            % File construct as an example.
            % Parts shown here for positioning.

            \version "2.19.0"
            \language "english"

            \include "external-settings-file-1.ily"
            \include "external-settings-file-2.ily"

            #(set-default-paper-size "a5" 'portrait)
            #(set-global-staff-size 16)

            \header {
                composer = \markup { Josquin }
                title = \markup { Missa sexti toni }
            }

            \layout {
                indent = #0
                left-margin = #15
            }

            \paper {
            }

            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_comments',
        '_date_time_token',
        '_default_paper_size',
        '_global_staff_size',
        '_includes',
        '_items',
        '_lilypond_language_token',
        '_lilypond_version_token',
        '_use_relative_includes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        comments=None,
        date_time_token=None,
        default_paper_size=None,
        global_staff_size=None,
        includes=None,
        items=None,
        lilypond_language_token=None,
        lilypond_version_token=None,
        use_relative_includes=None,
        ):
        comments = comments or ()
        comments = tuple(comments)
        self._comments = comments
        self._date_time_token = None
        if bool(date_time_token):
            self._date_time_token = DateTimeToken()
        self._default_paper_size = default_paper_size
        self._global_staff_size = global_staff_size
        includes = list(includes or [])
        includes = [str(_) for _ in includes]
        self._includes = includes
        self._items = list(items or [])
        self._lilypond_language_token = None
        if lilypond_language_token is not False:
            token = LilyPondLanguageToken()
            self._lilypond_language_token = token
        self._lilypond_version_token = None
        if lilypond_version_token is not False:
            token = LilyPondVersionToken()
            self._lilypond_version_token = token
        self._use_relative_includes = use_relative_includes

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when LilyPond file contains ``argument``.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> lilypond_file = abjad.LilyPondFile.new(staff)

            >>> staff in lilypond_file
            True

            >>> abjad.Staff in lilypond_file
            True

            >>> 'Allegro' in lilypond_file
            False

            >>> 0 in lilypond_file
            False

        """
        try:
            item = self[argument]
            return True
        except (AssertionError, KeyError, ValueError, TypeError):
            return False
        
    def __format__(self, format_specification=''):
        r"""
        Formats LilyPond file.

        ..  container:: example

            Gets format:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> print(format(lilypond_file)) # doctest: +SKIP
            % 2016-01-31 20:29
            <BLANKLINE>
            \version "2.19.35"
            \language "english"
            <BLANKLINE>
            \header {}
            <BLANKLINE>
            \layout {}
            <BLANKLINE>
            \paper {}

        ..  container:: example

            Works with empty layout and MIDI blocks:

            >>> score = abjad.Score([abjad.Staff("c'8 d'8 e'8 f'8")])
            >>> score_block = abjad.Block(name='score')
            >>> layout_block = abjad.Block(name='layout')
            >>> midi_block = abjad.Block(name='midi')
            >>> score_block.items.append(score)
            >>> score_block.items.append(layout_block)
            >>> score_block.items.append(midi_block)

            >>> abjad.f(score_block)
            \score {
                \new Score
                <<
                    \new Staff
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                >>
                \layout {}
                \midi {}
            }

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.attach(abjad.Articulation('.'), staff[0])
            >>> abjad.attach(abjad.Markup('Allegro'), staff[0])
            >>> score = abjad.Score([staff])
            >>> lilypond_file = abjad.LilyPondFile.new([score])
            >>> lilypond_file._lilypond_version_token = None

            >>> abjad.f(lilypond_file)
            \language "english"
            <BLANKLINE>
            \header {
                tagline = ##f
            }
            <BLANKLINE>
            \layout {}
            <BLANKLINE>
            \paper {}
            <BLANKLINE>
            \score {
                {
                    \new Score
                    <<
                        \new Staff
                        {
                            c'8
                            -\staccato
                            - \markup { Allegro }
                            d'8
                            e'8
                            f'8
                        }
                    >>
                }
            }

        Returns string.
        """
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        else:
            assert format_specification == 'storage'
            return StorageFormatManager(self).get_storage_format()

    def __getitem__(self, name):
        r"""
        Gets item with ``name``.

        ..  container:: example

            Gets header block:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file['header']
            <Block(name='header')>

        ..  container:: example

            Searches score:

            >>> voice_1 = abjad.Voice("c''4 b' a' g'", name='Custom Voice 1')
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> voice_2 = abjad.Voice("c'4 d' e' f'", name='Custom Voice 2')
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> staff = abjad.Staff(
            ...     [voice_1, voice_2],
            ...     is_simultaneous=True,
            ...     name='Custom Staff',
            ...     )
            >>> score = abjad.Score([staff], name='Custom Score')
            >>> lilypond_file = abjad.LilyPondFile.new(score)
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \context Score = "Custom Score"
                <<
                    \context Staff = "Custom Staff"
                    <<
                        \context Voice = "Custom Voice 1"
                        {
                            \voiceOne
                            c''4
                            b'4
                            a'4
                            g'4
                        }
                        \context Voice = "Custom Voice 2"
                        {
                            \voiceTwo
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    >>
                >>

            >>> lilypond_file['score']
            <Block(name='score')>

            >>> lilypond_file['Custom Score']
            <Score-"Custom Score"<<1>>>

            >>> lilypond_file[abjad.Score]
            <Score-"Custom Score"<<1>>>

            >>> lilypond_file['Custom Staff']
            <Staff-"Custom Staff"<<2>>>

            >>> lilypond_file[abjad.Staff]
            <Staff-"Custom Staff"<<2>>>

            >>> lilypond_file['Custom Voice 1']
            Voice("c''4 b'4 a'4 g'4", name='Custom Voice 1')

            >>> lilypond_file['Custom Voice 2']
            Voice("c'4 d'4 e'4 f'4", name='Custom Voice 2')

            >>> lilypond_file[abjad.Voice]
            Voice("c''4 b'4 a'4 g'4", name='Custom Voice 1')

        ..  container:: example

            REGRESSION. Works when score block contains parallel container:

                >>> include_container = abjad.Container()
                >>> string = r'\include "layout.ly"'
                >>> literal = abjad.LilyPondLiteral(string, 'opening')
                >>> abjad.attach(literal, include_container)
                >>> staff = abjad.Staff("c'4 d' e' f'", name='CustomStaff')
                >>> container = abjad.Container(
                ...     [include_container, staff],
                ...     is_simultaneous=True,
                ...     )
                >>> lilypond_file = abjad.LilyPondFile.new(
                ...     container,
                ...     lilypond_language_token=False,
                ...     lilypond_version_token=False,
                ...     )
                >>> del(lilypond_file.items[:3])

                >>> abjad.f(lilypond_file)
                \score {
                    <<
                        {
                            \include "layout.ly"
                        }
                        \context Staff = "CustomStaff"
                        {
                            c'4
                            d'4
                            e'4
                            f'4
                        }
                    >>
                }

                >>> lilypond_file[abjad.Staff]
                Staff("c'4 d'4 e'4 f'4", name='CustomStaff')

                >>> lilypond_file['CustomStaff']
                Staff("c'4 d'4 e'4 f'4", name='CustomStaff')

        Returns item.

        Raises key error when no item with ``name`` is found.
        """
        if not isinstance(name, str):
            if inspect.isclass(name):
                assert issubclass(name, Component), repr(name)
            else:
                assert isinstance(name, Component), repr(name)
        score = None
        if self.score_block and self.score_block.items:
            items = self.score_block.items
            for container in iterate(items).components(Container):
                if isinstance(container, Context):
                    score = container
                    break
        if isinstance(name, str):
            for item in self.items:
                if getattr(item, 'name', None) == name:
                    return item
            if score is not None:
                if score.name == name:
                    return score
                context = score[name]
                return context
            raise KeyError(f'can not find item with name {name!r}.')
        elif isinstance(name, Component):
            for item in self.items:
                if item is name:
                    return item
            if score is not None:
                if score is name:
                    return score
                prototype = Context
                for context in iterate(score).components(prototype):
                    if context is name:
                        return context
            raise KeyError(f'can not find {name}.')
        elif inspect.isclass(name) and issubclass(name, Component):
            for item in self.items:
                if isinstance(item, name):
                    return item
            if score is not None:
                if isinstance(score, name):
                    return score
                prototype = Context
                for context in iterate(score).components(prototype):
                    if isinstance(context, name):
                        return context
            raise KeyError(f'can not find item of class {name}.')
        else:
            raise TypeError(name)

    def __illustrate__(self):
        """
        Illustrates LilyPond file.

        Returns LilyPond file unchanged.
        """
        return self

    def __repr__(self):
        """
        Gets interpreter representation of LilyPond file.

        ..  container:: example

            Gets interpreter representation:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file
            LilyPondFile(comments=[],
            includes=[],
            items=[<Block(name='header')>, <Block(name='layout')>,
            <Block(name='paper')>, <Block(name='score')>],
            lilypond_language_token=LilyPondLanguageToken(),
            lilypond_version_token=LilyPondVersionToken(version_string='...'))

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        result = []
        if self.date_time_token is not None:
            string = f'% {self.date_time_token}'
            result.append(string)
        result.extend(self._get_formatted_comments())
        includes = []
        if self.lilypond_version_token is not None:
            string = f'{self.lilypond_version_token}'
            includes.append(string)
        if self.lilypond_language_token is not None:
            string = f'{self.lilypond_language_token}'
            includes.append(string)
        includes = '\n'.join(includes)
        if includes:
            result.append(includes)
        if self.use_relative_includes:
            string = "#(ly:set-option 'relative-includes #t)"
            result.append(string)
        result.extend(self._get_formatted_includes())
        result.extend(self._get_formatted_scheme_settings())
        result.extend(self._get_formatted_blocks())
        return result

    ### PRIVATE METHODS ###

    def _get_formatted_blocks(self):
        result = []
        for item in self.items:
            if ('_get_lilypond_format' in dir(item) and
                not isinstance(item, str)):
                try:
                    string = item._get_lilypond_format()
                except TypeError:
                    string = item._get_lilypond_format()
                if string:
                    result.append(string)
            else:
                result.append(str(item))
        return result

    def _get_formatted_comments(self):
        result = []
        for comment in self.comments:
            if ('_get_lilypond_format' in dir(comment) and
                not isinstance(comment, str)):
                lilypond_format = format(comment)
                if lilypond_format:
                    string = f'% {comment}'
                    result.append(string)
            else:
                string = f'% {comment!s}'
                result.append(string)
        if result:
            result = ['\n'.join(result)]
        return result

    def _get_formatted_includes(self):
        result = []
        for include in self.includes:
            if isinstance(include, str):
                string = rf'\include "{include}"'
                result.append(string)
            elif isinstance(include, pathlib.Path):
                string = rf'\include "{include!s}"'
                result.append(string)
            else:
                result.append(format(include))
        if result:
            result = ['\n'.join(result)]
        return result

    def _get_formatted_scheme_settings(self):
        result = []
        default_paper_size = self.default_paper_size
        if default_paper_size is not None:
            dimension, orientation = default_paper_size
            string = f"#(set-default-paper-size \"{dimension}\" '{orientation})"
            result.append(string)
        global_staff_size = self.global_staff_size
        if global_staff_size is not None:
            string = f'#(set-global-staff-size {global_staff_size})'
            result.append(string)
        if result:
            result = ['\n'.join(result)]
        return result

    def _get_lilypond_format(self):
        return '\n\n'.join(self._get_format_pieces())

    @staticmethod
    def _make_global_context_block(
        font_size=3,
        minimum_distance=10,
        padding=4,
        ):
        assert isinstance(font_size, (int, float))
        assert isinstance(padding, (int, float))
        block = ContextBlock(
            type_='Engraver_group',
            name='GlobalContext',
            )
        block.consists_commands.append('Axis_group_engraver')
        block.consists_commands.append('Time_signature_engraver')
        time_signature_grob = override(block).time_signature
        time_signature_grob.X_extent = (0, 0)
        time_signature_grob.X_offset = Scheme(
            'ly:self-alignment-interface::x-aligned-on-self'
            )
        time_signature_grob.Y_extent = (0, 0)
        time_signature_grob.break_align_symbol = False
        time_signature_grob.break_visibility = Scheme(
            'end-of-line-invisible',
            )
        time_signature_grob.font_size = font_size
        time_signature_grob.self_alignment_X = Scheme('center')
        spacing_vector = SpacingVector(
            0,
            minimum_distance,
            padding,
            0,
            )
        grob = override(block).vertical_axis_group
        grob.default_staff_staff_spacing = spacing_vector
        return block

    ### PUBLIC PROPERTIES ###

    @property
    def comments(self):
        """
        Gets comments of Lilypond file.

        ..  container:: example

            Gets comments:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.comments
            []

        Returns list.
        """
        return list(self._comments)

    @property
    def date_time_token(self):
        """
        Gets date-time token.

        ..  container:: example

            Gets date-time token:

            >>> lilypond_file = abjad.LilyPondFile.new(date_time_token=True)

            >>> lilypond_file.date_time_token
            DateTimeToken()

        Returns date-time token or none.
        """
        return self._date_time_token

    @property
    def default_paper_size(self):
        """
        Gets default paper size of LilyPond file.

        ..  container:: example

            Gets default paper size:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.default_paper_size is None
            True

        Set to pair or none.

        Defaults to none.

        Returns pair or none.
        """
        return self._default_paper_size

    @property
    def global_staff_size(self):
        """
        Gets global staff size of LilyPond file.

        ..  container:: example

            Gets global staff size:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.global_staff_size is None
            True

        Set to number or none.

        Defaults to none.

        Returns number or none.
        """
        return self._global_staff_size

    @property
    def header_block(self):
        """
        Gets header block.

        ..  container:: example

            Gets header block:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.header_block
            <Block(name='header')>

        Returns block or none.
        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == 'header':
                    return item

    @property
    def includes(self):
        """
        Gets includes of LilyPond file.

        ..  container:: example

            Gets includes:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.includes
            []

        Return list
        """
        return self._includes

    @property
    def items(self):
        r"""
        Gets items in LilyPond file.

        ..  container:: example

            Gets items:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> for item in lilypond_file.items:
            ...     item
            ...
            <Block(name='header')>
            <Block(name='layout')>
            <Block(name='paper')>
            <Block(name='score')>

        ..  container:: example

            Accepts strings:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> score_block = abjad.Block(name='score')
            >>> score_block.items.append(staff)
            >>> lilypond_file = abjad.LilyPondFile(
            ...     lilypond_language_token=False,
            ...     lilypond_version_token=False,
            ...     )
            >>> string = r'\customCommand'
            >>> lilypond_file.items.append(string)
            >>> lilypond_file.items.append(score_block)

            >>> abjad.f(lilypond_file)
            \customCommand
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

        ..  container:: example

            Returns list:

            >>> isinstance(lilypond_file.items, list)
            True

        Returns list.
        """
        return self._items

    @property
    def layout_block(self):
        """
        Gets layout block.

        ..  container:: example

            Gets layout block:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.layout_block
            <Block(name='layout')>

        Returns block or none.
        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == 'layout':
                    return item

    @property
    def lilypond_language_token(self):
        """
        Gets LilyPond language token.

        ..  container:: example

            Gets LilyPond language token:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.lilypond_language_token
            LilyPondLanguageToken()

        Returns LilyPond language token or none.
        """
        return self._lilypond_language_token

    @property
    def lilypond_version_token(self):
        """
        Gets LilyPond version token.

        ..  container:: example

            Gets LilyPond version token:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.lilypond_version_token # doctest: +SKIP
            LilyPondVersionToken('2.19.35')

        Returns LilyPond version token or none.
        """
        return self._lilypond_version_token

    @property
    def paper_block(self):
        """
        Gets paper block.

        ..  container:: example

            Gets paper block:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.paper_block
            <Block(name='paper')>

        Returns block or none.
        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == 'paper':
                    return item

    @property
    def score_block(self):
        """
        Gets score block.

        ..  container:: example

            Gets score block:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.score_block
            <Block(name='score')>

        Returns block or none.
        """
        for item in self.items:
            if isinstance(item, Block):
                if item.name == 'score':
                    return item

    @property
    def use_relative_includes(self):
        """
        Is true when LilyPond file should use relative includes.

        ..  container:: example

            Gets relative include flag:

            >>> lilypond_file = abjad.LilyPondFile.new()

            >>> lilypond_file.use_relative_includes is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._use_relative_includes

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        class_,
        music=None,
        date_time_token=None,
        default_paper_size=None,
        comments=None,
        includes=None,
        global_staff_size=None,
        lilypond_language_token=None,
        lilypond_version_token=None,
        use_relative_includes=None,
        ):
        r"""
        Makes basic LilyPond file.

        ..  container:: example

            Makes basic LilyPond file:

            >>> score = abjad.Score([abjad.Staff("c'8 d'8 e'8 f'8")])
            >>> lilypond_file = abjad.LilyPondFile.new(score)
            >>> lilypond_file.header_block.title = abjad.Markup('Missa sexti tonus')
            >>> lilypond_file.header_block.composer = abjad.Markup('Josquin')
            >>> lilypond_file.layout_block.indent = 0
            >>> lilypond_file.paper_block.top_margin = 15
            >>> lilypond_file.paper_block.left_margin = 15

            ::

                >>> abjad.f(lilypond_file) # doctest: +SKIP
                \header {
                    composer = \markup { Josquin }
                    title = \markup { Missa sexti tonus }
                }

                \layout {
                    indent = #0
                }

                \paper {
                    left-margin = #15
                    top-margin = #15
                }

                \score {
                    \new Score <<
                        \new Staff {
                            c'8
                            d'8
                            e'8
                            f'8
                        }
                    >>
                }

            >>> abjad.show(lilypond_file) # doctest: +SKIP

        Wraps ``music`` in LilyPond ``\score`` block.

        Adds LilyPond ``\header``, ``\layout``, ``\paper`` and ``\score``
        blocks to LilyPond file.

        Returns LilyPond file.
        """
        if isinstance(music, LilyPondFile):
            return music
        lilypond_file = class_(
            date_time_token=date_time_token,
            default_paper_size=default_paper_size,
            comments=comments,
            includes=includes,
            items=[
                Block(name='header'),
                Block(name='layout'),
                Block(name='paper'),
                Block(name='score'),
                ],
            global_staff_size=global_staff_size,
            lilypond_language_token=lilypond_language_token,
            lilypond_version_token=lilypond_version_token,
            use_relative_includes=use_relative_includes,
            )
        lilypond_file.header_block.tagline = False
        if music is not None:
            lilypond_file.score_block.items.append(music)
        return lilypond_file

    @classmethod
    def rhythm(
        class_,
        selections,
        divisions=None,
        attach_lilypond_voice_commands=None,
        implicit_scaling=None,
        pitched_staff=None,
        simultaneous_selections=None,
        time_signatures=None,
        ):
        r"""
        Makes rhythm-styled LilyPond file.

        ..  container:: example

            Makes rhythmic staff:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ...     ]
            >>> for selection in selections:
            ...     abjad.attach(abjad.Beam(), selection[:])
            ...
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file[abjad.Score]
                >>> abjad.f(score)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 3/4
                            s1 * 3/4
                        }   % measure
                        {   % measure
                            \time 4/8
                            s1 * 1/2
                        }   % measure
                        {   % measure
                            \time 1/4
                            s1 * 1/4
                        }   % measure
                    }
                    \new RhythmicStaff
                    {
                        {   % measure
                            \time 3/4
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8
                            ]
                        }   % measure
                        {   % measure
                            \time 4/8
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                        }   % measure
                        {   % measure
                            \time 1/4
                            c'8
                            [
                            c'8
                            ]
                        }   % measure
                    }
                >>

        ..  container:: example

            Set time signatures explicitly:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ...     ]
            >>> for selection in selections:
            ...     abjad.attach(abjad.Beam(), selection[:])
            ...
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     [(6, 8), (4, 8), (2, 8)],
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file[abjad.Score]
                >>> abjad.f(score)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 6/8
                            s1 * 3/4
                        }   % measure
                        {   % measure
                            \time 4/8
                            s1 * 1/2
                        }   % measure
                        {   % measure
                            \time 2/8
                            s1 * 1/4
                        }   % measure
                    }
                    \new RhythmicStaff
                    {
                        {   % measure
                            \time 6/8
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8
                            ]
                        }   % measure
                        {   % measure
                            \time 4/8
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                        }   % measure
                        {   % measure
                            \time 2/8
                            c'8
                            [
                            c'8
                            ]
                        }   % measure
                    }
                >>

        ..  container:: example

            Makes pitched staff:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ...     ]
            >>> for selection in selections:
            ...     abjad.attach(abjad.Beam(), selection[:])
            ...
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     pitched_staff=True,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 3/4
                            s1 * 3/4
                        }   % measure
                        {   % measure
                            \time 4/8
                            s1 * 1/2
                        }   % measure
                        {   % measure
                            \time 1/4
                            s1 * 1/4
                        }   % measure
                    }
                    \new Staff
                    {
                        {   % measure
                            \time 3/4
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8
                            ]
                        }   % measure
                        {   % measure
                            \time 4/8
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                        }   % measure
                        {   % measure
                            \time 1/4
                            c'8
                            [
                            c'8
                            ]
                        }   % measure
                    }
                >>

        ..  container:: example

            Makes simultaneous voices:

            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> maker = abjad.NoteMaker()
            >>> selections = [
            ...     maker(6 * [0], [(1, 8)]),
            ...     maker(8 * [0], [(1, 16)]),
            ...     maker(2 * [0], [(1, 8)]),
            ...     ]
            >>> for selection in selections:
            ...     abjad.attach(abjad.Beam(), selection[:])
            ...
            >>> for note in abjad.iterate(selections).components(abjad.Note):
            ...     note.written_pitch = abjad.NamedPitch("e'")
            ...
            >>> selection_1 = selections[0] + selections[1] + selections[2]
            >>> selections = [
            ...     maker(12 * [0], [(1, 16)]),
            ...     maker(16 * [0], [(1, 32)]),
            ...     maker(4 * [0], [(1, 16)]),
            ...     ]
            >>> for selection in selections:
            ...     abjad.attach(abjad.Beam(), selection[:])
            ...
            >>> selection_2 = selections[0] + selections[1] + selections[2]
            >>> selections = {
            ...     'Voice 1': selection_1,
            ...     'Voice 2': selection_2,
            ... }
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> voice_1 = lilypond_file['Voice 1']
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> voice_2 = lilypond_file['Voice 2']
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 3/4
                            s1 * 3/4
                        }   % measure
                        {   % measure
                            \time 4/8
                            s1 * 1/2
                        }   % measure
                        {   % measure
                            \time 1/4
                            s1 * 1/4
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            e'8
                            [
                            e'8
                            e'8
                            e'8
                            e'8
                            e'8
                            ]
                            e'16
                            [
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            ]
                            e'8
                            [
                            e'8
                            ]
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                            c'32
                            [
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            ]
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            ]
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        if isinstance(selections, list):
            for selection in selections:
                if not isinstance(selection, Selection):
                    message = f'must be selection: {selection!r}.'
                    raise TypeError(message)
        elif isinstance(selections, dict):
            for selection in selections.values():
                if not isinstance(selection, Selection):
                    message = f'must be selection: {selection!r}.'
                    raise TypeError(message)
        else:
            message = f'must be list or dictionary: {selections!r}.'
            raise TypeError(message)
        score = Score()
        lilypond_file = LilyPondFile.new(
            score,
            includes=['default.ily', 'rhythm-maker-docs.ily'],
            )
        if pitched_staff is None:
            if isinstance(selections, list):
                selections_ = selections
            elif isinstance(selections, dict):
                selections_ = selections.values()
            else:
                raise TypeError(selections)
            for note in iterate(selections_).leaves(Note):
                if note.written_pitch != NamedPitch("c'"):
                    pitched_staff = True
                    break
        if isinstance(selections, list):
            if divisions is None:
                duration = abjad_inspect(selections).duration()
                divisions = [duration]
            time_signatures = time_signatures or divisions
            maker = MeasureMaker(implicit_scaling=implicit_scaling)
            measures = maker(time_signatures)
            if pitched_staff:
                staff = Staff(measures)
            else:
                staff = Staff(measures, lilypond_type='RhythmicStaff')
            selections = sequence(selections).flatten(depth=-1)
            selections_ = copy.deepcopy(selections)
            try:
                agent = mutate(staff)
                measures = agent.replace_measure_contents(selections)
            except StopIteration:
                if pitched_staff:
                    staff = Staff(selections_)
                else:
                    staff = Staff(
                        selections_,
                        lilypond_type='RhythmicStaff',
                        )
        elif isinstance(selections, dict):
            voices = []
            for voice_name in sorted(selections):
                selections_ = selections[voice_name]
                selections_ = sequence(selections_).flatten(depth=-1)
                selections_ = copy.deepcopy(selections_)
                voice = Voice(selections_, name=voice_name)
                if attach_lilypond_voice_commands:
                    voice_name_to_command_string = {
                        'Voice 1': 'voiceOne',
                        'Voice 2': 'voiceTwo',
                        'Voice 3': 'voiceThree',
                        'Voice 4': 'voiceFour',
                        }
                    command_string = voice_name_to_command_string.get(
                        voice_name,
                        )
                    if command_string:
                        command = LilyPondLiteral('\\' + command_string)
                        attach(command, voice)
                voices.append(voice)
            staff = Staff(voices, is_simultaneous=True)
            if divisions is None:
                duration = abjad_inspect(staff).duration()
                divisions = [duration]
        else:
            message = 'must be list or dictionary of selections:'
            message += f' {selections!r}.'
            raise TypeError(message)
        score.append(staff)
        assert isinstance(divisions, collections.Sequence), repr(divisions)
        time_signatures = time_signatures or divisions
        context = Context(lilypond_type='GlobalContext')
        maker = MeasureMaker(implicit_scaling=implicit_scaling)
        measures = maker(time_signatures)
        context.extend(measures)
        score.insert(0, context)
        return lilypond_file
