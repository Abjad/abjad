import copy
import fractions
import itertools
import sys
import typing

import ply
from ply import lex
from ply.yacc import (
    YaccProduction,
    YaccSymbol,
    error_count,
    format_result,
    format_stack_entry,
)

from .. import _indentlib
from .. import bind as _bind
from .. import duration as _duration
from .. import exceptions as _exceptions
from .. import indicators as _indicators
from .. import lilypondfile as _lilypondfile
from .. import lyconst as _lyconst
from .. import lyenv as _lyenv
from .. import pitch as _pitch
from .. import score as _score
from .. import string as _string
from .. import tag as _tag
from .base import Parser
from .scheme import SchemeParser


class LilyPondDuration:
    """
    Model of a duration in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("duration", "multiplier")

    ### INITIALIZER ###

    def __init__(self, duration=None, multiplier=None):
        self.duration = duration
        self.multiplier = multiplier


_lyenv.current_module["breve"] = LilyPondDuration(_duration.Duration(2, 1), None)
_lyenv.current_module["longa"] = LilyPondDuration(_duration.Duration(4, 1), None)
_lyenv.current_module["maxima"] = LilyPondDuration(_duration.Duration(8, 1), None)


class MarkupCommand:
    """
    LilyPond markup command.
    """

    __slots__ = ("arguments", "name")

    def __init__(self, name=None, *arguments):
        assert isinstance(name, str), repr(name)
        self.name = name
        self.arguments = tuple(arguments)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a markup command with name and arguments equal to
        those of this markup command.
        """
        # defined explicitly because of initializer *arguments
        if isinstance(argument, type(self)):
            if self.name == argument.name:
                if self.arguments == argument.arguments:
                    return True
        return False

    def __hash__(self):
        """
        Hashes markup command.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self):
        """
        Gets repr.
        """
        return (
            f"{type(self).__name__}(name={self.name!r}, arguments={self.arguments!r})"
        )

    def _get_lilypond_format(self):
        def recurse(iterable):
            result = []
            for item in iterable:
                if isinstance(item, list | tuple):
                    result.append("{")
                    result.extend(recurse(item))
                    result.append("}")
                elif isinstance(item, MarkupCommand):
                    string = item._get_lilypond_format()
                    pieces = string.split("\n")
                    result.extend(pieces)
                elif isinstance(item, str) and "\n" in item:
                    result.append('#"')
                    result.extend(item.splitlines())
                    result.append('"')
                else:
                    assert isinstance(item, str), repr(item)
                    result.append(item)
            return [f"{indent}{item}" for item in result]

        indent = _indentlib.INDENT
        parts = [rf"\{self.name}"]
        parts.extend(recurse(self.arguments))
        string = "\n".join(parts)
        return string


class Music:
    """
    Abjad model of the LilyPond AST music node.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("music",)

    ### INITIALIZER ###

    def __init__(self, music=None):
        self.music = music


class ContextSpeccedMusic(Music):
    """
    Abjad model of the LilyPond AST context-specced music node.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        # "context",
        "lilypond_type",
        "music",
        "optional_id",
        "optional_context_mod",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_type=None,
        optional_id=None,
        optional_context_mod=None,
        music=None,
    ):
        lilypond_type = lilypond_type or ""
        music = music or SequentialMusic()
        assert isinstance(music, Music)
        self.lilypond_type = lilypond_type
        self.optional_id = optional_id
        self.optional_context_mod = optional_context_mod
        self.music = music

    ### PUBLIC METHODS ###

    def construct(self):
        """
        Constructs context.

        Returns context.
        """
        if self.lilypond_type in self.known_contexts:
            context = self.known_contexts[self.lilypond_type]([])
        else:
            raise Exception(f"context type not supported: {self.lilypond_type}.")

        if self.optional_id is not None:
            context.name = self.optional_id

        if self.optional_context_mod is not None:
            for x in self.optional_context_mod:
                print(x)
            # TODO: implement context modifications on contexts
            pass

        if isinstance(self.music, SimultaneousMusic):
            context.simultaneous = True
        # context.extend(music.construct())
        context.extend(self.music.construct())

        return context

    ### PUBLIC PROPERTIES ###

    @property
    def known_contexts(self):
        """
        Known contexts.

        Returns dictionary.
        """
        return {
            "ChoirStaff": _score.StaffGroup,
            "GrandStaff": _score.StaffGroup,
            "PianoStaff": _score.StaffGroup,
            "Score": _score.Score,
            "Staff": _score.Staff,
            "StaffGroup": _score.StaffGroup,
            "Voice": _score.Voice,
        }


class GuileProxy:
    """
    Emulates LilyPond music functions.

    Used internally by LilyPondParser.

    Not composer-safe.
    """

    ### CLASS VARIABLES ###

    _function_name_mapping: dict[str, typing.Callable] = {}

    ### INITIALIZER ###

    def __init__(self, client=None, *, tag=None):
        self.client = client
        self.tag = tag

    ### SPECIAL METHODS ###

    def __call__(self, function_name, arguments):
        """
        Calls Guile proxy on ``function_name`` with ``arguments``.

        Returns function output.
        """
        if hasattr(self, function_name[1:]):
            result = getattr(self, function_name[1:])(*arguments)
            return result
        elif function_name[1:] in self._function_name_mapping:
            function_name = function_name[1:]
            result = getattr(self, function_name)(*arguments)
            return result
        message = f"LilyPondParser can not emulate music function: {function_name}."
        raise Exception(message)

    ### FUNCTION EMULATORS ###

    def acciaccatura(self, music):
        r"""
        Handles LilyPond ``\acciaccatura`` command.
        """
        grace = _score.BeforeGraceContainer(
            music[:], command=r"\acciaccatura", tag=self.tag
        )
        return grace

    # afterGrace?

    def appoggiatura(self, music):
        r"""
        Handles LilyPond ``\appoggiatura`` command.
        """
        grace = _score.BeforeGraceContainer(
            music[:], command=r"\appoggiatura", tag=self.tag
        )
        return grace

    def bar(self, string):
        r"""
        Handles LilyPond ``\bar`` command.
        """
        return _indicators.BarLine(string)

    def breathe(self):
        r"""
        Handles LilyPond ``\breathe`` command.
        """
        return _indicators.LilyPondLiteral(r"\breathe", site="after")

    def clef(self, string):
        r"""
        Handles LilyPond ``\clef`` command.
        """
        return _indicators.Clef(string)

    def grace(self, music):
        r"""
        Handles LilyPond ``\grace`` command.
        """
        assert isinstance(music, _score.Container)
        leaves = music[:]
        music[:] = []
        return _score.BeforeGraceContainer(leaves, tag=self.tag)

    def key(self, notename_pitch, number_list):
        r"""
        Handles LilyPond ``\key`` command.
        """
        if number_list is None:
            number_list = "major"
        return _indicators.KeySignature(
            _pitch.NamedPitchClass(notename_pitch), _indicators.Mode(number_list)
        )

    def language(self, string):
        r"""
        Handles LilyPond ``\language`` command.
        """
        if string in self.client._language_pitch_names:
            self.client._pitch_names = self.client._language_pitch_names[string]
        # try reparsing the next note name, if a note name immediately follows
        lookahead = self.client._parser.lookahead
        if lookahead.type == "STRING":
            if lookahead.value in self.client._pitch_names:
                lookahead.type = "NOTENAME_PITCH"
                lookahead.value = _pitch.NamedPitchClass(
                    self.client._pitch_names[lookahead.value]
                )

    def makeClusters(self, music):
        r"""
        Handles LilyPond ``\makeClusters`` command.
        """
        return _score.Cluster(music[:], tag=self.tag)

    def mark(self, label):
        r"""
        Handles LilyPond ``\mark`` command.
        """
        if label is None:
            label = r"\default"
        return _indicators.LilyPondLiteral(r"\mark %s" % label)

    def oneVoice(self):
        r"""
        Handles LilyPond ``\oneVoice`` command.
        """
        return _indicators.VoiceNumber(None)

    # pitchedTrill

    def relative(self, pitch, music):
        r"""
        Handles LilyPond ``\relative`` command.
        """
        # We should always keep track of the last chord entered.
        # When there are repeated chords (via q),
        # we add the last chord as a key in a _repeated_chords dictionary.
        # Then, we associate a list with the chord "key" in the dict,
        # and append a reference to the repeated chord.

        # Should the referenced chord appear in a relative block,
        # we relativize that chord, and update any repeated chords
        # we've added to its list of referencing chords.

        # The parser's "last_chord" variable will now reflect the
        # relativized pitches of the original referenced chord,
        # and so any new chord repetitions following the \relative block
        # should result in matching absolute pitches to both the "last_chord"
        # and any other repetitions.

        if self._is_unrelativable(music):
            return music

        def recurse(component, pitch):
            if self._is_unrelativable(component):
                return pitch
            elif isinstance(component, _score.Chord | _score.Note):
                pitch = self._make_relative_leaf(component, pitch)
                if component in self.client._repeated_chords:
                    for repeated_chord in self.client._repeated_chords[component]:
                        repeated_chord.written_pitches = component.written_pitches
            elif isinstance(component, _score.Container):
                for child in component:
                    pitch = recurse(child, pitch)
            return pitch

        pitch = recurse(music, pitch)

        self._make_unrelativable(music)

        return music

    def skip(self, duration):
        r"""
        Handles LilyPond ``\skip`` command.
        """
        leaf = _score.Skip(duration.duration, tag=self.tag)
        if duration.multiplier is not None:
            _bind._unsafe_attach(duration.multiplier, leaf)
        return leaf

    def slashed_grace_container(self, music):
        r"""
        Handles LilyPond ``\slashedGrace`` command.
        """
        grace = _score.BeforeGraceContainer(music[:], tag=self.tag)
        return grace

    def time(self, number_list, fraction):
        r"""
        Handles LilyPond ``\time`` command.
        """
        n, d = fraction.numerator, fraction.denominator
        return _indicators.TimeSignature((n, d))

    def times(self, fraction, music):
        r"""
        Handles LilyPond ``\times`` command.
        """
        n, d = fraction.numerator, fraction.denominator
        if not isinstance(music, _score.Context) and not isinstance(music, _score.Leaf):
            assert isinstance(music, _score.Container), repr(music)
            leaves = music[:]
            music[:] = []
            return _score.Tuplet((n, d), leaves, tag=self.tag)
        return _score.Tuplet((n, d), [music], tag=self.tag)

    def transpose(self, from_pitch, to_pitch, music):
        r"""
        Handles LilyPond ``\transpose`` command.
        """

        def recurse(music):
            key_signatures = music._get_indicators(_indicators.KeySignature)
            if key_signatures:
                for key_signature in key_signatures:
                    new_tonic = _pitch.NamedPitch((key_signature.tonic.name, 4))
                    new_tonic = LilyPondParser._transpose_enharmonically(
                        from_pitch, to_pitch, new_tonic
                    ).pitch_class
                    new_key_signature = _indicators.KeySignature(
                        new_tonic, key_signature.mode
                    )
                    _bind.detach(key_signature, music)
                    _bind._unsafe_attach(new_key_signature, music)
            if isinstance(music, _score.Note):
                music.written_pitch = LilyPondParser._transpose_enharmonically(
                    from_pitch, to_pitch, music.written_pitch
                )
            elif isinstance(music, _score.Chord):
                for note_head in music.note_heads:
                    note_head.written_pitch = LilyPondParser._transpose_enharmonically(
                        from_pitch, to_pitch, note_head.written_pitch
                    )
            elif isinstance(music, _score.Container):
                for component in music:
                    recurse(component)

        self._make_unrelativable(music)
        recurse(music)
        return music

    # transposition

    def tuplet(self, fraction, _optional, music):
        r"""
        Handles LilyPond ``\tuplet`` command.

        The ``_optional`` parameter appears to get passed in but is unused.
        """
        n, d = fraction.numerator, fraction.denominator
        string = f"{n}:{d}"
        if not isinstance(music, _score.Context) and not isinstance(music, _score.Leaf):
            assert isinstance(music, _score.Container), repr(music)
            leaves = music[:]
            music[:] = []
            return _score.Tuplet(string, leaves, tag=self.tag)
        return _score.Tuplet(string, [music], tag=self.tag)

    # tweak

    def voiceFour(self):
        r"""
        Handles LilyPond ``\voiceFour`` command.
        """
        return _indicators.VoiceNumber(4)

    def voiceOne(self):
        r"""
        Handles LilyPond ``\voiceOnce`` command.
        """
        return _indicators.VoiceNumber(1)

    def voiceThree(self):
        r"""
        Handles LilyPond ``\voiceThree`` command.
        """
        return _indicators.VoiceNumber(3)

    def voiceTwo(self):
        r"""
        Handles LilyPond ``\voiceTwo`` command.
        """
        return _indicators.VoiceNumber(2)

    ### HELPER FUNCTIONS ###

    def _is_unrelativable(self, music):
        annotations = music._get_indicators(dict)
        keys = [list(_.keys())[0] for _ in annotations]
        if "UnrelativableMusic" in keys:
            return True
        return False

    def _make_relative_leaf(self, leaf, pitch):
        if self._is_unrelativable(leaf):
            return pitch
        elif isinstance(leaf, _score.Note):
            pitch = self._to_relative_octave(leaf.written_pitch, pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, _score.Chord):
            # TODO: This is not ideal w/r/t post events as LilyPond does
            # not sort chord contents
            chord_pitches = self.client._chord_pitch_orders[leaf]
            for i, chord_pitch in enumerate(chord_pitches):
                pitch = self._to_relative_octave(chord_pitch, pitch)
                chord_pitches[i] = pitch
            leaf.written_pitches = chord_pitches
            pitch = min(leaf.written_pitches)
        return pitch

    def _make_unrelativable(self, music):
        if not self._is_unrelativable(music):
            annotation = {"UnrelativableMusic": True}
            _bind._unsafe_attach(annotation, music)

    @staticmethod
    def _get_default_absolute_pitch(pitch, reference):
        pitch_name = pitch.pitch_class.name
        reference_octave = reference.octave.number
        absolute_pitch = _pitch.NamedPitch((pitch_name, reference_octave))
        reference_pc_number = reference._get_diatonic_pc_number()
        pitch_pc_number = pitch._get_diatonic_pc_number()
        number_of_diatonic_pitches = 7
        diatonic_interval_up = (
            pitch_pc_number - reference_pc_number
        ) % number_of_diatonic_pitches
        diatonic_interval_down = (
            number_of_diatonic_pitches - diatonic_interval_up
        ) % number_of_diatonic_pitches
        expect_higher_than_reference = (
            diatonic_interval_up < diatonic_interval_down
            or diatonic_interval_up == diatonic_interval_down
            and pitch.accidental > reference.accidental
        )
        if expect_higher_than_reference and absolute_pitch < reference:
            octave_transposition = 1
        elif not expect_higher_than_reference and absolute_pitch > reference:
            octave_transposition = -1
        else:
            octave_transposition = 0
        absolute_pitch.octave.number += octave_transposition
        return absolute_pitch

    @staticmethod
    def _apply_octave_transposition(pitch, absolute_pitch):
        base_octave = 3
        octave_transposition = pitch.octave.number - base_octave
        absolute_pitch.octave.number += octave_transposition
        return absolute_pitch

    @classmethod
    def _to_relative_octave(cls, pitch, reference):
        default_absolute_pitch = cls._get_default_absolute_pitch(pitch, reference)
        return cls._apply_octave_transposition(pitch, default_absolute_pitch)


class LilyPondEvent:
    """
    Model of an arbitrary event in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    """

    ### INITIALIZER ###

    def __init__(self, name=None, **keywords):
        self.name = name
        for k, v in keywords.items():
            if k != "name":
                setattr(self, k, v)

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation of LilyPond event.
        """
        result = repr(self.name)
        for key in self.__dict__:
            if key == "name":
                continue
            result += f", {key} = {getattr(self, key)!r}"
        name = type(self).__name__
        return f"{name}({result})"


class LilyPondFraction:
    """
    Model of a fraction in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("numerator", "denominator")

    ### INITIALIZER ###

    def __init__(self, numerator=0, denominator=1):
        self.numerator = numerator
        self.denominator = denominator


class LilyPondGrammarGenerator:
    """
    Generates a syntax skeleton from LilyPond grammar files.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, skeleton_path, parser_output_path, parser_tab_hh_path):
        """
        Calls LilyPond grammar generator.
        """
        self._write_parser_syntax_skeleton(
            self, skeleton_path, parser_output_path, parser_tab_hh_path
        )

    ### PRIVATE METHODS ###

    def _extract_productions_from_parser_output(self, file_path):
        with open(file_path, "r") as f:
            lines = f.read().split("\n")
        productions = {}
        nonterminal = None
        in_grammar = False
        for line in lines:
            text = line.strip()
            # starting and stopping
            if text == "Terminals, with rules where they appear":
                break
            elif text == "Grammar":
                in_grammar = True
                continue
            if not in_grammar:
                continue
            if not text:
                continue
            parts = text.split()[1:]
            if parts[0].startswith("$"):
                continue
            elif parts[0] == "|":
                right_hand = filter(lambda x: not x.startswith("$"), parts[1:])
                productions[nonterminal].append(parts[1:])
            else:
                nonterminal = parts[0][:-1]
                if nonterminal not in productions:
                    productions[nonterminal] = []
                right_hand = parts[1:]
                if right_hand[0] == "/*":  # /* empty */
                    productions[nonterminal].append([])
                else:
                    right_hand = filter(lambda x: not x.startswith("$"), right_hand)
                    productions[nonterminal].append(right_hand)
        return productions

    def _extract_token_names_from_parser_tab_hh(self, file_path):
        with open(file_path, "r") as f:
            lines = f.read().split("\n")
        token_names = {}
        in_enum = False
        for line in lines:
            text = line.strip()
            if in_enum and text == "};":
                break
            if in_enum:
                parts = text.split(" ")
                name = parts[0]
                if parts[2].endswith(","):
                    number = int(parts[2][:-1])
                else:
                    number = int(parts[2])
                token_names[number] = name
            if text == "enum yytokentype {":
                in_enum = True
        return token_names

    def _extract_token_values_from_parser_output(self, file_path):
        with open(file_path, "r") as f:
            lines = f.read().split("\n")
        token_values = {}
        in_token_list = False
        for line in lines:
            text = line.strip()
            if in_token_list and text == "Nonterminals, with rules where they appear":
                break
            elif text == "Terminals, with rules where they appear":
                in_token_list = True
                continue
            elif not text:
                continue
            elif not in_token_list:
                continue
            parts = text.split()
            if parts[0].isdigit():
                continue
            elif parts[0].startswith("$"):
                continue
            value = parts[0]
            number = int(parts[1][1:-1])
            token_values[number] = value
        return token_values

    def _generate_production_map(self, output_path, tab_hh_path):
        productions = self._extract_productions_from_parser_output(output_path)
        names = self._extract_token_names_from_parser_tab_hh(tab_hh_path)
        values = self._extract_token_values_from_parser_output(output_path)
        matches = self._match_token_names_with_token_values(names, values)
        rewrites = {}
        for nonterminal in productions:
            for rh in productions[nonterminal]:
                for i, r in enumerate(rh):
                    if r in matches:
                        rh[i] = matches[r]
                string = " ".join(rh)
                docstring = f"{nonterminal} : {string}"
                for i, r in enumerate(rh):
                    if r[0] == "'" and r[-1] == "'":
                        rh[i] = f"Chr{ord(r[-2])}"
                string = "__".join(rh)
                funcname = f"p_{nonterminal}__{string}"
                rewrites[funcname] = docstring
        return rewrites

    def _match_token_names_with_token_values(self, names, values):
        matches = {}
        for number, value in values.items():
            if number in names:
                name = names[number]
                matches[value] = name
        return matches

    def _write_parser_syntax_skeleton(
        self, skeleton_path, parser_output_path, parser_tab_hh_path
    ):
        productions = self._generate_production_map(
            parser_output_path, parser_tab_hh_path
        )
        with open(skeleton_path, "w") as f:
            f.write("from abjad.parsers.parser import SyntaxNode as Node \\\n")
            f.write("class _LilyPondSyntacticalDefinition:\n\n")
            f.write("    def __init__(self, client):\n")
            f.write("        self.client = client\n")
            f.write("        self.tokens = self.client.lexdef.tokens\n\n\n")
            f.write("    start_symbol = 'start_symbol'\n\n\n")
            f.write("    precedence = (\n")
            f.write("        ('nonassoc', 'COMPOSITE'),\n")
            f.write("        ('nonassoc', 'REPEAT'),\n")
            f.write("        ('nonassoc', 'ALTERNATIVE'),\n")
            f.write("        ('left', 'ADDLYRICS'),\n")
            f.write("        ('nonassoc', 'DEFAULT'),\n")
            f.write("        ('nonassoc', 'FUNCTION_ARGLIST'),\n")
            f.write(
                "        ('right', 'PITCH_IDENTIFIER', 'NOTENAME_PITCH',"
                " 'TONICNAME_PITCH', 'UNSIGNED', 'REAL', 'DURATION_IDENTIFIER', ':'),\n"
            )
            f.write("        ('nonassoc', 'NUMBER_IDENTIFIER', '/'),\n")
            f.write("    )\n\n\n")
            f.write("    ### SYNTACTICAL RULES (ALPHABETICAL) ###\n\n\n")
            current_nonterminal = "start_symbol"
            ly_keys = sorted(
                key for key in productions if key.startswith("p_start_symbol")
            )
            for key in ly_keys:
                funcname = key
                docstring = productions[key]
                f.write(f"    def {funcname}(self, p):\n")
                f.write(f"        {docstring!r}\n")
                f.write(f"        p[0] = Node('{current_nonterminal}', p[1:])\n\n\n")
            for funcname, docstring in sorted(productions.items()):
                nonterminal = funcname.split("__")[0][2:]
                if nonterminal == "start_symbol":
                    continue
                if nonterminal != current_nonterminal:
                    current_nonterminal = nonterminal
                    f.write(f"    ### {current_nonterminal} ###\n\n\n")
                f.write(f"    def {funcname}(self, p):\n")
                f.write(f"        {docstring!r}\n")
                f.write(f"        p[0] = Node('{current_nonterminal}', p[1:])\n\n\n")
            f.write("    def p_error(self, p):\n")
            f.write("        pass\n\n")


def _parse(self, input=None, lexer=None, debug=None, tracking=0, tokenfunc=None):
    self.lookahead = None  # Current lookahead symbol
    actions = self.action  # Local reference to action table (to avoid lookup on self.)
    goto = self.goto  # Local reference to goto table (to avoid lookup on self.)
    prod = (
        self.productions
    )  # Local reference to production list (to avoid lookup on self.)
    pslice = YaccProduction(None)  # Production object passed to grammar rules
    errorcount = 0  # Used during error recovery

    # --! DEBUG
    # debug.info("PLY: PARSE DEBUG START")
    # --! DEBUG

    # Set up the lexer and parser objects on pslice
    pslice.lexer = lexer
    pslice.parser = self

    # If input was supplied, pass to lexer
    if input is not None:
        lexer.input(input)

    if tokenfunc is None:
        # Tokenize function
        get_token = lexer.token
    else:
        get_token = tokenfunc

    # Set up the state and symbol stacks

    lookaheadstack = []  # Stack of lookahead tokens
    self.lookaheadstack = lookaheadstack
    statestack = []  # Stack of parsing states
    self.statestack = statestack
    symstack = []  # Stack of grammar symbols
    self.symstack = symstack

    pslice.stack = symstack  # Put in the production
    errtoken = None  # Err token

    # The start state is assumed to be (0,$end)

    statestack.append(0)
    sym = YaccSymbol()
    sym.type = "$end"
    symstack.append(sym)
    state = 0
    while 1:
        # Get the next symbol on the input.  If a lookahead symbol
        # is already set, we just use that. Otherwise, we'll pull
        # the next token off of the lookaheadstack or from the lexer

        # --! DEBUG
        # debug.debug('')
        # debug.debug('State  : %s', state)
        # --! DEBUG

        if not self.lookahead:
            if not self.lookaheadstack:
                self.lookahead = get_token()  # Get the next token
            else:
                self.lookahead = self.lookaheadstack.pop()
            if not self.lookahead:
                self.lookahead = YaccSymbol()
                self.lookahead.type = "$end"

        # --! DEBUG
        # debug.debug('Stack  : %s',
        #             ("%s . %s" % (" ".join([xx.type for xx in symstack][1:]), str(self.lookahead))).lstrip())
        # --! DEBUG

        # Check the action table
        ltype = self.lookahead.type
        t = actions[state].get(ltype)

        # This is a bad hack to deal with LilyPond's backup/reparse regime
        if t is None:
            a = set(actions[state].values())
            if 1 == len(a):
                t = list(a)[0]

        if t is not None:
            if t > 0:
                # shift a symbol on the stack
                statestack.append(t)
                state = t

                # --! DEBUG
                # debug.debug("Action : Shift and goto state %s", t)
                # --! DEBUG

                symstack.append(self.lookahead)
                self.lookahead = None

                # Decrease error count on successful shift
                if errorcount:
                    errorcount -= 1
                continue

            if t < 0:
                # reduce a symbol on the stack, emit a production
                p = prod[-t]
                pname = p.name
                plen = p.len

                # Get production function
                sym = YaccSymbol()
                sym.type = pname  # Production name
                sym.value = None

                # --! DEBUG
                # if plen:
                #     debug.info("Action : Reduce rule [%s] with %s and goto state %d", p.str, "["+",".join([format_stack_entry(_v.value) for _v in symstack[-plen:]])+"]",-t)
                # else:
                #     debug.info("Action : Reduce rule [%s] with %s and goto state %d", p.str, [],-t)
                #
                # --! DEBUG

                if plen:
                    targ = symstack[-plen - 1 :]
                    targ[0] = sym

                    # --! TRACKING
                    if tracking:
                        t1 = targ[1]
                        sym.lineno = t1.lineno
                        sym.lexpos = t1.lexpos
                        t1 = targ[-1]
                        sym.endlineno = getattr(t1, "endlineno", t1.lineno)
                        sym.endlexpos = getattr(t1, "endlexpos", t1.lexpos)

                    # --! TRACKING

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated
                    # below as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ

                    try:
                        # Call the grammar rule with our special slice object
                        del symstack[-plen:]
                        del statestack[-plen:]
                        p.callable(pslice)
                        # --! DEBUG
                        # debug.info("Result : %s", format_result(pslice[0]))
                        # --! DEBUG
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        self.lookaheadstack.append(self.lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = "error"
                        self.lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                else:
                    # --! TRACKING
                    if tracking:
                        sym.lineno = lexer.lineno
                        sym.lexpos = lexer.lexpos
                    # --! TRACKING

                    targ = [sym]

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated
                    # above as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ

                    try:
                        # Call the grammar rule with our special slice object
                        p.callable(pslice)
                        # --! DEBUG
                        # debug.info("Result : %s", format_result(pslice[0]))
                        # --! DEBUG
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        self.lookaheadstack.append(self.lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = "error"
                        self.lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if t == 0:
                n = symstack[-1]
                result = getattr(n, "value", None)
                # --! DEBUG
                # debug.info("Done   : Returning %s", format_result(result))
                # debug.info("PLY: PARSE DEBUG END")
                # --! DEBUG
                return result

        if t is None:
            # --! DEBUG
            # debug.error('Error  : %s',
            #             ("%s . %s" % (" ".join([xx.type for xx in symstack][1:]), str(self.lookahead))).lstrip())
            # --! DEBUG

            # We have some kind of parsing error here.  To handle
            # this, we are going to push the current token onto
            # the tokenstack and replace it with an 'error' token.
            # If there are any synchronization rules, they may
            # catch it.
            #
            # In addition to pushing the error token, we call call
            # the user defined p_error() function if this is the
            # first syntax error.  This function is only called if
            # errorcount == 0.
            if errorcount == 0 or self.errorok:
                errorcount = error_count
                self.errorok = 0
                errtoken = self.lookahead
                if errtoken.type == "$end":
                    errtoken = None  # End of file!
                if self.errorfunc:
                    global errok, token, restart
                    errok = (
                        self.errok
                    )  # Set some special functions available in error recovery
                    token = get_token
                    restart = self.restart
                    if errtoken and not hasattr(errtoken, "lexer"):
                        errtoken.lexer = lexer
                    tok = self.errorfunc(errtoken)
                    del errok, token, restart  # Delete special functions

                    if self.errorok:
                        # User must have done some kind of panic
                        # mode recovery on their own.  The
                        # returned token is the next self.lookahead
                        self.lookahead = tok
                        errtoken = None
                        continue
                else:
                    if errtoken:
                        if hasattr(errtoken, "lineno"):
                            lineno = self.lookahead.lineno
                        else:
                            lineno = 0
                        if lineno:
                            sys.stderr.write(
                                "yacc: Syntax error at line %d, token=%s\n"
                                % (lineno, errtoken.type)
                            )
                        else:
                            sys.stderr.write(
                                "yacc: Syntax error, token=%s" % errtoken.type
                            )
                    else:
                        sys.stderr.write("yacc: Parse error in input. EOF\n")
                        return

            else:
                errorcount = error_count

            # case 1:  the statestack only has 1 entry on it.  If we're in this state, the
            # entire parse has been rolled back and we're completely hosed.   The token is
            # discarded and we just keep going.

            if len(statestack) <= 1 and self.lookahead.type != "$end":
                self.lookahead = None
                errtoken = None
                state = 0
                # Nuke the pushback stack
                del self.lookaheadstack[:]
                continue

            # case 2: the statestack has a couple of entries on it, but we're
            # at the end of the file. nuke the top entry and generate an error token

            # Start nuking entries on the stack
            if self.lookahead.type == "$end":
                # Whoa. We're really hosed here. Bail out
                return

            if self.lookahead.type != "error":
                sym = symstack[-1]
                if sym.type == "error":
                    # Hmmm: error is on top of stack, we'll just nuke input
                    # symbol and continue
                    self.lookahead = None
                    continue
                t = YaccSymbol()
                t.type = "error"
                if hasattr(self.lookahead, "lineno"):
                    t.lineno = self.lookahead.lineno
                t.value = self.lookahead
                self.lookaheadstack.append(self.lookahead)
                self.lookahead = t
            else:
                symstack.pop()
                statestack.pop()
                state = statestack[-1]  # Potential bug fix

            continue

        # Call an error function here
        raise RuntimeError("yacc: internal parser error!!!\n")


def _parse_debug(self, input=None, lexer=None, debug=None, tracking=0, tokenfunc=None):
    self.lookahead = None  # Current lookahead symbol
    actions = self.action  # Local reference to action table (to avoid lookup on self.)
    goto = self.goto  # Local reference to goto table (to avoid lookup on self.)
    prod = (
        self.productions
    )  # Local reference to production list (to avoid lookup on self.)
    pslice = YaccProduction(None)  # Production object passed to grammar rules
    errorcount = 0  # Used during error recovery

    # --! DEBUG
    debug.info("PLY: PARSE DEBUG START")
    # --! DEBUG

    # Set up the lexer and parser objects on pslice
    pslice.lexer = lexer
    pslice.parser = self

    # If input was supplied, pass to lexer
    if input is not None:
        lexer.input(input)

    if tokenfunc is None:
        # Tokenize function
        get_token = lexer.token
    else:
        get_token = tokenfunc

    # Set up the state and symbol stacks

    lookaheadstack = []  # Stack of lookahead tokens
    self.lookaheadstack = lookaheadstack
    statestack = []  # Stack of parsing states
    self.statestack = statestack
    symstack = []  # Stack of grammar symbols
    self.symstack = symstack

    pslice.stack = symstack  # Put in the production
    errtoken = None  # Err token

    # The start state is assumed to be (0,$end)

    statestack.append(0)
    sym = YaccSymbol()
    sym.type = "$end"
    symstack.append(sym)
    state = 0
    while 1:
        # Get the next symbol on the input.  If a lookahead symbol
        # is already set, we just use that. Otherwise, we'll pull
        # the next token off of the lookaheadstack or from the lexer

        # --! DEBUG
        debug.debug("")
        debug.debug("State  : %s", state)
        # --! DEBUG

        if not self.lookahead:
            if not self.lookaheadstack:
                self.lookahead = get_token()  # Get the next token
            else:
                self.lookahead = self.lookaheadstack.pop()
            if not self.lookahead:
                self.lookahead = YaccSymbol()
                self.lookahead.type = "$end"

        # --! DEBUG
        debug.debug(
            "Stack  : %s",
            (
                "%s . %s"
                % (
                    " ".join([xx.type for xx in symstack][1:]),
                    str(self.lookahead),
                )
            ).lstrip(),
        )
        # --! DEBUG

        # Check the action table
        ltype = self.lookahead.type
        t = actions[state].get(ltype)

        # This is a bad hack to deal with LilyPond's backup/reparse regime
        if t is None:
            a = set(actions[state].values())
            if 1 == len(a):
                t = list(a)[0]

        if t is not None:
            if t > 0:
                # shift a symbol on the stack
                statestack.append(t)
                state = t

                # --! DEBUG
                debug.debug("Action : Shift and goto state %s", t)
                # --! DEBUG

                symstack.append(self.lookahead)
                self.lookahead = None

                # Decrease error count on successful shift
                if errorcount:
                    errorcount -= 1
                continue

            if t < 0:
                # reduce a symbol on the stack, emit a production
                p = prod[-t]
                pname = p.name
                plen = p.len

                # Get production function
                sym = YaccSymbol()
                sym.type = pname  # Production name
                sym.value = None

                # --! DEBUG
                if plen:
                    debug.info(
                        "Action : Reduce rule [%s] with %s and goto state %d",
                        p.str,
                        "["
                        + ",".join(
                            [format_stack_entry(_v.value) for _v in symstack[-plen:]]
                        )
                        + "]",
                        -t,
                    )
                else:
                    debug.info(
                        "Action : Reduce rule [%s] with %s and goto state %d",
                        p.str,
                        [],
                        -t,
                    )
                # --! DEBUG

                if plen:
                    targ = symstack[-plen - 1 :]
                    targ[0] = sym

                    # --! TRACKING
                    if tracking:
                        t1 = targ[1]
                        sym.lineno = t1.lineno
                        sym.lexpos = t1.lexpos
                        t1 = targ[-1]
                        sym.endlineno = getattr(t1, "endlineno", t1.lineno)
                        sym.endlexpos = getattr(t1, "endlexpos", t1.lexpos)

                    # --! TRACKING

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated
                    # below as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ

                    try:
                        # Call the grammar rule with our special slice object
                        del symstack[-plen:]
                        del statestack[-plen:]
                        p.callable(pslice)
                        # --! DEBUG
                        debug.info("Result : %s", format_result(pslice[0]))
                        # --! DEBUG
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        self.lookaheadstack.append(self.lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = "error"
                        self.lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                else:
                    # --! TRACKING
                    if tracking:
                        sym.lineno = lexer.lineno
                        sym.lexpos = lexer.lexpos
                    # --! TRACKING

                    targ = [sym]

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # The code enclosed in this section is duplicated
                    # above as a performance optimization.  Make sure
                    # changes get made in both locations.

                    pslice.slice = targ

                    try:
                        # Call the grammar rule with our special slice object
                        p.callable(pslice)
                        # --! DEBUG
                        debug.info("Result : %s", format_result(pslice[0]))
                        # --! DEBUG
                        symstack.append(sym)
                        state = goto[statestack[-1]][pname]
                        statestack.append(state)
                    except SyntaxError:
                        # If an error was set. Enter error recovery state
                        self.lookaheadstack.append(self.lookahead)
                        symstack.pop()
                        statestack.pop()
                        state = statestack[-1]
                        sym.type = "error"
                        self.lookahead = sym
                        errorcount = error_count
                        self.errorok = 0
                    continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if t == 0:
                n = symstack[-1]
                result = getattr(n, "value", None)
                # --! DEBUG
                debug.info("Done   : Returning %s", format_result(result))
                debug.info("PLY: PARSE DEBUG END")
                # --! DEBUG
                return result

        if t is None:
            # --! DEBUG
            debug.error(
                "Error  : %s",
                (
                    "%s . %s"
                    % (
                        " ".join([xx.type for xx in symstack][1:]),
                        str(self.lookahead),
                    )
                ).lstrip(),
            )
            # --! DEBUG

            # We have some kind of parsing error here.  To handle
            # this, we are going to push the current token onto
            # the tokenstack and replace it with an 'error' token.
            # If there are any synchronization rules, they may
            # catch it.
            #
            # In addition to pushing the error token, we call call
            # the user defined p_error() function if this is the
            # first syntax error.  This function is only called if
            # errorcount == 0.
            if errorcount == 0 or self.errorok:
                errorcount = error_count
                self.errorok = 0
                errtoken = self.lookahead
                if errtoken.type == "$end":
                    errtoken = None  # End of file!
                if self.errorfunc:
                    global errok, token, restart
                    errok = (
                        self.errok
                    )  # Set some special functions available in error recovery
                    token = get_token
                    restart = self.restart
                    if errtoken and not hasattr(errtoken, "lexer"):
                        errtoken.lexer = lexer
                    tok = self.errorfunc(errtoken)
                    del errok, token, restart  # Delete special functions

                    if self.errorok:
                        # User must have done some kind of panic
                        # mode recovery on their own.  The
                        # returned token is the next self.lookahead
                        self.lookahead = tok
                        errtoken = None
                        continue
                else:
                    if errtoken:
                        if hasattr(errtoken, "lineno"):
                            lineno = self.lookahead.lineno
                        else:
                            lineno = 0
                        if lineno:
                            sys.stderr.write(
                                "yacc: Syntax error at line %d, token=%s\n"
                                % (lineno, errtoken.type)
                            )
                        else:
                            sys.stderr.write(
                                "yacc: Syntax error, token=%s" % errtoken.type
                            )
                    else:
                        sys.stderr.write("yacc: Parse error in input. EOF\n")
                        return

            else:
                errorcount = error_count

            # case 1:  the statestack only has 1 entry on it.  If we're in this state, the
            # entire parse has been rolled back and we're completely hosed.   The token is
            # discarded and we just keep going.

            if len(statestack) <= 1 and self.lookahead.type != "$end":
                self.lookahead = None
                errtoken = None
                state = 0
                # Nuke the pushback stack
                del self.lookaheadstack[:]
                continue

            # case 2: the statestack has a couple of entries on it, but we're
            # at the end of the file. nuke the top entry and generate an error token

            # Start nuking entries on the stack
            if self.lookahead.type == "$end":
                # Whoa. We're really hosed here. Bail out
                return

            if self.lookahead.type != "error":
                sym = symstack[-1]
                if sym.type == "error":
                    # Hmmm: error is on top of stack, we'll just nuke input
                    # symbol and continue
                    self.lookahead = None
                    continue
                t = YaccSymbol()
                t.type = "error"
                if hasattr(self.lookahead, "lineno"):
                    t.lineno = self.lookahead.lineno
                t.value = self.lookahead
                self.lookaheadstack.append(self.lookahead)
                self.lookahead = t
            else:
                symstack.pop()
                statestack.pop()
                state = statestack[-1]  # Potential bug fix

            continue

        # Call an error function here
        raise RuntimeError("yacc: internal parser error!!!\n")


class LilyPondLexicalDefinition:
    """
    The lexical definition of LilyPond's syntax.

    Effectively equivalent to LilyPond's ``lexer.ll`` file.

    Not composer-safe.

    Used internally by ``LilyPondParser``.
    """

    ### INITIALIZER ###

    def __init__(self, client=None, *, tag: _tag.Tag | None = None):
        self.client = client
        self.tag = tag

    states = (
        # lexer.ll:115
        # ('extratoken', 'exclusive'),
        # ('chords', 'exclusive'),
        # ('figures', 'exclusive'),
        # ('incl', 'exclusive'),
        # ('lyrics', 'exclusive'),
        # ('lyric_quote ', 'exclusive'),
        ("longcomment", "exclusive"),
        ("markup", "exclusive"),
        ("notes", "exclusive"),
        ("quote", "exclusive"),
        # ('sourcefileline', 'exclusive'),
        # ('sourcefilename', 'exclusive'),
        ("version", "exclusive"),
        ("scheme", "exclusive"),
    )

    # lexer.ll:129
    A = r"[a-zA-Z\200-\377]"
    AA = r"(%s|_)" % A
    N = r"[0-9]"
    AN = r"(%s|%s)" % (AA, N)
    ANY_CHAR = r"(.|\n)"
    PUNCT = r"[?!:'`]"
    ACCENT = r"""\\[`'"^]"""
    NATIONAL = r"[\001-\006\021-\027\031\036]"
    TEX = r"%s|-|%s|%s|%s" % (AA, PUNCT, ACCENT, NATIONAL)
    WORD = r"%s%s*" % (A, AN)
    DASHED_WORD = r"%s(%s|-)*" % (A, AN)
    DASHED_KEY_WORD = r"\\%s" % DASHED_WORD

    # lexer.ll:144
    ALPHAWORD = r"%s+" % A
    DIGIT = r"%s" % N
    UNSIGNED = r"%s+" % N
    INT = r"(-?%s)" % UNSIGNED
    REAL = r"((%s\.%s*)|(-?\.%s+))" % (INT, N, N)
    E_UNSIGNED = r"\\%s+" % N
    FRACTION = r"%s+\/%s+" % (N, N)
    KEYWORD = r"\\%s" % WORD
    WHITE = r"[ \n\t\f\r]"  # only whitespace
    HORIZONTALWHITE = r"[ \t]"  # only non-line-breaking whitespace
    BLACK = r"[^ \n\t\f\r]"  # only non-whitespace
    RESTNAME = r"[rs]"
    NOTECOMMAND = r"\\%s+" % A
    MARKUPCOMMAND = r"\\(%s|[-_])+" % A
    LYRICS = r"(%s|%s)[^0-9 \t\n\r\f]*" % (AA, TEX)
    ESCAPED = r"""[nt\\'"]"""
    EXTENDER = r"__"
    HYPHEN = r"--"
    BOM_UTF8 = r"\357\273\277"

    keywords = {
        # parser.yy:182, lily-lexer.cc:39
        #        '\\accepts': 'ACCEPTS',
        #        '\\addlyrics': 'ADDLYRICS',
        #        '\\alias': 'ALIAS',
        #        '\\alternative': 'ALTERNATIVE',
        #        '\\book': 'BOOK',
        #        '\\bookpart': 'BOOKPART',
        "\\change": "CHANGE",
        #        '\\chordmode': 'CHORDMODE',
        #        '\\chords': 'CHORDS',
        #        '\\consists': 'CONSISTS',
        "\\context": "CONTEXT",
        "\\default": "DEFAULT",
        #        '\\defaultchild': 'DEFAULTCHILD',
        #        '\\denies': 'DENIES',
        #        '\\description': 'DESCRIPTION',
        #        '\\drummode': 'DRUMMODE',
        #        '\\drums': 'DRUMS',
        #        '\\figuremode': 'FIGUREMODE',
        #        '\\figures': 'FIGURES',
        "\\header": "HEADER",
        #        '\\version-error': 'INVALID',
        "\\layout": "LAYOUT",
        #        '\\lyricmode': 'LYRICMODE',
        #        '\\lyrics': 'LYRICS',
        #        '\\lyricsto': 'LYRICSTO',
        "\\markup": "MARKUP",
        "\\markuplist": "MARKUPLIST",
        "\\midi": "MIDI",
        #        '\\name': 'NAME',
        #        '\\notemode': 'NOTEMODE',
        "\\override": "OVERRIDE",
        "\\paper": "PAPER",
        #        '\\remove': 'REMOVE',
        #        '\\repeat': 'REPEAT',
        "\\rest": "REST",
        "\\revert": "REVERT",
        "\\score": "SCORE",
        "\\sequential": "SEQUENTIAL",
        "\\set": "SET",
        "\\simultaneous": "SIMULTANEOUS",
        "\\tempo": "TEMPO",
        #        '\\type': 'TYPE',
        "\\unset": "UNSET",
        "\\with": "WITH",
        # parser.yy:233
        "\\new": "NEWCONTEXT",
        # ???
        #        '\\objectid': 'OBJECTID',
    }

    tokens = [
        #        'CHORD_BASS', # "/+"
        #        'CHORD_CARET', # "^"
        #        'CHORD_COLON', # ":"
        #        'CHORD_MINUS', # "-"
        #        'CHORD_SLASH', # "/"
        "ANGLE_OPEN",  # "<"
        "ANGLE_CLOSE",  # ">"
        "DOUBLE_ANGLE_OPEN",  # "<<"
        "DOUBLE_ANGLE_CLOSE",  # ">>"
        "E_BACKSLASH",  # "\\"
        "E_ANGLE_CLOSE",  # "\\>"
        #        'E_CHAR', # "\\C[haracter]"
        "E_CLOSE",  # "\\)"
        "E_EXCLAMATION",  # "\\!"
        #        'E_BRACKET_OPEN', # "\\["
        "E_OPEN",  # "\\("
        #        'E_BRACKET_CLOSE', # "\\]"
        "E_ANGLE_OPEN",  # "\\<"
        #        'E_PLUS', # "\\+"
        #        'E_TILDE', # "\\~"
        "EXTENDER",  # "__"
        #        'FIGURE_CLOSE', # "\\>"
        #        'FIGURE_OPEN', # "\\<"
        #        'FIGURE_SPACE', # "_"
        "HYPHEN",  # "--"
        #        'LYRIC_MARKUP',
        "MULTI_MEASURE_REST",
        "E_UNSIGNED",
        "UNSIGNED",
        "EXPECT_MARKUP",  # "markup?"
        "EXPECT_PITCH",  # "ly:pitch?"
        "EXPECT_DURATION",  # "ly:duration?"
        "EXPECT_SCM",  # "scheme?"
        "BACKUP",  # "(backed-up?)"
        "REPARSE",  # "(reparsed?)"
        "EXPECT_MARKUP_LIST",  # "markup-list?"
        "EXPECT_OPTIONAL",  # "optional?"
        "EXPECT_NO_MORE_ARGS",  #
        #        'EMBEDDED_LILY', # "#{"
        #        'BOOK_IDENTIFIER',
        #        'CHORD_MODIFIER',
        "CHORD_REPETITION",
        "CONTEXT_DEF_IDENTIFIER",
        "CONTEXT_MOD_IDENTIFIER",
        #        'DRUM_PITCH',
        "PITCH_IDENTIFIER",
        "DURATION_IDENTIFIER",
        "EVENT_IDENTIFIER",
        "EVENT_FUNCTION",
        "FRACTION",
        #        'LYRICS_STRING',
        #        'LYRIC_ELEMENT',
        #        'LYRIC_MARKUP_IDENTIFIER',
        "MARKUP_FUNCTION",
        "MARKUP_LIST_FUNCTION",
        "MARKUP_IDENTIFIER",
        "MARKUPLIST_IDENTIFIER",
        "MUSIC_FUNCTION",
        "MUSIC_IDENTIFIER",
        "NOTENAME_PITCH",
        "NUMBER_IDENTIFIER",
        "OUTPUT_DEF_IDENTIFIER",
        "REAL",
        "RESTNAME",
        "SCM_FUNCTION",
        "SCM_IDENTIFIER",
        "SCM_TOKEN",
        "SCORE_IDENTIFIER",
        "STRING",
        "STRING_IDENTIFIER",
        "TONICNAME_PITCH",
    ] + list(keywords.values())

    literals = (
        "!",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        ":",
        "<",
        "=",
        ">",
        "?",
        "[",
        "\\",
        "^",
        "_",
        "{",
        "|",
        "}",
        "~",
        "]",
    )

    string_accumulator = ""

    ### LEXICAL RULES ###

    # lexer.ll:165
    # <*>\r
    def t_ANY_165(self, t):
        r"\r"
        pass

    # lexer.ll:169
    # <extratoken>{ANY_CHAR}

    # lexer.ll:186
    # <extratoken><<EOF>>

    # lexer.ll:201
    # <INITIAL,chords,lyrics,figures,notes>{BOM_UTF8}/.*

    # lexer.ll:210
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>"%{"
    def t_INITIAL_markup_notes_210(self, t):
        r"%{"
        t.lexer.push_state("longcomment")
        pass

    # lexer.ll:214
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*[\n\r]
    def t_INITIAL_markup_notes_214(self, t):
        r"%[^{\n\r][^\n\r]*[\n\r]"
        pass

    def t_INITIAL_markup_notes_214_EOF(self, t):
        r"%[^{\n\r][^\n\r]*$"
        pass

    # lexer.ll:216
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r]
    def t_INITIAL_markup_notes_216(self, t):
        r"%[^{\n\r]"
        pass

    # lexer.ll:218
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[\n\r]
    def t_INITIAL_markup_notes_218(self, t):
        r"%[\n\r]"
        pass

    # lexer.ll:220
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*
    def t_INITIAL_markup_notes_220(self, t):
        r"%[^{\n\r][^\n\r]*"
        pass

    # lexer.ll:222
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>{WHITE}+
    def t_INITIAL_markup_notes_222(self, t):
        "[ \n\t\f\r]"
        pass

    # lexer.ll:227
    # <INITIAL,notes,figures,chords,markup>\"
    def t_INITIAL_markup_notes_227(self, t):
        r"\" "
        t.lexer.push_state("quote")
        self.string_accumulator = ""
        pass

    # lexer.ll:233
    # <INITIAL,chords,lyrics,notes,figures>\\version{WHITE}*
    def t_INITIAL_notes_233(self, t):
        r"\\version[ \n\t\f\r]*"
        t.lexer.push_state("version")
        pass

    # lexer.ll:236
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefilename{WHITE}*

    # lexer.ll:239
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefileline{WHITE}*

    # lexer.ll:242
    # <version>\"[^"]*\"
    def t_version_242(self, t):
        r'\"[^"]*\"'
        t.lexer.pop_state()
        pass

    # lexer.ll:256
    # <sourcefilename>\"[^"]*\"

    # lexer.ll:270
    # <sourcefileline>{INT}

    # lexer.ll:278
    # <version>{ANY_CHAR}
    @lex.TOKEN(ANY_CHAR)
    def t_version_278(self, t):
        print(("LilyPondParser: Illegal character '%s'" % t.value[0]))
        t.lexer.skip(1)

    # lexer.ll:282
    # <sourcefilename>{ANY_CHAR}

    # lexer.ll:286
    # <sourcefileline>{ANY_CHAR}

    # lexer.ll:296
    # <longcomment>"%"+"}"
    def t_longcomment_296(self, t):
        r"%}"
        t.lexer.pop_state()
        pass

    # lexer.ll:291
    # <longcomment>[^\%]*
    def t_longcomment_291(self, t):
        r"[^%]+"
        pass

    # lexer.ll:293
    # <longcomment>\%*[^}%]*
    def t_longcomment_293(self, t):
        r"%+[^}%]*"
        pass

    # lexer.ll:302
    # <INITIAL,chords,lyrics,notes,figures>\\maininput

    # lexer.ll:312
    # <INITIAL,chords,lyrics,figures,notes>\\include

    # lexer.ll:315
    # <incl>\"[^"]*\"

    # lexer.ll:322
    # <incl>\\{BLACK}*{WHITE}?

    # lexer.ll:341
    # <incl,version,sourcefilename>\"[^"]*
    def t_version_341(self, t):
        r'"[^"]*'
        raise Exception(f"end quote missing: {t!r}.")

    # lexer.ll:345
    # <chords,notes,figures>{RESTNAME}
    #    @lex.token.TOKEN(RESTNAME)
    #    def t_notes_345(self, t):
    #        t.type = 'RESTNAME'
    #        return t

    # lexer.ll:350
    # <chords,notes,figures>R
    #    def t_notes_350(self, t):
    #        'R'
    #        t.type = 'MULTI_MEASURE_REST'
    #        return t

    # def t_INITIAL_markup_notes_353_boolean(self, t):
    #    '\#\#(t|f)'
    #    t.type = 'SCM_TOKEN'
    #    if t.value[2] == 't':
    #        t.value = True
    #    else:
    #        t.value = False
    #    return t

    # @lex.TOKEN("\#'%s" % DASHED_WORD)
    # def t_INITIAL_markup_notes_353_identifier(self, t):
    #    t.type = 'SCM_IDENTIFIER'
    #    t.value = t.value[2:]
    #    return t

    # lexer.ll:353
    # <INITIAL,chords,figures,lyrics,markup,notes>#
    def t_INITIAL_markup_notes_353(self, t):
        r"\#"
        # t.type = 'SCHEME_START'
        # t.lexer.push_state('INITIAL')
        scheme_parser = SchemeParser(debug=False)
        input_string = t.lexer.lexdata[t.lexpos + 1 :]
        # print 'PREPARSE'
        try:
            scheme_parser(input_string)
        except _exceptions.SchemeParserFinishedError:
            result = scheme_parser.result
            t.value = result
            t.type = "SCM_TOKEN"
            # if isinstance(result, str):
            #    t.type = 'STRING'
            #    if t.value.find(' ') != -1:
            #        t.value = f'"{t.value}"'
            # else:
            #    t.type = 'SCM_TOKEN'
            t.lexer.skip(scheme_parser.cursor_end + 1)
        return t

    # lexer.ll:387
    # <INITIAL,notes,lyrics>\<\<
    def t_INITIAL_notes_387(self, t):
        r"\<\<"
        t.type = "DOUBLE_ANGLE_OPEN"
        return t

    # lexer.ll:390
    # <INITIAL,notes,lyrics>\>\>
    def t_INITIAL_notes_390(self, t):
        r"\>\>"
        t.type = "DOUBLE_ANGLE_CLOSE"
        return t

    # lexer.ll:396
    # <INITIAL,notes>\<
    def t_INITIAL_notes_396(self, t):
        r"\<"
        t.type = "ANGLE_OPEN"
        return t

    # lexer.ll:399
    # <INITIAL,notes>\>
    def t_INITIAL_notes_399(self, t):
        r"\>"
        t.type = "ANGLE_CLOSE"
        return t

    # lexer.ll:405
    # <figures>_

    # lexer.ll:408
    # <figures>\>

    # lexer.ll:411
    # <figures>\<

    # lexer.ll:417
    # <notes,figures>{ALPHAWORD}
    @lex.TOKEN(ALPHAWORD)
    def t_notes_417(self, t):
        pitch_names = self.client._pitch_names
        value = t.value
        if value in pitch_names:
            t.type = "NOTENAME_PITCH"
            t.value = _pitch.NamedPitchClass(pitch_names[t.value])
        elif value in _lyconst.drums:
            t.type = "NOTENAME_PITCH"
            t.value = _lyconst.drums[value]
        elif value in ["r", "s"]:
            t.type = "RESTNAME"
        elif value == "R":
            t.type = "MULTI_MEASURE_REST"
        elif value == "q":
            if self.client._last_chord is None:
                self.client._last_chord = _score.Chord(
                    ["c", "g", "c'"], (1, 4), tag=self.tag
                )
            t.type = "CHORD_REPETITION"
        else:
            t.type = "STRING"
        return t

    # lexer.ll:421
    # <notes,figures>{NOTECOMMAND}
    @lex.TOKEN(NOTECOMMAND)
    def t_notes_421(self, t):
        t.type = self.scan_escaped_word(t)
        return t

    # lexer.ll:424
    # <notes,figures>{FRACTION}
    @lex.TOKEN(FRACTION)
    def t_notes_424(self, t):
        t.type = "FRACTION"
        parts = t.value.split("/")
        t.value = LilyPondFraction(int(parts[0]), int(parts[1]))
        return t

    # lexer.ll:428
    # <notes,figures>{UNSIGNED}/\/|{UNSIGNED}
    # @lex.TOKEN('%s/\/|%s' % (UNSIGNED, UNSIGNED))
    @lex.TOKEN(r"%s/\/" % UNSIGNED)
    def t_notes_428(self, t):
        t.type = "UNSIGNED"
        t.value = int(t.value)
        return t

    @lex.TOKEN(UNSIGNED)
    def t_notes_428b(self, t):
        t.type = "UNSIGNED"
        t.value = int(t.value)
        return t

    # lexer.ll:433
    # <notes,figures>{E_UNSIGNED}
    @lex.TOKEN(E_UNSIGNED)
    def t_notes_433(self, t):
        t.type = "E_UNSIGNED"
        t.value = int(t.value[1:])
        return t

    # lexer.ll:440
    # <quote,lyric_quote>\\{ESCAPED}
    @lex.TOKEN("\\%s" % ESCAPED)
    def t_quote_440(self, t):
        self.string_accumulator += t.value
        pass

    def t_quote_XXX(self, t):
        r'\\"'
        self.string_accumulator += t.value
        pass

    # lexer.ll:443
    # <quote,lyric_quote>[^\\""]+
    def t_quote_443(self, t):
        r'[^\\""]+'
        self.string_accumulator += t.value
        pass

    # lexer.ll:446
    # <quote,lyric_quote>\"
    def t_quote_446(self, t):
        r"\" "
        t.lexer.pop_state()
        t.type = "STRING"
        t.value = self.string_accumulator
        return t

    # lexer.ll:456
    # <quote,lyric_quote>.
    def t_quote_456(self, t):
        r"."
        self.string_accumulator += t.value
        pass

    # lexer.ll:462
    # <lyrics>\"

    # lexer.ll:465
    # <lyrics>{FRACTION}

    # lexer.ll:469
    # <lyrics>{UNSIGNED}/\/[^0-9]

    # lexer.ll:473
    # <lyrics>{UNSIGNED}/\/|{UNSIGNED}

    # lexer.ll:478
    # <lyrics>{NOTECOMMAND}

    # lexer.ll:481
    # <lyrics>{LYRICS}

    # lexer.ll:499
    # <lyrics>.

    # lexer.ll:504
    # <chords>{ALPHAWORD}

    # lexer.ll:507
    # <chords>{NOTECOMMAND}

    # lexer.ll:510
    # <chords>{FRACTION}

    # lexer.ll:514
    # <chords>{UNSIGNED}/\/[^0-9]

    # lexer.ll:518
    # <chords>{UNSIGNED}/\/|{UNSIGNED}

    # lexer.ll:523
    # <chords>-

    # lexer.ll:526
    # <chords>:

    # lexer.ll:529
    # <chords>\/\+

    # lexer.ll:532
    # <chords>\/

    # lexer.ll:535
    # <chords>\^

    # lexer.ll:538
    # <chords>.

    # lexer.ll:545
    # <markup>\\score
    def t_markup_545(self, t):
        r"\\score"
        t.type = "SCORE"
        return t

    # lexer.ll:548
    # <markup>{MARKUPCOMMAND}
    @lex.TOKEN(MARKUPCOMMAND)
    def t_markup_548(self, t):
        value = t.value[1:]
        if (
            value in self.client._markup_functions
            or value in self.client._markup_list_functions
        ):
            if value in self.client._markup_functions:
                t.type = "MARKUP_FUNCTION"
                signature = self.client._markup_functions[value]
            else:
                t.type = "MARKUP_LIST_FUNCTION"
                signature = self.client._markup_list_functions[value]
            # print t.type, value, signature
            self.push_signature(signature, t)
        else:
            t.type = self.scan_escaped_word(t)
        return t

    # lexer.ll:598
    # <markup>[{}]
    #    def t_markup_598(self, t):
    #        r'[{}]'
    #        t.type = t.value
    #        return t

    # lexer.ll:601
    # <markup>[^#{}\"\\ \t\n\r\f]+
    def t_markup_601(self, t):
        r"[^#{}\"\\ \t\n\r\f]+"
        t.type = "STRING"
        return t

    # lexer.ll:614
    # <markup>.

    # lexer.ll:619
    # <longcomment><<EOF>>

    # lexer.ll:626
    # <<EOF>>

    # lexer.ll:643
    # <INITIAL>{DASHED_WORD}
    @lex.TOKEN(DASHED_WORD)
    def t_INITIAL_643(self, t):
        t.type = self.scan_bare_word(t)
        return t

    # lexer.ll:646
    # <INITIAL>{DASHED_KEY_WORD}
    @lex.TOKEN(DASHED_KEY_WORD)
    def t_INITIAL_646(self, t):
        t.type = self.scan_escaped_word(t)
        return t

    # lexer.ll:651
    # -{UNSIGNED}|{REAL}
    @lex.TOKEN(REAL)
    def t_651_a(self, t):
        t.type = "REAL"
        t.value = float(t.value)
        return t

    @lex.TOKEN("-%s" % UNSIGNED)
    def t_651_b(self, t):
        t.type = "REAL"
        t.value = float(t.value)
        return t

    # lexer.ll:661
    # -\.
    def t_661(self, t):
        r"-\."
        t.type = "REAL"
        t.value = 0.0
        return t

    # lexer.ll:666
    # {UNSIGNED}
    @lex.TOKEN(UNSIGNED)
    def t_666(self, t):
        t.type = "UNSIGNED"
        t.value = float(t.value)
        return t

    # lexer.ll:672
    # [{}]

    # lexer.ll:676
    # [*:=]

    # lexer.ll:682
    # <INITIAL,notes,figures>.

    # lexer.ll:686
    # <INITIAL,lyrics,notes,figures>\\.
    def t_INITIAL_notes_686(self, t):
        r"\\."
        if t.value[1] == ">":
            t.type = "E_ANGLE_CLOSE"
        elif t.value[1] == "<":
            t.type = "E_ANGLE_OPEN"
        elif t.value[1] == "!":
            t.type = "E_EXCLAMATION"
        elif t.value[1] == "(":
            t.type = "E_OPEN"
        elif t.value[1] == ")":
            t.type = "E_CLOSE"
        elif t.value[1] == "[":
            t.type = "E_BRACKET_OPEN"
        elif t.value[1] == "+":
            t.type = "E_PLUS"
        elif t.value[1] == "]":
            t.type = "E_BRACKET_CLOSE"
        elif t.value[1] == "~":
            t.type = "E_TILDE"
        elif t.value[1] == "\\":
            t.type = "E_BACKSLASH"
        else:
            t.type = "E_CHAR"
        return t

    # lexer.ll:
    # <*>.716
    #    def t_ANY_716(self, t):
    #        r'.'
    #        raise Exception

    ### DEFAULT RULES ###

    t_ignore = ""  # let the grammar handle ignoring things

    #    t_extratoken_ignore = t_ignore
    #    t_chords_ignore = t_ignore
    #    t_figures_ignore = t_ignore
    #    t_incl_ignore = t_ignore
    #    t_lyrics_ignore = t_ignore
    #    t_lyric_quote_ignore = t_ignore
    t_longcomment_ignore = t_ignore
    t_markup_ignore = t_ignore
    t_notes_ignore = t_ignore
    t_quote_ignore = t_ignore
    #    t_sourcefileline_ignore = t_ignore
    #    t_sourcefilename_ignore = t_ignore
    t_version_ignore = t_ignore

    t_scheme_ignore = t_ignore

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print(("LilyPondParser: Illegal character '%s'" % t.value[0]))
        t.lexer.skip(1)

    #    t_extratoken_error = t_error
    #    t_chords_error = t_error
    #    t_figures_error = t_error
    #    t_incl_error = t_error
    #    t_lyrics_error = t_error
    #    t_lyric_quote_error = t_error
    t_longcomment_error = t_error
    t_markup_error = t_error
    t_notes_error = t_error
    t_quote_error = t_error
    #    t_sourcefileline_error = t_error
    #    t_sourcefilename_error = t_error
    t_version_error = t_error
    t_scheme_error = t_error

    def scan_bare_word(self, t):
        if t.lexer.current_state() in ("notes",):
            pitch_names = self.client._pitch_names
            if t.value in pitch_names:
                t.type = "NOTENAME_PITCH"
            elif t.value == "q" and self.client._last_chord:
                t.type = "CHORD_REPETITION"
        return "STRING"

    def scan_escaped_word(self, t):
        # first, check for it in the keyword list
        if t.value in self.keywords:
            value = self.keywords[t.value]
            if value == "MARKUP":
                t.lexer.push_state("markup")
                if t.lexer.current_state() == "lyrics":
                    return "LYRIC_MARKUP"
            elif value == "WITH":
                t.lexer.push_state("INITIAL")
            return value
        identifier = t.value[1:]
        # check for the identifier in the scope stack
        lookup = self.client._resolve_identifier(identifier)
        if lookup is not None:
            identifier_lookup = {
                "book_block": "BOOK_IDENTIFIER",
                "bookpart_block": "BOOK_IDENTIFIER",
                "context_def_spec_block": "CONTEXT_DEF_IDENTIFIER",
                "context_modification": "CONTEXT_MOD_IDENTIFIER",
                "post_event_nofinger": "EVENT_IDENTIFIER",
                "full_markup": "MARKUP_IDENTIFIER",
                "full_markup_list": "MARKUPLINES_IDENTIFIER",
                "music": "MUSIC_IDENTIFIER",
                "number_expression": "NUMBER_IDENTIFIER",
                "output_def": "output_DEF_IDENTIFIER",
                "embedded_scm": "SCM_IDENTIFIER",
                "score_block": "SCORE_IDENTIFIER",
                "string": "STRING_IDENTIFIER",
                # 'PITCH_IDENTIFIER' ?
                # 'DURATION_IDENTIFIER' ?
                # 'LYRIC_MARKUP_IDENTIFIER' ?
            }
            t.value = copy.deepcopy(lookup.value)
            return identifier_lookup[lookup.type]
        # then, check for it in the current_module dictionary
        # which we've dumped out of LilyPond
        if identifier not in self.client._current_module:
            raise Exception(f"unknown escaped word: {t.value!r}.")
        lookup = self.client._current_module[identifier]
        # if the lookup resolves to a function definition,
        # we have to push artificial tokens onto the token stack.
        # the tokens are pushed in reverse order (LIFO).
        if isinstance(lookup, dict) and "type" in lookup:
            if lookup["type"] == "ly:music-function?":
                signature = lookup["signature"]
                funtype = "SCM_FUNCTION"
                if signature[0] == "ly:music?":
                    funtype = "MUSIC_FUNCTION"
                elif signature[0] == "ly:event?":
                    funtype = "EVENT_FUNCTION"
                self.push_signature(signature[1:], t)
                return funtype
            elif lookup["type"] == "ly:prob?":
                if "event" in lookup["types"]:
                    return "EVENT_IDENTIFIER"
                elif "context-specification" in lookup["types"] and hasattr(
                    self.client._guile, identifier
                ):
                    t.value = getattr(self.client._guile, identifier)()
                    return "MUSIC_IDENTIFIER"
        # we also check for other types, to handle \longa, \breve etc.
        elif isinstance(lookup, LilyPondDuration):
            t.value = copy.copy(lookup)
            return "DURATION_IDENTIFIER"
        # else...
        t.value = copy.copy(lookup)
        return "SCM_IDENTIFIER"

    def push_signature(self, signature, t):
        token = lex.LexToken()
        token.type = "EXPECT_NO_MORE_ARGS"
        token.value = None
        token.lineno = t.lineno
        token.lexpos = t.lexpos
        self.client._push_extra_token(token)

        optional = False
        for predicate in signature:
            if predicate == "optional?":
                optional = True
                continue

            token = lex.LexToken()
            token.value = predicate
            token.lineno = t.lineno
            token.lexpos = t.lexpos

            if predicate == "ly:music?":
                token.type = "EXPECT_SCM"  # ?!?!
            elif predicate == "ly:pitch?":
                token.type = "EXPECT_PITCH"
            elif predicate == "ly:duration?":
                token.type = "EXPECT_DURATION"
            elif predicate in ["markup?", "cheap-markup?"]:
                token.type = "EXPECT_MARKUP"
            elif predicate == "markup-list?":
                token.type = "EXPECT_MARKUP_LIST"
            else:
                token.type = "EXPECT_SCM"

            self.client._push_extra_token(token)

            if optional:
                optional_token = lex.LexToken()
                optional_token.value = "optional?"
                optional_token.lineno = t.lineno
                optional_token.lexpos = t.lexpos
                optional_token.type = "EXPECT_OPTIONAL"
                self.client._push_extra_token(optional_token)
                optional = False


# apply monkey patch
ply.yacc.LRParser._lilypond_patch_parse = _parse
ply.yacc.LRParser._lilypond_patch_parse_debug = _parse_debug


class LilyPondParser(Parser):
    r"""
    A LilyPond syntax parser.

    ..  container:: example

        >>> parser = abjad.parser.LilyPondParser()
        >>> string = r"\new Staff { c'4 ( d'8 e' fs'2) \fermata }"
        >>> staff = parser(string)
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            c'4
            (
            d'8
            e'8
            fs'2
            - \fermata
            )
        }

    ..  container:: example

        The LilyPond parser understands most spanners, articulations and
        dynamics:

        >>> string = r'''
        ... \new Staff {
        ...     c'8 \f \> (
        ...     d' -_ [
        ...     e' ^>
        ...     f' \ppp \<
        ...     g' \startTrillSpan \(
        ...     a' \)
        ...     b' ] \stopTrillSpan
        ...     c'' ) \accent \sfz
        ... }
        ... '''
        >>> staff = parser(string)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                \f
                (
                \>
                d'8
                - \portato
                [
                e'8
                ^ \accent
                f'8
                \ppp
                \<
                g'8
                \(
                \startTrillSpan
                a'8
                \)
                b'8
                \stopTrillSpan
                ]
                c''8
                - \accent
                \sfz
                )
            }

    ..  container:: example

        The LilyPond parser understands contexts and markup:

        >>> string = r'''\new Score <<
        ...     \new Staff = "Treble Staff" {
        ...         \new Voice = "Treble Voice" {
        ...             c' ^\markup { \bold Treble! }
        ...         }
        ...     }
        ...     \new Staff = "Bass Staff" {
        ...         \new Voice = "Bass Voice" {
        ...             \clef bass
        ...             c, _\markup { \italic Bass! }
        ...         }
        ...     }
        ... >>
        ... '''
        >>> score = parser(string)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \context Staff = "Treble Staff"
                {
                    \context Voice = "Treble Voice"
                    {
                        c'4
                        ^ \markup {
                            \bold
                                Treble!
                            }
                    }
                }
                \context Staff = "Bass Staff"
                {
                    \context Voice = "Bass Voice"
                    {
                        \clef "bass"
                        c,4
                        _ \markup {
                            \italic
                                Bass!
                            }
                    }
                }
            >>

    ..  container:: example

        The LilyPond parser also understands certain aspects of LilyPond file
        layouts, such as header blocks:

        >>> string = r'''
        ... \header {
        ...     composer = \markup { by \bold "Foo von Bar" }
        ...     title = \markup { The ballad of Foo von Bar }
        ...     tagline = \markup { "" }
        ... }
        ... \score {
        ...     \new Staff {
        ...         \time 3/4
        ...         g' ( b' d'' )
        ...         e''4. ( c''8 c'4 )
        ...     }
        ... }
        ... '''
        >>> blocks = parser(string)
        >>> abjad.show(blocks) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(blocks) # doctest: +SKIP
            >>> print(string) # doctest: +SKIP
            % 2017-07-11 15:13
            <BLANKLINE>
            \version "2.19.63"
            \language "english"
            <BLANKLINE>
            \header {
                composername = \markup {
                    Foo
                    van
                    Bar
                    }
                composer = \markup {
                    by
                    \bold
                        "Foo von Bar"
                    }
                title = \markup {
                    The
                    ballad
                    of
                    "Foo von Bar"
                    }
                tagline = \markup {}
            }
            <BLANKLINE>
            \score {
                \new Staff {
                    \time 3/4
                    g'4 (
                    b'4
                    d''4 )
                    e''4. (
                    c''8
                    c'4 )
                }
            }

    ..  container:: example

        The LilyPond parser supports a small number of LilyPond music
        functions, such as \relative and \transpose.

        ..  note::

            Music functions which mutate the score during compilation result in a
            normalized Abjad score structure. The resulting structure corresponds
            to the music as it appears on the page, rather than as it was input to
            the parser:

        >>> string = r'''
        ... \new Staff \relative c {
        ...     c32 d e f g a b c d e f g a b c d e f g a b c
        ... }
        ... '''
        >>> staff = parser(string)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c32
                d32
                e32
                f32
                g32
                a32
                b32
                c'32
                d'32
                e'32
                f'32
                g'32
                a'32
                b'32
                c''32
                d''32
                e''32
                f''32
                g''32
                a''32
                b''32
                c'''32
            }

    ..  container:: example

        The LilyPond parser defaults to English note names, but any of the
        other languages supported by LilyPond may be used:

        >>> parser = abjad.parser.LilyPondParser('nederlands')
        >>> string = '{ c des e fis }'
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c4
                df4
                e4
                fs4
            }

    Briefly, LilyPondParser understands theses aspects of LilyPond syntax:

    - Notes, chords, rests, skips and multi-measure rests
    - Durations, dots, and multipliers
    - All pitchnames, and octave ticks
    - Simple markup (i.e. ``c'4 ^ "hello!"``)
    - Most articulations
    - Most spanners, incl. beams, slurs, phrasing slurs, ties, and glissandi
    - Most context types via ``\new`` and ``\context``,
      as well as context ids (i.e. ``\new Staff = "foo" { }``)
    - Variable assigns (ie ``global = { \time 3/4 } \new Staff { \global }``)
    - Many music functions:
        - ``\acciaccatura``
        - ``\appoggiatura``
        - ``\bar``
        - ``\breathe``
        - ``\clef``
        - ``\grace``
        - ``\key``
        - ``\transpose``
        - ``\language``
        - ``\makeClusters``
        - ``\mark``
        - ``\oneVoice``
        - ``\relative``
        - ``\skip``
        - ``\slashedGrace``
        - ``\time``
        - ``\times``
        - ``\transpose``
        - ``\tuplet``
        - ``\voiceOne``, ``\voiceTwo``, ``\voiceThree``, ``\voiceFour``

    LilyPondParser currently **DOES NOT** understand many other aspects
    of LilyPond syntax:

    - ``\markup``
    - ``\book``, ``\bookpart``, ``\header``, ``\layout``, ``\midi``, ``\paper``
    - ``\repeat`` and ``\alternative``
    - Lyrics
    - ``\chordmode``, ``\drummode`` or ``\figuremode``
    - Property operations, such as ``\override``,
      ``\revert``, ``\set``, ``\unset``, and ``\once``
    - Music functions which generate or extensively mutate musical structures
    - Embedded Scheme statements (anything beginning with ``#``)
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_chord_pitch_orders",
        "_current_module",
        "_default_duration",
        "_default_language",
        "_guile",
        "_language_pitch_names",
        "_last_chord",
        "_lexdef",
        "_markup_functions",
        "_markup_list_functions",
        "_pitch_names",
        "_repeated_chords",
        "_scope_stack",
        "_syndef",
        "tag",
    )

    ### INITIALIZER ###

    def __init__(self, default_language="english", *, debug=False, tag=None):
        # LilyPond emulation data
        self._guile = GuileProxy(self, tag=tag)
        self._current_module = _lyenv.current_module
        self._language_pitch_names = _lyenv.language_pitch_names
        self._markup_functions = _lyenv.markup_functions
        self._markup_list_functions = _lyenv.markup_list_functions
        self.default_language = default_language
        self.tag = tag

        # attach parser and lexer rules
        self._lexdef = LilyPondLexicalDefinition(self, tag=tag)
        self._syndef = LilyPondSyntacticalDefinition(self, tag=tag)

        # build PLY parser and lexer
        Parser.__init__(self, debug=debug)

        self._reset_parser_variables()

    ### SPECIAL METHODS ###

    def __call__(self, input_string):
        """
        Calls LilyPond parser on ``input_string``.

        Returns Abjad components.
        """
        self._reset_parser_variables()
        if self._debug:
            result = self._parser._lilypond_patch_parse_debug(
                input_string, lexer=self._lexer, debug=self._logger
            )
        else:
            result = self._parser._lilypond_patch_parse(input_string, lexer=self._lexer)
        return result

    ### PRIVATE METHODS ###

    def _assign_variable(self, identifier, value):
        self._scope_stack[-1][identifier] = value

    def _backup_token(self, token_type, token_value):
        if self._debug:
            self._logger.info("Extra  : Backing up")

        # push the current lookahead back onto the lookaheadstack
        self._push_extra_token(self._parser.lookahead)

        # create the backup token, set as new lookahead
        backup = ply.lex.LexToken()
        backup.type = "BACKUP"
        backup.value = "(backed-up?)"
        backup.lexpos = 0
        backup.lineno = 0
        self._parser.lookahead = backup

        if token_type:
            token = ply.lex.LexToken()
            token.type = token_type
            token.value = token_value
            token.lexpos = 0
            token.lineno = 0
            self._push_extra_token(token)

    def _construct_context_specced_music(
        self, context, optional_id, optional_context_mod, music
    ):
        known_contexts = {
            "ChoirStaff": _score.StaffGroup,
            "GrandStaff": _score.StaffGroup,
            "PianoStaff": _score.StaffGroup,
            "Score": _score.Score,
            "Staff": _score.Staff,
            "StaffGroup": _score.StaffGroup,
            "Voice": _score.Voice,
        }
        lilypond_type = context
        if context in known_contexts:
            context = known_contexts[context]([])
        else:
            raise Exception(f"context type {context!r} not supported.")
        if lilypond_type in ("GrandStaff", "PianoStaff"):
            context.lilypond_type = lilypond_type
        if optional_id is not None:
            context.name = optional_id
        if optional_context_mod is not None:
            for x in optional_context_mod:
                print(x)
            # TODO: impelement context mods on contexts
            pass
        context.simultaneous = music.simultaneous
        # add children
        while len(music):
            component = music.pop(0)
            context.append(component)
        for wrapper in music._wrappers:
            _bind._unsafe_attach(wrapper, context)
        return context

    def _construct_sequential_music(self, music):
        # indicator sorting could be rewritten into a single list using tuples
        # with t[0] being 'forward' or 'backward' and t[1] being the indicator
        # as this better preserves attachment order. Not clear if we need it.
        container = _score.Container(tag=self.tag)
        previous_leaf = None
        apply_forward = []
        apply_backward = []
        # sort events into forward or backwards attaching
        # and attach them to the proper leaf
        for x in music:
            if isinstance(x, _score.Component) and not isinstance(
                x, _score.BeforeGraceContainer
            ):
                for indicator in apply_forward:
                    try:
                        _bind._unsafe_attach(indicator, x)
                    except _exceptions.MissingContextError:
                        score = _score.Score([x], simultaneous=False)
                        _bind._unsafe_attach(indicator, x)
                        score[:] = []
                if previous_leaf:
                    for indicator in apply_backward:
                        _bind._unsafe_attach(indicator, previous_leaf)
                else:
                    for indicator in apply_backward:
                        _bind._unsafe_attach(indicator, x)
                apply_forward[:] = []
                apply_backward[:] = []
                previous_leaf = x
                container.append(x)
            else:
                if isinstance(x, _indicators.BarLine):
                    apply_backward.append(x)
                elif isinstance(x, _indicators.LilyPondLiteral) and x.argument in (
                    r"\break",
                    r"\breathe",
                    r"\pageBreak",
                ):
                    apply_backward.append(x)
                else:
                    apply_forward.append(x)
        # attach remaining events to last leaf
        # or to the container itself if there were no leaves
        if previous_leaf:
            for indicator in apply_forward:
                _bind._unsafe_attach(indicator, previous_leaf)
            for indicator in apply_backward:
                _bind._unsafe_attach(indicator, previous_leaf)
        else:
            for indicator in apply_forward:
                _bind._unsafe_attach(indicator, container)
            for indicator in apply_backward:
                _bind._unsafe_attach(indicator, container)
        return container

    def _construct_simultaneous_music(self, music):
        def is_separator(x):
            if isinstance(x, LilyPondEvent):
                if x.name == "VoiceSeparator":
                    return True
            return False

        container = _score.Container(tag=self.tag)
        container.simultaneous = True
        # check for voice separators
        groups = []
        for value, group in itertools.groupby(music, is_separator):
            if not value:
                groups.append(list(group))
        # without voice separators
        if 1 == len(groups):
            # assert all(isinstance(x, _score.Context) for x in groups[0])
            container.extend(groups[0])
        # with voice separators
        else:
            for group in groups:
                container.append(
                    _score.Voice(
                        self._construct_sequential_music(group)[:], tag=self.tag
                    )
                )
        return container

    @classmethod
    def _get_scheme_predicates(class_):
        return {
            "boolean?": lambda x: isinstance(x, bool),
            "cheap-list?": lambda x: isinstance(x, list | tuple),
            "cheap-markup?": lambda x: isinstance(x, MarkupCommand),
            "fraction?": lambda x: isinstance(x, LilyPondFraction),
            "integer?": lambda x: isinstance(x, int),
            "list?": lambda x: isinstance(x, list | tuple),
            "ly:duration?": lambda x: isinstance(x, LilyPondDuration),
            "ly:music?": lambda x: isinstance(x, _score.Component),
            "ly:pitch?": lambda x: isinstance(x, _pitch.NamedPitch),
            "markup?": lambda x: isinstance(x, MarkupCommand),
            "number-list?": lambda x: isinstance(x, list | tuple)
            and all(isinstance(y, int | float) for y in x),
            "number?": lambda x: isinstance(x, int | float),
            "real?": lambda x: isinstance(x, int | float),
            "string?": lambda x: isinstance(x, str),
            "void?": lambda x: isinstance(x, type(None)),
            # the following predicates have not yet been implemented in Abjad
            "hash-table?": lambda x: True,
            "list-or-symbol?": lambda x: True,
            "ly:dir?": lambda x: True,
            "ly:moment?": lambda x: True,
            "number-or-string?": lambda x: True,
            "number-pair?": lambda x: True,
            "optional?": lambda x: True,
            "pair?": lambda x: True,
            "procedure?": lambda x: True,
            "scheme?": lambda x: True,
            "string-or-pair?": lambda x: True,
            "symbol-or-boolean?": lambda x: True,
            "symbol?": lambda x: True,
        }

    def _pop_variable_scope(self):
        if self._scope_stack:
            self._scope_stack.pop()

    def _process_post_events(self, leaf, post_events):
        prototype = (
            _indicators.Articulation,
            _indicators.BarLine,
            _indicators.Dynamic,
            _indicators.Glissando,
            _indicators.LilyPondLiteral,
            _indicators.Markup,
            _indicators.RepeatTie,
            _indicators.StartBeam,
            _indicators.StartGroup,
            _indicators.StartHairpin,
            _indicators.StartPhrasingSlur,
            _indicators.StartSlur,
            _indicators.StartTextSpan,
            _indicators.StartTrillSpan,
            _indicators.StemTremolo,
            _indicators.StopBeam,
            _indicators.StopGroup,
            _indicators.StopHairpin,
            _indicators.StopPhrasingSlur,
            _indicators.StopSlur,
            _indicators.StopTextSpan,
            _indicators.StopTrillSpan,
            _indicators.Tie,
        )
        for post_event in post_events:
            if isinstance(post_event, prototype):
                _bind._unsafe_attach(post_event, leaf)
            if isinstance(post_event, tuple) and isinstance(post_event[0], prototype):
                indicator, direction = post_event
                _bind._unsafe_attach(indicator, leaf, direction=direction)

    def _push_extra_token(self, token):
        self._parser.lookaheadstack.append(token)

    def _push_variable_scope(self):
        self._scope_stack.append({})

    def _relex_lookahead(self):
        if not str(self._parser.lookahead) == "$end":
            difference = self._parser.lookahead.lexpos - self._lexer.lexpos
            self._lexer.skip(difference)
            self._parser.lookahead = None

    def _reparse_token(self, predicate, token_type, token_value):
        if self._debug:
            self._logger.info("Extra  : Reparsing")

        # push the current lookahead back onto the lookaheadstack
        self._push_extra_token(self._parser.lookahead)

        token = ply.lex.LexToken()
        token.type = token_type
        token.value = token_value
        token.lexpos = 0
        token.lineno = 0
        self._push_extra_token(token)

        reparse = ply.lex.LexToken()
        reparse.type = "REPARSE"
        reparse.value = predicate
        reparse.lineno = 0
        reparse.lexpos = 0
        self._parser.lookahead = reparse

    def _reset_parser_variables(self):
        try:
            self._parser.restart()
        except Exception:
            pass
        self._scope_stack = [{}]
        self._chord_pitch_orders = {}
        self._lexer.push_state("notes")
        self._default_duration = LilyPondDuration((1, 4), None)
        self._last_chord = None
        # LilyPond's default!
        # self._last_chord = _score.Chord(['c', 'g', "c'"], (1, 4))
        self._pitch_names = self._language_pitch_names[self.default_language]
        self._repeated_chords = {}

    def _resolve_event_identifier(self, identifier):
        # without leading slash
        lookup = self._current_module[identifier]
        name = lookup["name"]
        if name == "ArticulationEvent":
            return _indicators.Articulation(lookup["articulation-type"])
        elif name == "AbsoluteDynamicEvent":
            return _indicators.Dynamic(lookup["text"])
        elif name == "BeamEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartBeam()
            else:
                return _indicators.StopBeam()
        elif name == "CrescendoEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartHairpin("<")
            else:
                return _indicators.StopHairpin()
        elif name == "DecrescendoEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartHairpin(">")
            else:
                return _indicators.StopHairpin()
        elif name == "GlissandoEvent":
            return _indicators.Glissando()
        elif name == "LaissezVibrerEvent":
            return _indicators.LilyPondLiteral(r"\laissezVibrer", site="after")
        elif name == "LineBreakEvent":
            return _indicators.LilyPondLiteral(r"\break")
        elif name == "NoteGroupingEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartGroup()
            else:
                return _indicators.StopGroup()
        elif name == "PhrasingSlurEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartPhrasingSlur()
            else:
                return _indicators.StopPhrasingSlur()
        elif name == "RepeatTieEvent":
            return _indicators.RepeatTie()
        elif name == "SlurEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartSlur()
            else:
                return _indicators.StopSlur()
        elif name == "TextSpanEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartTextSpan()
            else:
                return _indicators.StopTextSpan()
        elif name == "TieEvent":
            return _indicators.Tie()
        elif name == "TrillSpanEvent":
            if lookup["span-direction"] == -1:
                return _indicators.StartTrillSpan()
            else:
                return _indicators.StopTrillSpan()
        event = LilyPondEvent(name)
        if "span-direction" in lookup:
            if lookup["span-direction"] == -1:
                event.span_direction = "start"
            else:
                event.span_direction = "stop"
        return event

    def _resolve_identifier(self, identifier):
        for scope in reversed(self._scope_stack):
            if identifier in scope:
                return scope[identifier]
        return None

    def _test_scheme_predicate(self, predicate, value):
        predicates = self._get_scheme_predicates()
        if predicate in predicates:
            return predicates[predicate](value)
        return True

    @staticmethod
    def _transpose_enharmonically(pitch_a, pitch_b, pitch_c):
        """
        Transpose ``pitch_c`` by the distance between ``pitch_b``
        and ``pitch_a1``.

        This function was reverse-engineered from LilyPond's source code.

        Returns named pitch.
        """

        def normalize_alteration(step, alteration):
            while 2.0 < alteration:
                alteration -= step_size(step)
                step += 1.0
            while alteration < -2.0:
                step -= 1.0
                alteration += step_size(step)
            return step, alteration

        def normalize_octave(octave, step):
            normalized_step = step % len(scale)
            octave += (step - normalized_step) / len(scale)
            return octave, normalized_step

        def step_size(step):
            normalized_step = step % len(scale)
            if normalized_step == 6:
                return 1.0  # b to c
            return scale[normalized_step + 1] - scale[normalized_step]

        if not isinstance(pitch_a, _pitch.NamedPitch):
            pitch_a = _pitch.NamedPitch(pitch_a)
        if not isinstance(pitch_b, _pitch.NamedPitch):
            pitch_b = _pitch.NamedPitch(pitch_b)
        if not isinstance(pitch_c, _pitch.NamedPitch):
            pitch_c = _pitch.NamedPitch(pitch_c)
        scale = [0.0, 2.0, 4.0, 5.0, 7.0, 9.0, 11.0]
        a_oct, a_step = (
            pitch_a.octave.number,
            pitch_a._get_diatonic_pc_number(),
        )
        b_oct, b_step = (
            pitch_b.octave.number,
            pitch_b._get_diatonic_pc_number(),
        )
        c_oct, c_step, c_alt = (
            pitch_c.octave.number,
            pitch_c._get_diatonic_pc_number(),
            pitch_c.accidental.semitones,
        )
        d_oct, d_step, d_tones = (
            b_oct - a_oct,
            b_step - a_step,
            float(pitch_b.number) - float(pitch_a.number),
        )
        tmp_alt = float(pitch_c.number) + d_tones
        # print 'TMP_ALT: %f' % tmp_alt
        new_oct = c_oct + d_oct
        new_step = c_step + d_step
        new_alt = c_alt
        # print 'NEW:', new_oct, new_step, new_alt
        new_step, new_alt = normalize_alteration(new_step, new_alt)
        new_oct, new_step = normalize_octave(new_oct, new_step)
        # print 'NEW(norm):', new_oct, new_step, new_alt
        octave_ticks = _pitch.Octave(new_oct).ticks
        pitch_class_name = _pitch._diatonic_pc_number_to_diatonic_pc_name[new_step % 7]
        accidental = str(_pitch.Accidental(new_alt))
        tmp_pitch = _pitch.NamedPitch(pitch_class_name + accidental + octave_ticks)
        # print 'TMP(pitch): %r' % tmp_pitch
        new_alt += tmp_alt - float(tmp_pitch.number)
        # print 'NEW(alt): %f' % new_alt
        new_step, new_alt = normalize_alteration(new_step, new_alt)
        new_oct, new_step = normalize_octave(new_oct, new_step)
        # print 'NEW(norm):', new_oct, new_step, new_alt
        octave_ticks = _pitch.Octave(new_oct).ticks
        pitch_class_name = _pitch._diatonic_pc_number_to_diatonic_pc_name[new_step % 7]
        accidental = str(_pitch.Accidental(new_alt))
        return _pitch.NamedPitch(pitch_class_name + accidental + octave_ticks)

    ### PUBLIC METHODS ###

    @staticmethod
    def list_known_contexts() -> list[str]:
        """
        Lists all LilyPond contexts recognized by LilyPond parser.

        ..  container:: example

            >>> class_ = abjad.parser.LilyPondParser
            >>> for context in class_.list_known_contexts():
            ...     print(context)
            ...
            ChoirStaff
            ChordNames
            CueVoice
            Devnull
            DrumStaff
            DrumVoice
            Dynamics
            FiguredBass
            FretBoards
            Global
            GrandStaff
            GregorianTranscriptionStaff
            GregorianTranscriptionVoice
            KievanStaff
            KievanVoice
            Lyrics
            MensuralStaff
            MensuralVoice
            NoteNames
            NullVoice
            OneStaff
            PetrucciStaff
            PetrucciVoice
            PianoStaff
            RhythmicStaff
            Score
            Staff
            StaffGroup
            TabStaff
            TabVoice
            VaticanaStaff
            VaticanaVoice
            Voice

        """

        return sorted(_lyenv.contexts.keys())

    @staticmethod
    def list_known_dynamics() -> tuple[str, ...]:
        """
        Lists all dynamics recognized by LilyPond parser.

        ..  container:: example

            >>> class_ = abjad.parser.LilyPondParser
            >>> for dynamic in class_.list_known_dynamics():
            ...     print(dynamic)
            ...
            f
            ff
            fff
            ffff
            fffff
            fp
            fz
            mf
            mp
            p
            pp
            ppp
            pppp
            ppppp
            rfz
            sf
            sff
            sfp
            sfz
            sp
            spp

        """
        result = []
        for key, value in _lyenv.current_module.items():
            if not isinstance(value, dict):
                continue
            if "dynamic-event" in value.get("types", ()):
                result.append(key)
        result.sort()
        return tuple(result)

    @staticmethod
    def list_known_grobs() -> list[str]:
        """
        Lists all LilyPond grobs recognized by LilyPond parser.

        ..  container:: example

            >>> class_ = abjad.parser.LilyPondParser
            >>> for grob in class_.list_known_grobs():
            ...     print(grob)
            ...
            Accidental
            AccidentalCautionary
            AccidentalPlacement
            AccidentalSuggestion
            Ambitus
            AmbitusAccidental
            AmbitusLine
            AmbitusNoteHead
            Arpeggio
            BalloonTextItem
            BarLine
            BarNumber
            BassFigure
            BassFigureAlignment
            BassFigureAlignmentPositioning
            BassFigureBracket
            BassFigureContinuation
            BassFigureLine
            Beam
            BendAfter
            BreakAlignGroup
            BreakAlignment
            BreathingSign
            ChordName
            Clef
            ClefModifier
            ClusterSpanner
            ClusterSpannerBeacon
            CombineTextScript
            CueClef
            CueEndClef
            Custos
            DotColumn
            Dots
            DoublePercentRepeat
            DoublePercentRepeatCounter
            DoubleRepeatSlash
            DynamicLineSpanner
            DynamicText
            DynamicTextSpanner
            Episema
            Fingering
            FingeringColumn
            Flag
            FootnoteItem
            FootnoteSpanner
            FretBoard
            Glissando
            GraceSpacing
            GridLine
            GridPoint
            Hairpin
            HorizontalBracket
            HorizontalBracketText
            InstrumentName
            InstrumentSwitch
            KeyCancellation
            KeySignature
            KievanLigature
            LaissezVibrerTie
            LaissezVibrerTieColumn
            LedgerLineSpanner
            LeftEdge
            LigatureBracket
            LyricExtender
            LyricHyphen
            LyricSpace
            LyricText
            MeasureCounter
            MeasureGrouping
            MelodyItem
            MensuralLigature
            MetronomeMark
            MultiMeasureRest
            MultiMeasureRestNumber
            MultiMeasureRestText
            NonMusicalPaperColumn
            NoteCollision
            NoteColumn
            NoteHead
            NoteName
            NoteSpacing
            OttavaBracket
            PaperColumn
            ParenthesesItem
            PercentRepeat
            PercentRepeatCounter
            PhrasingSlur
            PianoPedalBracket
            RehearsalMark
            RepeatSlash
            RepeatTie
            RepeatTieColumn
            Rest
            RestCollision
            Script
            ScriptColumn
            ScriptRow
            Slur
            SostenutoPedal
            SostenutoPedalLineSpanner
            SpacingSpanner
            SpanBar
            SpanBarStub
            StaffGrouper
            StaffSpacing
            StaffSymbol
            StanzaNumber
            Stem
            StemStub
            StemTremolo
            StringNumber
            StrokeFinger
            SustainPedal
            SustainPedalLineSpanner
            System
            SystemStartBar
            SystemStartBrace
            SystemStartBracket
            SystemStartSquare
            TabNoteHead
            TextScript
            TextSpanner
            Tie
            TieColumn
            TimeSignature
            TrillPitchAccidental
            TrillPitchGroup
            TrillPitchHead
            TrillSpanner
            TupletBracket
            TupletNumber
            UnaCordaPedal
            UnaCordaPedalLineSpanner
            VaticanaLigature
            Vertical
            VerticalAxisGroup
            VoiceFollower
            VoltaBracket
            VoltaBracketSpanner

        """

        return sorted(_lyenv.grob_interfaces.keys())

    @staticmethod
    def list_known_languages() -> list[str]:
        """
        Lists all note-input languages recognized by LilyPond parser.

        ..  container:: example

            >>> class_ = abjad.parser.LilyPondParser
            >>> for language in class_.list_known_languages():
            ...     print(language)
            ...
            catalan
            deutsch
            english
            espanol
            español
            français
            italiano
            nederlands
            norsk
            portugues
            suomi
            svenska
            vlaams

        """
        return sorted(_lyenv.language_pitch_names.keys())

    @staticmethod
    def list_known_markup_functions() -> list[str]:
        """
        Lists all markup functions recognized by LilyPond parser.

        ..  container:: example

            >>> class_  = abjad.parser.LilyPondParser
            >>> for name in class_.list_known_markup_functions():
            ...     print(name)
            ...
            abs-fontsize
            arrow-head
            auto-footnote
            backslashed-digit
            beam
            bold
            box
            bracket
            caps
            center-align
            center-column
            char
            circle
            column
            column-lines
            combine
            compound-meter
            concat
            customTabClef
            dir-column
            doubleflat
            doublesharp
            draw-circle
            draw-dashed-line
            draw-dotted-line
            draw-hline
            draw-line
            dynamic
            ellipse
            epsfile
            eyeglasses
            fermata
            fill-line
            fill-with-pattern
            filled-box
            finger
            first-visible
            flat
            fontCaps
            fontsize
            footnote
            fraction
            fret-diagram
            fret-diagram-terse
            fret-diagram-verbose
            fromproperty
            general-align
            halign
            harp-pedal
            hbracket
            hcenter-in
            hspace
            huge
            italic
            justified-lines
            justify
            justify-field
            justify-line
            justify-string
            large
            larger
            left-align
            left-brace
            left-column
            line
            lookup
            lower
            magnify
            map-markup-commands
            markalphabet
            markletter
            medium
            musicglyph
            natural
            normal-size-sub
            normal-size-super
            normal-text
            normalsize
            note
            note-by-number
            null
            number
            on-the-fly
            oval
            override
            override-lines
            pad
            pad-around
            pad-to-box
            pad-x
            page-link
            page-ref
            parenthesize
            path
            pattern
            postscript
            property-recursive
            put-adjacent
            raise
            replace
            rest
            rest-by-number
            right-align
            right-brace
            right-column
            roman
            rotate
            rounded-box
            sans
            scale
            score
            score-lines
            semiflat
            semisharp
            sesquiflat
            sesquisharp
            sharp
            simple
            slashed-digit
            small
            smallCaps
            smaller
            stencil
            strut
            sub
            super
            table-of-contents
            teeny
            text
            tied-lyric
            tiny
            translate
            translate-scaled
            transparent
            triangle
            typewriter
            underline
            upright
            vcenter
            verbatim-file
            vspace
            whiteout
            whiteout-box
            with-color
            with-dimensions
            with-link
            with-url
            woodwind-diagram
            wordwrap
            wordwrap-field
            wordwrap-internal
            wordwrap-lines
            wordwrap-string
            wordwrap-string-internal

        """
        return sorted(
            list(_lyenv.markup_functions.keys())
            + list(_lyenv.markup_list_functions.keys())
        )

    @staticmethod
    def list_known_music_functions() -> list[str]:
        """
        Lists all music functions recognized by LilyPond parser.

        ..  container:: example

            >>> class_ = abjad.parser.LilyPondParser
            >>> for name in class_.list_known_music_functions():
            ...     print(name)
            ...
            acciaccatura
            appoggiatura
            bar
            breathe
            clef
            grace
            key
            language
            makeClusters
            mark
            relative
            skip
            time
            times
            transpose
            tuplet

        """
        music_functions = []
        for name in _lyenv.current_module:
            dictionary = _lyenv.current_module[name]
            if not isinstance(dictionary, dict):
                continue
            assert isinstance(dictionary, dict)
            if "type" not in dictionary:
                continue
            if not dictionary["type"] == "ly:music-function?":
                continue
            if not hasattr(GuileProxy, name):
                continue
            music_functions.append(name)
        return sorted(music_functions)

    ### PUBLIC PROPERTIES ###

    @property
    def available_languages(self) -> tuple[str, ...]:
        r"""
        Tuple of pitch-name languages supported by LilyPondParser.

        ..  container:: example

            >>> parser = abjad.parser.LilyPondParser()
            >>> for language in parser.available_languages:
            ...     print(language)
            ...
            catalan
            deutsch
            english
            espanol
            español
            français
            italiano
            nederlands
            norsk
            portugues
            suomi
            svenska
            vlaams

        """
        return tuple(sorted(self._language_pitch_names.keys()))

    @property
    def default_language(self) -> str:
        """
        Gets and sets default language of parser.

        ..  container:: example

            >>> parser = abjad.parser.LilyPondParser()

            >>> parser.default_language
            'english'

            >>> parser('{ c df e fs }')
            Container('c4 df4 e4 fs4')

            >>> parser.default_language = 'nederlands'
            >>> parser.default_language
            'nederlands'

            >>> parser('{ c des e fis }')
            Container('c4 df4 e4 fs4')

        """
        return self._default_language

    @default_language.setter
    def default_language(self, argument):
        assert argument in self.available_languages
        self._default_language = argument

    @property
    def lexer_rules_object(self):
        """
        Lexer rules object of LilyPond parser.
        """
        return self._lexdef

    @property
    def parser_rules_object(self):
        """
        Parser rules object of LilyPond parser.
        """
        return self._syndef


class LilyPondSyntacticalDefinition:
    """
    The syntactical definition of LilyPond's syntax.

    Effectively equivalent to LilyPond's ``parser.yy`` file.

    Not composer-safe.

    Used internally by ``LilyPondParser``.
    """

    start = "start_symbol"

    precedence = (
        # ('nonassoc', 'ALTERNATIVE'),
        ("nonassoc", "COMPOSITE"),
        # ('left', 'ADDLYRICS'),
        ("nonassoc", "DEFAULT"),
        ("nonassoc", "FUNCTION_ARGLIST"),
        (
            "right",
            "PITCH_IDENTIFIER",
            "NOTENAME_PITCH",
            "TONICNAME_PITCH",
            "UNSIGNED",
            "REAL",
            "DURATION_IDENTIFIER",
            ":",
        ),
        ("nonassoc", "NUMBER_IDENTIFIER", "/"),
        ("left", "+", "-"),
        # ('left', 'UNARY_MINUS')
    )

    ### INITIALIZER ###

    def __init__(self, client=None, *, tag=None):
        self.client = client
        if client is not None:
            self.tokens = self.client._lexdef.tokens
        else:
            self.tokens = []
        self.tag = tag

    ### SYNTACTICAL RULES (ALPHABETICAL) ###

    #    def p_start_symbol__EMBEDDED_LILY__embedded_lilypond(self, p):
    #        'start_symbol : EMBEDDED_LILY embedded_lilypond'
    #        p[0] = SyntaxNode('start_symbol', p[1:])

    def p_start_symbol__lilypond(self, p):
        "start_symbol : lilypond"
        if 1 < len(p[1]):
            lilypond_file = _lilypondfile.LilyPondFile()
            lilypond_file.items.extend(p[1])
            p[0] = lilypond_file
        elif 1 == len(p[1]):
            p[0] = p[1][0]
        else:
            p[0] = None

    ### assignment ###

    def p_assignment__assignment_id__Chr61__identifier_init(self, p):
        "assignment : assignment_id '=' identifier_init"
        p[0] = [p[1], p[3]]

    #    def p_assignment__assignment_id__property_path__Chr61__identifier_init(self, p):
    #        "assignment : assignment_id property_path '=' identifier_init"
    #        p[0] = [p[1], p[3]]

    def p_assignment__embedded_scm(self, p):
        "assignment : embedded_scm"
        p[0] = None

    ### assignment_id ###

    #    def p_assignment_id__LYRICS_STRING(self, p):
    #        'assignment_id : LYRICS_STRING'
    #        p[0] = SyntaxNode('assignment_id', p[1:])

    def p_assignment_id__STRING(self, p):
        "assignment_id : STRING"
        p[0] = p[1]

    ### bare_number ###

    def p_bare_number__REAL__NUMBER_IDENTIFIER(self, p):
        "bare_number : REAL NUMBER_IDENTIFIER"
        p[0] = p[1]

    def p_bare_number__UNSIGNED__NUMBER_IDENTIFIER(self, p):
        "bare_number : UNSIGNED NUMBER_IDENTIFIER"
        p[0] = p[1]

    def p_bare_number__bare_number_closed(self, p):
        "bare_number : bare_number_closed"
        p[0] = p[1]

    ### bare_number_closed ###

    def p_bare_number_closed__NUMBER_IDENTIFIER(self, p):
        "bare_number_closed : NUMBER_IDENTIFIER"
        p[0] = p[1]

    def p_bare_number_closed__REAL(self, p):
        "bare_number_closed : REAL"
        p[0] = p[1]

    def p_bare_number_closed__UNSIGNED(self, p):
        "bare_number_closed : UNSIGNED"
        p[0] = p[1]

    ### bare_unsigned ###

    def p_bare_unsigned__UNSIGNED(self, p):
        "bare_unsigned : UNSIGNED"
        p[0] = p[1]

    ### bass_figure ###

    #    def p_bass_figure__FIGURE_SPACE(self, p):
    #        'bass_figure : FIGURE_SPACE'
    #        p[0] = SyntaxNode('bass_figure', p[1:])

    #    def p_bass_figure__bass_figure__Chr93(self, p):
    #        "bass_figure : bass_figure ']'"
    #        p[0] = SyntaxNode('bass_figure', p[1:])

    #    def p_bass_figure__bass_figure__figured_bass_alteration(self, p):
    #        'bass_figure : bass_figure figured_bass_alteration'
    #        p[0] = SyntaxNode('bass_figure', p[1:])

    #    def p_bass_figure__bass_figure__figured_bass_modification(self, p):
    #        'bass_figure : bass_figure figured_bass_modification'
    #        p[0] = SyntaxNode('bass_figure', p[1:])

    #    def p_bass_figure__bass_number(self, p):
    #        'bass_figure : bass_number'
    #        p[0] = SyntaxNode('bass_figure', p[1:])

    ### bass_number ###

    #    def p_bass_number__STRING(self, p):
    #        'bass_number : STRING'
    #        p[0] = SyntaxNode('bass_number', p[1:])

    #    def p_bass_number__UNSIGNED(self, p):
    #        'bass_number : UNSIGNED'
    #        p[0] = SyntaxNode('bass_number', p[1:])

    #    def p_bass_number__full_markup(self, p):
    #        'bass_number : full_markup'
    #        p[0] = SyntaxNode('bass_number', p[1:])

    ### book_block ###

    #    def p_book_block__BOOK__Chr123__book_body__Chr125(self, p):
    #        "book_block : BOOK '{' book_body '}'"
    #        p[0] = SyntaxNode('book_block', p[1:])

    ### book_body ###

    #    def p_book_body__Empty(self, p):
    #        'book_body : '
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__BOOK_IDENTIFIER(self, p):
    #        'book_body : BOOK_IDENTIFIER'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__bookpart_block(self, p):
    #        'book_body : book_body bookpart_block'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__composite_music(self, p):
    #        'book_body : book_body composite_music'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__embedded_scm(self, p):
    #        'book_body : book_body embedded_scm'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__error(self, p):
    #        'book_body : book_body error'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__full_markup(self, p):
    #        'book_body : book_body full_markup'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__full_markup_list(self, p):
    #        'book_body : book_body full_markup_list'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__lilypond_header(self, p):
    #        'book_body : book_body lilypond_header'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__paper_block(self, p):
    #        'book_body : book_body paper_block'
    #        p[0] = SyntaxNode('book_body', p[1:])

    #    def p_book_body__book_body__score_block(self, p):
    #        'book_body : book_body score_block'
    #        p[0] = SyntaxNode('book_body', p[1:])

    ### bookpart_block ###

    #    def p_bookpart_block__BOOKPART__Chr123__bookpart_body__Chr125(self, p):
    #        "bookpart_block : BOOKPART '{' bookpart_body '}'"
    #        p[0] = SyntaxNode('bookpart_block', p[1:])

    ### bookpart_body ###

    #    def p_bookpart_body__Empty(self, p):
    #        'bookpart_body : '
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__BOOK_IDENTIFIER(self, p):
    #        'bookpart_body : BOOK_IDENTIFIER'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__composite_music(self, p):
    #        'bookpart_body : bookpart_body composite_music'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__embedded_scm(self, p):
    #        'bookpart_body : bookpart_body embedded_scm'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__error(self, p):
    #        'bookpart_body : bookpart_body error'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__full_markup(self, p):
    #        'bookpart_body : bookpart_body full_markup'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__full_markup_list(self, p):
    #        'bookpart_body : bookpart_body full_markup_list'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__lilypond_header(self, p):
    #        'bookpart_body : bookpart_body lilypond_header'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__paper_block(self, p):
    #        'bookpart_body : bookpart_body paper_block'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    #    def p_bookpart_body__bookpart_body__score_block(self, p):
    #        'bookpart_body : bookpart_body score_block'
    #        p[0] = SyntaxNode('bookpart_body', p[1:])

    ### br_bass_figure ###

    #    def p_br_bass_figure__Chr91__bass_figure(self, p):
    #        "br_bass_figure : '[' bass_figure"
    #        p[0] = SyntaxNode('br_bass_figure', p[1:])

    #    def p_br_bass_figure__bass_figure(self, p):
    #        'br_bass_figure : bass_figure'
    #        p[0] = SyntaxNode('br_bass_figure', p[1:])

    ### braced_music_list ###

    def p_braced_music_list__Chr123__music_list__Chr125(self, p):
        "braced_music_list : '{' music_list '}'"
        p[0] = p[2]

    ### chord_body ###

    def p_chord_body__ANGLE_OPEN__chord_body_elements__ANGLE_CLOSE(self, p):
        "chord_body : ANGLE_OPEN chord_body_elements ANGLE_CLOSE"
        p[0] = p[2]

    ### chord_body_element ###

    #    def p_chord_body_element__DRUM_PITCH__post_events(self, p):
    #        'chord_body_element : DRUM_PITCH post_events'
    #        p[0] = SyntaxNode('chord_body_element', p[1:])

    def p_chord_body_element__music_function_chord_body(self, p):
        "chord_body_element : music_function_chord_body"
        p[0] = SyntaxNode("chord_body_element", p[1:])

    def p_chord_body_element__pitch__exclamations__questions__octave_check__post_events(
        self, p
    ):
        "chord_body_element : pitch exclamations questions octave_check post_events"
        if p[1] not in _lyconst.drums:
            note_head = _score.NoteHead(
                written_pitch=p[1],
                is_cautionary=bool(p[3]),
                is_forced=bool(p[2]),
            )
        else:
            note_head = _score.DrumNoteHead(
                written_pitch=p[1],
                is_cautionary=bool(p[3]),
                is_forced=bool(p[2]),
            )
        p[0] = SyntaxNode("chord_body_element", (note_head, p[5]))

    ### chord_body_elements ###

    def p_chord_body_elements__Empty(self, p):
        "chord_body_elements :"
        p[0] = []

    def p_chord_body_elements__chord_body_elements__chord_body_element(self, p):
        "chord_body_elements : chord_body_elements chord_body_element"
        p[0] = p[1] + [p[2]]

    ### chord_item ###

    #    def p_chord_item__CHORD_MODIFIER(self, p):
    #        'chord_item : CHORD_MODIFIER'
    #        p[0] = SyntaxNode('chord_item', p[1:])

    #    def p_chord_item__chord_separator(self, p):
    #        'chord_item : chord_separator'
    #        p[0] = SyntaxNode('chord_item', p[1:])

    #    def p_chord_item__step_numbers(self, p):
    #        'chord_item : step_numbers'
    #        p[0] = SyntaxNode('chord_item', p[1:])

    ### chord_items ###

    #    def p_chord_items__Empty(self, p):
    #        'chord_items : '
    #        p[0] = SyntaxNode('chord_items', p[1:])

    #    def p_chord_items__chord_items__chord_item(self, p):
    #        'chord_items : chord_items chord_item'
    #        p[0] = SyntaxNode('chord_items', p[1:])

    ### chord_separator ###

    #    def p_chord_separator__CHORD_BASS__steno_tonic_pitch(self, p):
    #        'chord_separator : CHORD_BASS steno_tonic_pitch'
    #        p[0] = SyntaxNode('chord_separator', p[1:])

    #    def p_chord_separator__CHORD_CARET(self, p):
    #        'chord_separator : CHORD_CARET'
    #        p[0] = SyntaxNode('chord_separator', p[1:])

    #    def p_chord_separator__CHORD_COLON(self, p):
    #        'chord_separator : CHORD_COLON'
    #        p[0] = SyntaxNode('chord_separator', p[1:])

    #    def p_chord_separator__CHORD_SLASH__steno_tonic_pitch(self, p):
    #        'chord_separator : CHORD_SLASH steno_tonic_pitch'
    #        p[0] = SyntaxNode('chord_separator', p[1:])

    ### closed_music ###

    def p_closed_music__complex_music_prefix__closed_music(self, p):
        "closed_music : complex_music_prefix closed_music"
        p[0] = SyntaxNode("closed_music", p[1:])

    def p_closed_music__music_bare(self, p):
        "closed_music : music_bare"
        p[0] = SyntaxNode("closed_music", p[1:])

    ### command_element ###

    def p_command_element__Chr124(self, p):
        "command_element : '|'"
        p[0] = LilyPondEvent("BarCheck")

    def p_command_element__E_BACKSLASH(self, p):
        "command_element : E_BACKSLASH"
        p[0] = LilyPondEvent("VoiceSeparator")

    #    def p_command_element__E_BRACKET_CLOSE(self, p):
    #        'command_element : E_BRACKET_CLOSE'
    #        message = 'ligatures not supported.'
    #        raise Exception(message)

    #    def p_command_element__E_BRACKET_OPEN(self, p):
    #        'command_element : E_BRACKET_OPEN'
    #        message = 'ligatures not supported.'
    #        raise Exception(message)

    def p_command_element__command_event(self, p):
        "command_element : command_event"
        p[0] = p[1]

    ### command_event ###

    #    def p_command_event__E_TILDE(self, p):
    #        'command_event : E_TILDE'
    #        message = 'pes and flexa events not supported.'
    #        raise Exception(message)

    def p_command_event__tempo_event(self, p):
        "command_event : tempo_event"
        p[0] = p[1]

    ### complex_music ###

    def p_complex_music__complex_music_prefix__music(self, p):
        "complex_music : complex_music_prefix music"
        context = p[1][1]
        optional_id = p[1][2]
        optional_context_mod = p[1][3]
        music = p[2]
        p[0] = self.client._construct_context_specced_music(
            context, optional_id, optional_context_mod, music
        )

    def p_complex_music__music_function_call(self, p):
        "complex_music : music_function_call"
        p[0] = p[1]

    #    def p_complex_music__re_rhythmed_music(self, p):
    #        'complex_music : re_rhythmed_music'
    #        p[0] = SyntaxNode('complex_music', p[1:])

    #    def p_complex_music__repeated_music(self, p):
    #        'complex_music : repeated_music'
    #        p[0] = SyntaxNode('complex_music', p[1:])

    ### complex_music_prefix ###

    def p_complex_music_prefix__CONTEXT__simple_string__optional_id__optional_context_mod(
        self, p
    ):
        "complex_music_prefix : CONTEXT simple_string optional_id optional_context_mod"
        p[0] = SyntaxNode("complex_music_prefix", p.__getslice__(1, None))

    def p_complex_music_prefix__NEWCONTEXT__simple_string__optional_id__optional_context_mod(
        self, p
    ):
        "complex_music_prefix : NEWCONTEXT simple_string optional_id optional_context_mod"
        p[0] = SyntaxNode("complex_music_prefix", p.__getslice__(1, None))

    ### composite_music ###

    def p_composite_music__complex_music(self, p):
        "composite_music : complex_music"
        p[0] = p[1]

    def p_composite_music__music_bare(self, p):
        "composite_music : music_bare"
        p[0] = p[1]

    ### context_change ###

    def p_context_change__CHANGE__STRING__Chr61__STRING(self, p):
        "context_change : CHANGE STRING '=' STRING"
        p[0] = SyntaxNode("context_change", p.__getslice__(1, None))

    ### context_def_mod ###

    #    def p_context_def_mod__ACCEPTS(self, p):
    #        'context_def_mod : ACCEPTS'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__ALIAS(self, p):
    #        'context_def_mod : ALIAS'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__CONSISTS(self, p):
    #        'context_def_mod : CONSISTS'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__DEFAULTCHILD(self, p):
    #        'context_def_mod : DEFAULTCHILD'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__DENIES(self, p):
    #        'context_def_mod : DENIES'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__DESCRIPTION(self, p):
    #        'context_def_mod : DESCRIPTION'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__NAME(self, p):
    #        'context_def_mod : NAME'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__REMOVE(self, p):
    #        'context_def_mod : REMOVE'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    #    def p_context_def_mod__TYPE(self, p):
    #        'context_def_mod : TYPE'
    #        p[0] = SyntaxNode('context_def_mod', p[1:])

    ### context_def_spec_block ###

    def p_context_def_spec_block__CONTEXT__Chr123__context_def_spec_body__Chr125(
        self, p
    ):
        "context_def_spec_block : CONTEXT '{' context_def_spec_body '}'"
        p[0] = SyntaxNode("context_def_spec_block", p.__getslice__(1, None))

    ### context_def_spec_body ###

    def p_context_def_spec_body__CONTEXT_DEF_IDENTIFIER(self, p):
        "context_def_spec_body : CONTEXT_DEF_IDENTIFIER"
        p[0] = SyntaxNode("context_def_spec_body", p.__getslice__(1, None))

    def p_context_def_spec_body__Empty(self, p):
        "context_def_spec_body :"
        p[0] = SyntaxNode("context_def_spec_body", p.__getslice__(1, None))

    def p_context_def_spec_body__context_def_spec_body__context_mod(self, p):
        "context_def_spec_body : context_def_spec_body context_mod"
        p[0] = SyntaxNode("context_def_spec_body", p.__getslice__(1, None))

    def p_context_def_spec_body__context_def_spec_body__context_modification(self, p):
        "context_def_spec_body : context_def_spec_body context_modification"
        p[0] = SyntaxNode("context_def_spec_body", p.__getslice__(1, None))

    def p_context_def_spec_body__context_def_spec_body__embedded_scm(self, p):
        "context_def_spec_body : context_def_spec_body embedded_scm"
        p[0] = SyntaxNode("context_def_spec_body", p.__getslice__(1, None))

    ### context_mod ###

    #    def p_context_mod__context_def_mod__STRING(self, p):
    #        'context_mod : context_def_mod STRING'
    #        p[0] = SyntaxNode('context_mod', p[1:])

    #    def p_context_mod__context_def_mod__embedded_scm(self, p):
    #        'context_mod : context_def_mod embedded_scm'
    #        p[0] = SyntaxNode('context_mod', p[1:])

    def p_context_mod__property_operation(self, p):
        "context_mod : property_operation"
        p[0] = p[1]

    ### context_mod_list ###

    def p_context_mod_list__Empty(self, p):
        "context_mod_list :"
        p[0] = []

    def p_context_mod_list__context_mod_list__CONTEXT_MOD_IDENTIFIER(self, p):
        "context_mod_list : context_mod_list CONTEXT_MOD_IDENTIFIER"
        p[0] = p[1] + [p[2]]

    def p_context_mod_list__context_mod_list__context_mod(self, p):
        "context_mod_list : context_mod_list context_mod"
        p[0] = p[1] + [p[2]]

    def p_context_mod_list__context_mod_list__embedded_scm(self, p):
        "context_mod_list : context_mod_list embedded_scm"
        p[0] = p[1] + [p[2]]

    ### context_modification ###

    def p_context_modification__CONTEXT_MOD_IDENTIFIER(self, p):
        "context_modification : CONTEXT_MOD_IDENTIFIER"
        p[0] = [p[1]]

    def p_context_modification__WITH__CONTEXT_MOD_IDENTIFIER(self, p):
        "context_modification : WITH CONTEXT_MOD_IDENTIFIER"
        p[0] = [p[2]]

    def p_context_modification__WITH__Chr123__context_mod_list__Chr125(self, p):
        "context_modification : WITH '{' context_mod_list '}'"
        p[0] = p[3]
        self.client._lexer.pop_state()
        self.client._relex_lookahead()

    def p_context_modification__WITH__embedded_scm_closed(self, p):
        "context_modification : WITH embedded_scm_closed"
        p[0] = [p[2]]

    ### context_prop_spec ###

    def p_context_prop_spec__simple_string(self, p):
        "context_prop_spec : simple_string"
        p[0] = SyntaxNode("context_prop_spec", p.__getslice__(1, None))

    def p_context_prop_spec__simple_string__Chr46__simple_string(self, p):
        "context_prop_spec : simple_string '.' simple_string"
        p[0] = SyntaxNode("context_prop_spec", p.__getslice__(1, None))

    ### direction_less_char ###

    def p_direction_less_char__Chr126(self, p):
        "direction_less_char : '~'"
        ### p[0] = self.client._resolve_event_identifier("tildeSymbol")
        p[0] = self.client._resolve_event_identifier("~")

    def p_direction_less_char__Chr40(self, p):
        "direction_less_char : '('"
        ### p[0] = self.client._resolve_event_identifier("parenthesisOpenSymbol")
        p[0] = self.client._resolve_event_identifier("(")

    def p_direction_less_char__Chr41(self, p):
        "direction_less_char : ')'"
        ### p[0] = self.client._resolve_event_identifier("parenthesisCloseSymbol")
        p[0] = self.client._resolve_event_identifier(")")

    def p_direction_less_char__Chr91(self, p):
        "direction_less_char : '['"
        # p[0] = self.client._resolve_event_identifier("bracketOpenSymbol")
        p[0] = self.client._resolve_event_identifier("[")

    def p_direction_less_char__Chr93(self, p):
        "direction_less_char : ']'"
        # p[0] = self.client._resolve_event_identifier("bracketCloseSymbol")
        p[0] = self.client._resolve_event_identifier("]")

    def p_direction_less_char__E_ANGLE_CLOSE(self, p):
        "direction_less_char : E_ANGLE_CLOSE"
        # p[0] = self.client._resolve_event_identifier("escapedBiggerSymbol")
        p[0] = self.client._resolve_event_identifier(r"\>")

    def p_direction_less_char__E_ANGLE_OPEN(self, p):
        "direction_less_char : E_ANGLE_OPEN"
        # p[0] = self.client._resolve_event_identifier("escapedSmallerSymbol")
        p[0] = self.client._resolve_event_identifier(r"\<")

    def p_direction_less_char__E_CLOSE(self, p):
        "direction_less_char : E_CLOSE"
        # p[0] = self.client._resolve_event_identifier("escapedParenthesisCloseSymbol")
        p[0] = self.client._resolve_event_identifier(r"\)")

    def p_direction_less_char__E_EXCLAMATION(self, p):
        "direction_less_char : E_EXCLAMATION"
        # p[0] = self.client._resolve_event_identifier("escapedExclamationSymbol")
        p[0] = self.client._resolve_event_identifier(r"\!")

    def p_direction_less_char__E_OPEN(self, p):
        "direction_less_char : E_OPEN"
        # p[0] = self.client._resolve_event_identifier("escapedParenthesisOpenSymbol")
        p[0] = self.client._resolve_event_identifier(r"\(")

    ### direction_less_event ###

    def p_direction_less_event__EVENT_IDENTIFIER(self, p):
        "direction_less_event : EVENT_IDENTIFIER"
        identifier = p[1]
        if identifier.startswith("\\"):
            identifier = identifier[1:]
        p[0] = self.client._resolve_event_identifier(identifier)

    def p_direction_less_event__direction_less_char(self, p):
        "direction_less_event : direction_less_char"
        p[0] = p[1]

    def p_direction_less_event__event_function_event(self, p):
        "direction_less_event : event_function_event"
        p[0] = SyntaxNode("direction_less_event", p.__getslice__(1, None))

    def p_direction_less_event__tremolo_type(self, p):
        "direction_less_event : tremolo_type"
        p[0] = p[1]

    ### direction_reqd_event ###

    def p_direction_reqd_event__gen_text_def(self, p):
        "direction_reqd_event : gen_text_def"
        p[0] = p[1]

    def p_direction_reqd_event__script_abbreviation(self, p):
        "direction_reqd_event : script_abbreviation"
        p[0] = p[1]

    ### dots ###

    def p_dots__Empty(self, p):
        "dots :"
        p[0] = SyntaxNode("dots", 0)

    def p_dots__dots__Chr46(self, p):
        "dots : dots '.'"
        p[0] = SyntaxNode("dots", p[1].value + 1)

    ### duration_length ###

    def p_duration_length__multiplied_duration(self, p):
        "duration_length : multiplied_duration"
        p[0] = p[1]

    ### embedded_lilypond ###

    #    def p_embedded_lilypond__Empty(self, p):
    #        'embedded_lilypond : '
    #        p[0] = SyntaxNode('embedded_lilypond', p[1:])

    #    def p_embedded_lilypond__INVALID__embedded_lilypond(self, p):
    #        'embedded_lilypond : INVALID embedded_lilypond'
    #        p[0] = SyntaxNode('embedded_lilypond', p[1:])

    #    def p_embedded_lilypond__error(self, p):
    #        'embedded_lilypond : error'
    #        p[0] = SyntaxNode('embedded_lilypond', p[1:])

    #    def p_embedded_lilypond__identifier_init(self, p):
    #        'embedded_lilypond : identifier_init'
    #        p[0] = SyntaxNode('embedded_lilypond', p[1:])

    #    def p_embedded_lilypond__music__music__music_list(self, p):
    #        'embedded_lilypond : music music music_list'
    #        p[0] = SyntaxNode('embedded_lilypond', p[1:])

    ### embedded_scm ###

    def p_embedded_scm__embedded_scm_bare(self, p):
        "embedded_scm : embedded_scm_bare"
        p[0] = p[1]

    def p_embedded_scm__scm_function_call(self, p):
        "embedded_scm : scm_function_call"
        p[0] = p[1]

    ### embedded_scm_arg ###

    def p_embedded_scm_arg__embedded_scm_bare_arg(self, p):
        "embedded_scm_arg : embedded_scm_bare_arg"
        p[0] = p[1]

    def p_embedded_scm_arg__music_arg(self, p):
        "embedded_scm_arg : music_arg"
        p[0] = p[1]

    def p_embedded_scm_arg__scm_function_call(self, p):
        "embedded_scm_arg : scm_function_call"
        p[0] = p[1]

    ### embedded_scm_arg_closed ###

    def p_embedded_scm_arg_closed__closed_music(self, p):
        "embedded_scm_arg_closed : closed_music"
        p[0] = p[1]

    def p_embedded_scm_arg_closed__embedded_scm_bare_arg(self, p):
        "embedded_scm_arg_closed : embedded_scm_bare_arg"
        p[0] = p[1]

    def p_embedded_scm_arg_closed__scm_function_call_closed(self, p):
        "embedded_scm_arg_closed : scm_function_call_closed"
        p[0] = p[1]

    ### embedded_scm_bare ###

    def p_embedded_scm_bare__SCM_IDENTIFIER(self, p):
        "embedded_scm_bare : SCM_IDENTIFIER"
        p[0] = p[1]

    def p_embedded_scm_bare__SCM_TOKEN(self, p):
        "embedded_scm_bare : SCM_TOKEN"
        p[0] = p[1]

    ### embedded_scm_bare_arg ###

    def p_embedded_scm_bare_arg__STRING(self, p):
        "embedded_scm_bare_arg : STRING"
        p[0] = p[1]

    def p_embedded_scm_bare_arg__STRING_IDENTIFIER(self, p):
        "embedded_scm_bare_arg : STRING_IDENTIFIER"
        p[0] = p[1]

    #    def p_embedded_scm_bare_arg__book_block(self, p):
    #        'embedded_scm_bare_arg : book_block'
    #        p[0] = p[1]

    #    def p_embedded_scm_bare_arg__bookpart_block(self, p):
    #        'embedded_scm_bare_arg : bookpart_block'
    #        p[0] = p[1]

    def p_embedded_scm_bare_arg__context_def_spec_block(self, p):
        "embedded_scm_bare_arg : context_def_spec_block"
        p[0] = p[1]

    def p_embedded_scm_bare_arg__context_modification(self, p):
        "embedded_scm_bare_arg : context_modification"
        p[0] = p[1]

    def p_embedded_scm_bare_arg__embedded_scm_bare(self, p):
        "embedded_scm_bare_arg : embedded_scm_bare"
        p[0] = p[1]

    def p_embedded_scm_bare_arg__full_markup(self, p):
        "embedded_scm_bare_arg : full_markup"
        p[0] = p[1]

    def p_embedded_scm_bare_arg__full_markup_list(self, p):
        "embedded_scm_bare_arg : full_markup_list"
        p[0] = p[1]

    def p_embedded_scm_bare_arg__output_def(self, p):
        "embedded_scm_bare_arg : output_def"
        p[0] = p[1]

    def p_embedded_scm_bare_arg__score_block(self, p):
        "embedded_scm_bare_arg : score_block"
        p[0] = p[1]

    ### embedded_scm_chord_body ###

    def p_embedded_scm_chord_body__SCM_FUNCTION__music_function_chord_body_arglist(
        self, p
    ):
        "embedded_scm_chord_body : SCM_FUNCTION music_function_chord_body_arglist"
        p[0] = SyntaxNode("embedded_scm_chord_body", p[1:])

    def p_embedded_scm_chord_body__bare_number(self, p):
        "embedded_scm_chord_body : bare_number"
        p[0] = p[1]

    def p_embedded_scm_chord_body__chord_body_element(self, p):
        "embedded_scm_chord_body : chord_body_element"
        p[0] = p[1]

    def p_embedded_scm_chord_body__embedded_scm_bare_arg(self, p):
        "embedded_scm_chord_body : embedded_scm_bare_arg"
        p[0] = p[1]

    def p_embedded_scm_chord_body__fraction(self, p):
        "embedded_scm_chord_body : fraction"
        p[0] = p[1]

    #    def p_embedded_scm_chord_body__lyric_element(self, p):
    #        'embedded_scm_chord_body : lyric_element'
    #        p[0] = p[1]

    ### embedded_scm_closed ###

    def p_embedded_scm_closed__embedded_scm_bare(self, p):
        "embedded_scm_closed : embedded_scm_bare"
        p[0] = p[1]

    def p_embedded_scm_closed__scm_function_call_closed(self, p):
        "embedded_scm_closed : scm_function_call_closed"
        p[0] = p[1]

    ### event_chord ###

    def p_event_chord__CHORD_REPETITION__optional_notemode_duration__post_events(
        self, p
    ):
        "event_chord : CHORD_REPETITION optional_notemode_duration post_events"
        pitches = self.client._last_chord.written_pitches
        duration = p[2].duration
        chord = _score.Chord(pitches, duration, tag=self.tag)
        self.client._chord_pitch_orders[chord] = pitches
        if p[2].multiplier is not None:
            multiplier = fractions.Fraction(p[2].multiplier)
            chord.multiplier = multiplier
        self.client._process_post_events(chord, p[3])
        annotation = {"UnrelativableMusic": True}
        _bind._unsafe_attach(annotation, chord)
        if self.client._last_chord not in self.client._repeated_chords:
            self.client._repeated_chords[self.client._last_chord] = []
        self.client._repeated_chords[self.client._last_chord].append(chord)
        p[0] = chord

    def p_event_chord__MULTI_MEASURE_REST__optional_notemode_duration__post_events(
        self, p
    ):
        "event_chord : MULTI_MEASURE_REST optional_notemode_duration post_events"
        rest = _score.MultimeasureRest(p[2].duration, tag=self.tag)
        if p[2].multiplier is not None:
            multiplier = fractions.Fraction(p[2].multiplier)
            rest.multiplier = _duration.pair(multiplier)
        self.client._process_post_events(rest, p[3])
        p[0] = rest

    def p_event_chord__command_element(self, p):
        "event_chord : command_element"
        p[0] = p[1]

    def p_event_chord__note_chord_element(self, p):
        "event_chord : note_chord_element"
        self.client._last_chord = p[1]
        p[0] = p[1]

    def p_event_chord__simple_chord_elements__post_events(self, p):
        "event_chord : simple_chord_elements post_events"
        self.client._process_post_events(p[1], p[2])
        p[0] = p[1]

    ### event_function_event ###

    def p_event_function_event__EVENT_FUNCTION__function_arglist_closed(self, p):
        "event_function_event : EVENT_FUNCTION function_arglist_closed"
        p[0] = SyntaxNode("event_function_event", p[1:])

    ### exclamations ###

    def p_exclamations__Empty(self, p):
        "exclamations :"
        p[0] = 0

    def p_exclamations__exclamations__Chr33(self, p):
        "exclamations : exclamations '!'"
        p[0] = p[1] + 1

    ### figure_list ###

    #    def p_figure_list__Empty(self, p):
    #        'figure_list : '
    #        p[0] = SyntaxNode('figure_list', p[1:])

    #    def p_figure_list__figure_list__br_bass_figure(self, p):
    #        'figure_list : figure_list br_bass_figure'
    #        p[0] = SyntaxNode('figure_list', p[1:])

    ### figure_spec ###

    #    def p_figure_spec__FIGURE_OPEN__figure_list__FIGURE_CLOSE(self, p):
    #        'figure_spec : FIGURE_OPEN figure_list FIGURE_CLOSE'
    #        p[0] = SyntaxNode('figure_spec', p[1:])

    ### figured_bass_alteration ###

    #    def p_figured_bass_alteration__Chr33(self, p):
    #        "figured_bass_alteration : '!'"
    #        p[0] = SyntaxNode('figured_bass_alteration', p[1:])

    #    def p_figured_bass_alteration__Chr43(self, p):
    #        "figured_bass_alteration : '+'"
    #        p[0] = SyntaxNode('figured_bass_alteration', p[1:])

    #    def p_figured_bass_alteration__Chr45(self, p):
    #        "figured_bass_alteration : '-'"
    #        p[0] = SyntaxNode('figured_bass_alteration', p[1:])

    ### figured_bass_modification ###

    #    def p_figured_bass_modification__Chr47(self, p):
    #        "figured_bass_modification : '/'"
    #        p[0] = SyntaxNode('figured_bass_modification', p[1:])

    #    def p_figured_bass_modification__E_BACKSLASH(self, p):
    #        'figured_bass_modification : E_BACKSLASH'
    #        p[0] = SyntaxNode('figured_bass_modification', p[1:])

    #    def p_figured_bass_modification__E_EXCLAMATION(self, p):
    #        'figured_bass_modification : E_EXCLAMATION'
    #        p[0] = SyntaxNode('figured_bass_modification', p[1:])

    #    def p_figured_bass_modification__E_PLUS(self, p):
    #        'figured_bass_modification : E_PLUS'
    #        p[0] = SyntaxNode('figured_bass_modification', p[1:])

    ### fingering ###

    def p_fingering__UNSIGNED(self, p):
        "fingering : UNSIGNED"
        p[0] = SyntaxNode("fingering", p[1:])

    ### fraction ###

    def p_fraction__FRACTION(self, p):
        "fraction : FRACTION"
        p[0] = p[1]

    def p_fraction__UNSIGNED__Chr47__UNSIGNED(self, p):
        "fraction : UNSIGNED '/' UNSIGNED"
        p[0] = fractions.Fraction(p[1], p[3])

    ### full_markup ###

    def p_full_markup__MARKUP_IDENTIFIER(self, p):
        "full_markup : MARKUP_IDENTIFIER"
        p[0] = SyntaxNode("full_markup", p.__getslice__(1, None))

    def p_full_markup__MARKUP__markup_top(self, p):
        "full_markup : MARKUP markup_top"
        parts = []
        for item in p[2]:
            if isinstance(item, MarkupCommand):
                parts.append(item._get_lilypond_format())
            else:
                parts.append(item)
        string = " ".join(parts)
        string = rf"\markup {{ {string} }}"
        p[0] = _indicators.Markup(string)
        self.client._lexer.pop_state()
        self.client._relex_lookahead()

    ### full_markup_list ###

    def p_full_markup_list__MARKUPLIST_IDENTIFIER(self, p):
        "full_markup_list : MARKUPLIST_IDENTIFIER"
        # p[0] = SyntaxNode('full_markup_list', p[1:])
        p[0] = p[1]

    def p_full_markup_list__MARKUPLIST__markup_list(self, p):
        "full_markup_list : MARKUPLIST markup_list"
        # p[0] = SyntaxNode('full_markup_list', p[1:])
        p[0] = p[2]

    ### function_arglist ###

    def p_function_arglist__function_arglist_common(self, p):
        "function_arglist : function_arglist_common"
        p[0] = p[1]

    def p_function_arglist__function_arglist_nonbackup(self, p):
        "function_arglist : function_arglist_nonbackup"
        p[0] = p[1]

    ### function_arglist_backup ###

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed_keep__duration_length(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_closed_keep duration_length"
        p[0] = p[3] + [p[4]]

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_keep__pitch_also_in_chords(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_keep pitch_also_in_chords"
        p[0] = p[3] + [p[4]]

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__BACKUP(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup BACKUP"
        p[0] = p[3] + [p[1]]
        self.client._backup_token(False, None)

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__NUMBER_IDENTIFIER(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep '-' NUMBER_IDENTIFIER"
        n = -1 * p[5]
        if self.client._test_scheme_predicate(p[2], n):
            p[0] = p[3] + [p[1]]
        else:
            self.client._backup_token("NUMBER_IDENTIFIER", n)

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__REAL(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep '-' REAL"
        n = -1 * p[5]
        if self.client._test_scheme_predicate(p[2], n):
            self.client._reparse_token(p[2], "REAL", n)
            p[0] = p[3]
        else:
            self.client._backup_token("REAL", n)

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__UNSIGNED(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep '-' UNSIGNED"
        n = -1 * p[5]
        if self.client._test_scheme_predicates(p[2], n):
            self.client._reparse_token(p[2], "REAL", n)
            p[0] = p[3]
        else:
            # This would normally create a FingeringEvent, and test that against the predicate
            self.client._backup_token("REAL", n)
            p[0] = p[3] + [p[1]]

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__FRACTION(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep FRACTION"
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token("FRACTION", p[4])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__NUMBER_IDENTIFIER(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep NUMBER_IDENTIFIER"
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token("NUMBER_IDENTIFIER", p[4])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__REAL(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep REAL"
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3]
            self.client._reparse_token(p[2], "REAL", p[4])
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token("REAL", p[4])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__UNSIGNED(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep UNSIGNED"
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3]
            self.client._reparse_token(p[2], "UNSIGNED", p[4])
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token("UNSIGNED", p[4])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__post_event_nofinger(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep post_event_nofinger"
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token("EVENT_IDENTIFIER", p[4])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_keep__embedded_scm_arg_closed(
        self, p
    ):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_keep embedded_scm_arg_closed"
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token("SCM_IDENTIFIER", p[4])

    #    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_keep__lyric_element(self, p):
    #        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_keep lyric_element'
    #        if self.client._test_scheme_predicate(p[2], p[4]):
    #            p[0] = p[3] + [p[4]]
    #        else:
    #            p[0] = p[3] + [p[1]]
    #            self.client._backup_token('LYRICS_STRING', p[4])

    def p_function_arglist_backup__function_arglist_backup__REPARSE__bare_number(
        self, p
    ):
        "function_arglist_backup : function_arglist_backup REPARSE bare_number"
        p[0] = self.client._check_scheme_argument(p[1], p[3], p[2])

    def p_function_arglist_backup__function_arglist_backup__REPARSE__embedded_scm_arg_closed(
        self, p
    ):
        "function_arglist_backup : function_arglist_backup REPARSE embedded_scm_arg_closed"
        p[0] = self.client._check_scheme_argument(p[1], p[3], p[2])

    def p_function_arglist_backup__function_arglist_backup__REPARSE__fraction(self, p):
        "function_arglist_backup : function_arglist_backup REPARSE fraction"
        p[0] = self.client._check_scheme_argument(p[1], p[3], p[2])

    ### function_arglist_bare ###

    def p_function_arglist_bare__EXPECT_DURATION__function_arglist_closed_optional__duration_length(
        self, p
    ):
        "function_arglist_bare : EXPECT_DURATION function_arglist_closed_optional duration_length"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_bare__EXPECT_NO_MORE_ARGS(self, p):
        "function_arglist_bare : EXPECT_NO_MORE_ARGS"
        p[0] = []

    def p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_skip__DEFAULT(
        self, p
    ):
        "function_arglist_bare : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_skip DEFAULT"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_skip__DEFAULT(
        self, p
    ):
        "function_arglist_bare : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_skip DEFAULT"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip__DEFAULT(
        self, p
    ):
        "function_arglist_bare : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip DEFAULT"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_bare__EXPECT_PITCH__function_arglist_optional__pitch_also_in_chords(
        self, p
    ):
        "function_arglist_bare : EXPECT_PITCH function_arglist_optional pitch_also_in_chords"
        p[0] = p[2] + [p[3]]

    ### function_arglist_closed ###

    def p_function_arglist_closed__function_arglist_closed_common(self, p):
        "function_arglist_closed : function_arglist_closed_common"
        p[0] = p[1]

    def p_function_arglist_closed__function_arglist_nonbackup(self, p):
        "function_arglist_closed : function_arglist_nonbackup"
        p[0] = p[1]

    ### function_arglist_closed_common ###

    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__NUMBER_IDENTIFIER(
        self, p
    ):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional '-' NUMBER_IDENTIFIER"
        p[0] = p[2] + [-1 * p[4]]

    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__REAL(
        self, p
    ):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional '-' REAL"
        p[0] = p[2] + [-1 * p[4]]

    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__UNSIGNED(
        self, p
    ):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional '-' UNSIGNED"
        p[0] = p[2] + [-1 * p[4]]

    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__bare_number(
        self, p
    ):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional bare_number"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__fraction(
        self, p
    ):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional fraction"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__post_event_nofinger(
        self, p
    ):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional post_event_nofinger"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_optional__embedded_scm_arg_closed(
        self, p
    ):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_optional embedded_scm_arg_closed"
        p[0] = p[2] + [p[3]]

    #    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_optional__lyric_element(self, p):
    #        'function_arglist_closed_common : EXPECT_SCM function_arglist_optional lyric_element'
    #        p[0] = p[2] + [p[3]]

    def p_function_arglist_closed_common__function_arglist_bare(self, p):
        "function_arglist_closed_common : function_arglist_bare"
        p[0] = p[1]

    ### function_arglist_closed_keep ###

    def p_function_arglist_closed_keep__function_arglist_backup(self, p):
        "function_arglist_closed_keep : function_arglist_backup"
        p[0] = p[1]

    def p_function_arglist_closed_keep__function_arglist_closed_common(self, p):
        "function_arglist_closed_keep : function_arglist_closed_common"
        p[0] = p[1]

    ### function_arglist_closed_optional ###

    def p_function_arglist_closed_optional__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed_optional(
        self, p
    ):
        "function_arglist_closed_optional : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_closed_optional"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_closed_optional__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_closed_optional(
        self, p
    ):
        "function_arglist_closed_optional : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_closed_optional"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_closed_optional__function_arglist_backup__BACKUP(self, p):
        "function_arglist_closed_optional : function_arglist_backup BACKUP"
        p[0] = p[1]

    def p_function_arglist_closed_optional__function_arglist_closed_keep(self, p):
        "function_arglist_closed_optional : function_arglist_closed_keep %prec FUNCTION_ARGLIST"
        p[0] = p[1]

    ### function_arglist_common ###

    def p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__bare_number(
        self, p
    ):
        "function_arglist_common : EXPECT_SCM function_arglist_closed_optional bare_number"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__fraction(
        self, p
    ):
        "function_arglist_common : EXPECT_SCM function_arglist_closed_optional fraction"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__post_event_nofinger(
        self, p
    ):
        "function_arglist_common : EXPECT_SCM function_arglist_closed_optional post_event_nofinger"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_common__EXPECT_SCM__function_arglist_optional__embedded_scm_arg(
        self, p
    ):
        "function_arglist_common : EXPECT_SCM function_arglist_optional embedded_scm_arg"
        p[0] = p[2] + [p[3]]

    def p_function_arglist_common__function_arglist_bare(self, p):
        "function_arglist_common : function_arglist_bare"
        p[0] = p[1]

    #    def p_function_arglist_common__function_arglist_common_lyric(self, p):
    #        'function_arglist_common : function_arglist_common_lyric'
    #        p[0] = p[1]

    def p_function_arglist_common__function_arglist_common_minus(self, p):
        "function_arglist_common : function_arglist_common_minus"
        p[0] = p[1]

    ### function_arglist_common_lyric ###

    #    def p_function_arglist_common_lyric__EXPECT_SCM__function_arglist_optional__lyric_element(self, p):
    #        'function_arglist_common_lyric : EXPECT_SCM function_arglist_optional lyric_element'
    #        p[0] = p[2] + [p[3]]

    #    def p_function_arglist_common_lyric__function_arglist_common_lyric__REPARSE__lyric_element_arg(self, p):
    #        'function_arglist_common_lyric : function_arglist_common_lyric REPARSE lyric_element_arg'
    #        p[0] = p[1] + [p[3]]

    ### function_arglist_common_minus ###

    def p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__NUMBER_IDENTIFIER(
        self, p
    ):
        "function_arglist_common_minus : EXPECT_SCM function_arglist_closed_optional '-' NUMBER_IDENTIFIER"
        p[0] = p[2] + [-1 * p[4]]

    def p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__REAL(
        self, p
    ):
        "function_arglist_common_minus : EXPECT_SCM function_arglist_closed_optional '-' REAL"
        p[0] = p[2] + [-1 * p[3]]

    def p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__UNSIGNED(
        self, p
    ):
        "function_arglist_common_minus : EXPECT_SCM function_arglist_closed_optional '-' UNSIGNED"
        p[0] = p[2] + [-1 * p[3]]

    def p_function_arglist_common_minus__function_arglist_common_minus__REPARSE__bare_number(
        self, p
    ):
        "function_arglist_common_minus : function_arglist_common_minus REPARSE bare_number"
        p[0] = p[1] + [p[3]]

    ### function_arglist_keep ###

    def p_function_arglist_keep__function_arglist_backup(self, p):
        "function_arglist_keep : function_arglist_backup"
        p[0] = p[1]

    def p_function_arglist_keep__function_arglist_common(self, p):
        "function_arglist_keep : function_arglist_common"
        p[0] = p[1]

    ### function_arglist_nonbackup ###

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed__duration_length(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_closed duration_length"
        p[0] = p[3] + [p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist__pitch_also_in_chords(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_PITCH function_arglist pitch_also_in_chords"
        p[0] = p[3] + [p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist__embedded_scm_arg_closed(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist embedded_scm_arg_closed"
        p[0] = p[3] + [p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__NUMBER_IDENTIFIER(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed '-' NUMBER_IDENTIFIER"
        p[0] = p[3] + [-1 * p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__REAL(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed '-' REAL"
        p[0] = p[3] + [-1 * p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__UNSIGNED(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed '-' UNSIGNED"
        p[0] = p[3] + [-1 * p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__FRACTION(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed FRACTION"
        p[0] = p[3] + [p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__bare_number_closed(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed bare_number_closed"
        p[0] = p[3] + [p[4]]

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__post_event_nofinger(
        self, p
    ):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed post_event_nofinger"
        p[0] = p[3] + [p[4]]

    ### function_arglist_optional ###

    def p_function_arglist_optional__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_optional(
        self, p
    ):
        "function_arglist_optional : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_optional"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_optional__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_optional(
        self, p
    ):
        "function_arglist_optional : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_optional"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_optional__function_arglist_backup__BACKUP(self, p):
        "function_arglist_optional : function_arglist_backup BACKUP"
        p[0] = p[1]

    def p_function_arglist_optional__function_arglist_keep(self, p):
        "function_arglist_optional : function_arglist_keep %prec FUNCTION_ARGLIST"
        p[0] = p[1]

    ### function_arglist_skip ###

    def p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_skip(
        self, p
    ):
        "function_arglist_skip : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_skip %prec FUNCTION_ARGLIST"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_skip(
        self, p
    ):
        "function_arglist_skip : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_skip %prec FUNCTION_ARGLIST"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip(
        self, p
    ):
        "function_arglist_skip : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip %prec FUNCTION_ARGLIST"
        p[0] = p[3] + [p[1]]

    def p_function_arglist_skip__function_arglist_common(self, p):
        "function_arglist_skip : function_arglist_common"
        p[0] = p[1]

    ### gen_text_def ###

    def p_gen_text_def__full_markup(self, p):
        "gen_text_def : full_markup"
        p[0] = p[1]

    def p_gen_text_def__simple_string(self, p):
        "gen_text_def : simple_string"
        # assert isinstance(p[1], str), repr(p[1])
        p[0] = _indicators.Markup(rf"\markup {{ {p[1]} }}")

    ### grouped_music_list ###

    def p_grouped_music_list__sequential_music(self, p):
        "grouped_music_list : sequential_music"
        p[0] = p[1]

    def p_grouped_music_list__simultaneous_music(self, p):
        "grouped_music_list : simultaneous_music"
        p[0] = p[1]

    ### identifier_init ###

    #    def p_identifier_init__book_block(self, p):
    #        'identifier_init : book_block'
    #        p[0] = SyntaxNode('book_block', p[1])

    #    def p_identifier_init__bookpart_block(self, p):
    #        'identifier_init : bookpart_block'
    #        p[0] = SyntaxNode('bookpart_block', p[1])

    def p_identifier_init__context_def_spec_block(self, p):
        "identifier_init : context_def_spec_block"
        p[0] = SyntaxNode("context_def_spec_block", p[1])

    def p_identifier_init__context_modification(self, p):
        "identifier_init : context_modification"
        p[0] = SyntaxNode("context_modification", p[1])

    def p_identifier_init__embedded_scm(self, p):
        "identifier_init : embedded_scm"
        p[0] = SyntaxNode("embedded_scm", p[1])

    def p_identifier_init__full_markup(self, p):
        "identifier_init : full_markup"
        p[0] = SyntaxNode("full_markup", p[1])

    def p_identifier_init__full_markup_list(self, p):
        "identifier_init : full_markup_list"
        p[0] = SyntaxNode("full_markup_list", p[1])

    def p_identifier_init__music(self, p):
        "identifier_init : music"
        p[0] = SyntaxNode("music", p[1])

    def p_identifier_init__number_expression(self, p):
        "identifier_init : number_expression"
        p[0] = SyntaxNode("number_expression", p[1])

    def p_identifier_init__output_def(self, p):
        "identifier_init : output_def"
        p[0] = SyntaxNode("output_def", p[1])

    def p_identifier_init__post_event_nofinger(self, p):
        "identifier_init : post_event_nofinger"
        p[0] = SyntaxNode("post_event_nofinger", p[1])

    def p_identifier_init__score_block(self, p):
        "identifier_init : score_block"
        p[0] = SyntaxNode("score_block", p[1])

    def p_identifier_init__string(self, p):
        "identifier_init : string"
        p[0] = SyntaxNode("string", p[1])

    ### lilypond ###

    def p_lilypond__Empty(self, p):
        "lilypond :"
        p[0] = []

    #    def p_lilypond__lilypond__INVALID(self, p):
    #        'lilypond : lilypond INVALID'
    #        p[0] = p[1]

    def p_lilypond__lilypond__assignment(self, p):
        "lilypond : lilypond assignment"
        p[0] = p[1]
        if p[2] is not None:
            self.client._assign_variable(p[2][0], p[2][1])

    def p_lilypond__lilypond__error(self, p):
        "lilypond : lilypond error"
        p[0] = p[1]

    def p_lilypond__lilypond__toplevel_expression(self, p):
        "lilypond : lilypond toplevel_expression"
        p[0] = p[1] + [p[2]]

    ### lilypond_header ###

    def p_lilypond_header__HEADER__Chr123__lilypond_header_body__Chr125(self, p):
        "lilypond_header : HEADER '{' lilypond_header_body '}'"
        self.client._pop_variable_scope()
        p[0] = p[3]

    ### lilypond_header_body ###

    def p_lilypond_header_body__Empty(self, p):
        "lilypond_header_body :"
        self.client._push_variable_scope()
        p[0] = _lilypondfile.Block(name="header")

    def p_lilypond_header_body__lilypond_header_body__assignment(self, p):
        "lilypond_header_body : lilypond_header_body assignment"
        self.client._assign_variable(p[2][0], p[2][1])
        setattr(p[1], p[2][0], p[2][1].value)
        p[0] = p[1]

    ### lyric_element ###

    #    def p_lyric_element__LYRICS_STRING(self, p):
    #        'lyric_element : LYRICS_STRING'
    #        p[0] = SyntaxNode('lyric_element', p[1:])

    #    def p_lyric_element__lyric_markup(self, p):
    #        'lyric_element : lyric_markup'
    #        p[0] = SyntaxNode('lyric_element', p[1:])

    ### lyric_element_arg ###

    #    def p_lyric_element_arg__LYRIC_ELEMENT__optional_notemode_duration__post_events(self, p):
    #        'lyric_element_arg : LYRIC_ELEMENT optional_notemode_duration post_events'
    #        p[0] = SyntaxNode('lyric_element_arg', p[1:])

    #    def p_lyric_element_arg__lyric_element(self, p):
    #        'lyric_element_arg : lyric_element'
    #        p[0] = SyntaxNode('lyric_element_arg', p[1:])

    #    def p_lyric_element_arg__lyric_element__multiplied_duration__post_events(self, p):
    #        'lyric_element_arg : lyric_element multiplied_duration post_events'
    #        p[0] = SyntaxNode('lyric_element_arg', p[1:])

    #    def p_lyric_element_arg__lyric_element__post_event__post_events(self, p):
    #        'lyric_element_arg : lyric_element post_event post_events'
    #        p[0] = SyntaxNode('lyric_element_arg', p[1:])

    ### lyric_element_music ###

    #    def p_lyric_element_music__lyric_element__optional_notemode_duration__post_events(self, p):
    #        'lyric_element_music : lyric_element optional_notemode_duration post_events'
    #        p[0] = SyntaxNode('lyric_element_music', p[1:])

    ### lyric_markup ###

    #    def p_lyric_markup__LYRIC_MARKUP_IDENTIFIER(self, p):
    #        'lyric_markup : LYRIC_MARKUP_IDENTIFIER'
    #        p[0] = SyntaxNode('lyric_markup', p[1:])

    #    def p_lyric_markup__LYRIC_MARKUP__markup_top(self, p):
    #        'lyric_markup : LYRIC_MARKUP markup_top'
    #        p[0] = SyntaxNode('lyric_markup', p[1:])

    ### markup ###

    def p_markup__markup_head_1_list__simple_markup(self, p):
        "markup : markup_head_1_list simple_markup"
        markup = p[2]
        for item in reversed(p[1]):
            command = item[0][1:]
            arguments = item[1:]
            arguments.append(markup)
            markup = MarkupCommand(command, *arguments)
        p[0] = markup

    def p_markup__simple_markup(self, p):
        "markup : simple_markup"
        p[0] = p[1]

    ### markup_braced_list ###

    def p_markup_braced_list__Chr123__markup_braced_list_body__Chr125(self, p):
        "markup_braced_list : '{' markup_braced_list_body '}'"
        p[0] = p[2]

    ### markup_braced_list_body ###

    def p_markup_braced_list_body__Empty(self, p):
        "markup_braced_list_body :"
        p[0] = []

    def p_markup_braced_list_body__markup_braced_list_body__markup(self, p):
        "markup_braced_list_body : markup_braced_list_body markup"
        p[0] = p[1] + [p[2]]

    def p_markup_braced_list_body__markup_braced_list_body__markup_list(self, p):
        "markup_braced_list_body : markup_braced_list_body markup_list"
        p[0] = p[1] + [p[2]]

    ### markup_command_basic_arguments ###

    def p_markup_command_basic_arguments__EXPECT_MARKUP_LIST__markup_command_list_arguments__markup_list(
        self, p
    ):
        "markup_command_basic_arguments : EXPECT_MARKUP_LIST markup_command_list_arguments markup_list"
        p[0] = p[2] + [p[3]]

    def p_markup_command_basic_arguments__EXPECT_NO_MORE_ARGS(self, p):
        "markup_command_basic_arguments : EXPECT_NO_MORE_ARGS"
        p[0] = []

    def p_markup_command_basic_arguments__EXPECT_SCM__markup_command_list_arguments__embedded_scm_closed(
        self, p
    ):
        "markup_command_basic_arguments : EXPECT_SCM markup_command_list_arguments embedded_scm_closed"
        p[0] = p[2] + [p[3]]

    ### markup_command_list ###

    def p_markup_command_list__MARKUP_LIST_FUNCTION__markup_command_list_arguments(
        self, p
    ):
        "markup_command_list : MARKUP_LIST_FUNCTION markup_command_list_arguments"
        p[0] = MarkupCommand(p[1][1:], *p[2])

    ### markup_command_list_arguments ###

    def p_markup_command_list_arguments__EXPECT_MARKUP__markup_command_list_arguments__markup(
        self, p
    ):
        "markup_command_list_arguments : EXPECT_MARKUP markup_command_list_arguments markup"
        p[0] = p[2] + [p[3]]

    def p_markup_command_list_arguments__markup_command_basic_arguments(self, p):
        "markup_command_list_arguments : markup_command_basic_arguments"
        p[0] = p[1]

    ### markup_composed_list ###

    def p_markup_composed_list__markup_head_1_list__markup_braced_list(self, p):
        "markup_composed_list : markup_head_1_list markup_braced_list"
        markup = p[2]
        for item in reversed(p[1]):
            command = item[0][1:]
            arguments = item[1:]
            arguments.append(markup)
            markup = MarkupCommand(command, *arguments)
        p[0] = markup

    ### markup_head_1_item ###

    def p_markup_head_1_item__MARKUP_FUNCTION__EXPECT_MARKUP__markup_command_list_arguments(
        self, p
    ):
        "markup_head_1_item : MARKUP_FUNCTION EXPECT_MARKUP markup_command_list_arguments"
        p[0] = [p[1]] + p[3]

    ### markup_head_1_list ###

    def p_markup_head_1_list__markup_head_1_item(self, p):
        "markup_head_1_list : markup_head_1_item"
        p[0] = [p[1]]

    def p_markup_head_1_list__markup_head_1_list__markup_head_1_item(self, p):
        "markup_head_1_list : markup_head_1_list markup_head_1_item"
        p[0] = p[1] + [p[2]]

    ### markup_list ###

    def p_markup_list__MARKUPLIST_IDENTIFIER(self, p):
        "markup_list : MARKUPLIST_IDENTIFIER"
        p[0] = p[1]

    def p_markup_list__markup_braced_list(self, p):
        "markup_list : markup_braced_list"
        p[0] = p[1]

    def p_markup_list__markup_command_list(self, p):
        "markup_list : markup_command_list"
        p[0] = p[1]

    def p_markup_list__markup_composed_list(self, p):
        "markup_list : markup_composed_list"
        p[0] = p[1]

    def p_markup_list__markup_scm__MARKUPLIST_IDENTIFIER(self, p):
        "markup_list : markup_scm MARKUPLIST_IDENTIFIER"
        p[0] = SyntaxNode("markup_list", p.__getslice__(1, None))

    ### markup_scm ###

    def p_markup_scm__embedded_scm_bare__BACKUP(self, p):
        "markup_scm : embedded_scm_bare BACKUP"

        p[0] = p[1]

        token = lex.LexToken()
        token.type = "MARKUP_IDENTIFIER"
        token.value = p[1]
        token.lexpos = 0
        token.lineno = 0

        self.client._push_extra_token(self.client._parser.lookahead)
        self.client._push_extra_token(p.slice[2])
        self.client._push_extra_token(token)
        self.client._parser.lookahead = None

    ### markup_top ###

    def p_markup_top__markup_head_1_list__simple_markup(self, p):
        "markup_top : markup_head_1_list simple_markup"
        markup = p[2]
        for item in reversed(p[1]):
            command = item[0][1:]
            arguments = item[1:]
            arguments.append(markup)
            markup = MarkupCommand(command, *arguments)
        p[0] = markup

    def p_markup_top__markup_list(self, p):
        "markup_top : markup_list"
        p[0] = p[1]

    def p_markup_top__simple_markup(self, p):
        "markup_top : simple_markup"
        p[0] = p[1]

    ### mode_changed_music ###

    #    def p_mode_changed_music__mode_changing_head__grouped_music_list(self, p):
    #        'mode_changed_music : mode_changing_head grouped_music_list'
    #        p[0] = SyntaxNode('mode_changed_music', p[1:])

    #    def p_mode_changed_music__mode_changing_head_with_context__optional_context_mod__grouped_music_list(self, p):
    #        'mode_changed_music : mode_changing_head_with_context optional_context_mod grouped_music_list'
    #        p[0] = SyntaxNode('mode_changed_music', p[1:])

    ### mode_changing_head ###

    #    def p_mode_changing_head__CHORDMODE(self, p):
    #        'mode_changing_head : CHORDMODE'
    #        p[0] = SyntaxNode('mode_changing_head', p[1:])

    #    def p_mode_changing_head__DRUMMODE(self, p):
    #        'mode_changing_head : DRUMMODE'
    #        p[0] = SyntaxNode('mode_changing_head', p[1:])

    #    def p_mode_changing_head__FIGUREMODE(self, p):
    #        'mode_changing_head : FIGUREMODE'
    #        p[0] = SyntaxNode('mode_changing_head', p[1:])

    #    def p_mode_changing_head__LYRICMODE(self, p):
    #        'mode_changing_head : LYRICMODE'
    #        p[0] = SyntaxNode('mode_changing_head', p[1:])

    #    def p_mode_changing_head__NOTEMODE(self, p):
    #        'mode_changing_head : NOTEMODE'
    #        p[0] = SyntaxNode('mode_changing_head', p[1:])

    ### mode_changing_head_with_context ###

    #    def p_mode_changing_head_with_context__CHORDS(self, p):
    #        'mode_changing_head_with_context : CHORDS'
    #        p[0] = SyntaxNode('mode_changing_head_with_context', p[1:])

    #    def p_mode_changing_head_with_context__DRUMS(self, p):
    #        'mode_changing_head_with_context : DRUMS'
    #        p[0] = SyntaxNode('mode_changing_head_with_context', p[1:])

    #    def p_mode_changing_head_with_context__FIGURES(self, p):
    #        'mode_changing_head_with_context : FIGURES'
    #        p[0] = SyntaxNode('mode_changing_head_with_context', p[1:])

    #    def p_mode_changing_head_with_context__LYRICS(self, p):
    #        'mode_changing_head_with_context : LYRICS'
    #        p[0] = SyntaxNode('mode_changing_head_with_context', p[1:])

    ### multiplied_duration ###

    def p_multiplied_duration__multiplied_duration__Chr42__FRACTION(self, p):
        "multiplied_duration : multiplied_duration '*' FRACTION"
        if p[1].multiplier is not None:
            p[0] = LilyPondDuration(p[1].duration, p[1].multiplier * p[3])
        else:
            p[0] = LilyPondDuration(
                p[1].duration, fractions.Fraction(p[3].numerator, p[3].denominator)
            )

    def p_multiplied_duration__multiplied_duration__Chr42__bare_unsigned(self, p):
        "multiplied_duration : multiplied_duration '*' bare_unsigned"
        if p[1].multiplier is not None:
            p[0] = LilyPondDuration(p[1].duration, p[1].multiplier * p[3])
        else:
            p[0] = LilyPondDuration(p[1].duration, p[3])

    def p_multiplied_duration__steno_duration(self, p):
        "multiplied_duration : steno_duration"
        p[0] = p[1]

    ### music ###

    def p_music__composite_music(self, p):
        "music : composite_music %prec COMPOSITE"
        p[0] = p[1]

    #    def p_music__lyric_element_music(self, p):
    #        'music : lyric_element_music'
    #        p[0] = p[1]

    def p_music__simple_music(self, p):
        "music : simple_music"
        p[0] = p[1]

    ### music_arg ###

    def p_music_arg__composite_music(self, p):
        "music_arg : composite_music %prec COMPOSITE"
        p[0] = p[1]

    def p_music_arg__simple_music(self, p):
        "music_arg : simple_music"
        p[0] = p[1]

    ### music_bare ###

    def p_music_bare__MUSIC_IDENTIFIER(self, p):
        "music_bare : MUSIC_IDENTIFIER"
        p[0] = p[1]

    def p_music_bare__grouped_music_list(self, p):
        "music_bare : grouped_music_list"
        p[0] = p[1]

    #    def p_music_bare__mode_changed_music(self, p):
    #        'music_bare : mode_changed_music'
    #        p[0] = SyntaxNode('music_bare', p[1:])

    ### music_function_call ###

    def p_music_function_call__MUSIC_FUNCTION__function_arglist(self, p):
        "music_function_call : MUSIC_FUNCTION function_arglist"
        p[0] = self.client._guile(p[1], p[2])

    ### music_function_chord_body ###

    def p_music_function_chord_body__MUSIC_FUNCTION__music_function_chord_body_arglist(
        self, p
    ):
        "music_function_chord_body : MUSIC_FUNCTION music_function_chord_body_arglist"
        p[0] = SyntaxNode("music_function_chord_body", p.__getslice__(1, None))

    ### music_function_chord_body_arglist ###

    def p_music_function_chord_body_arglist__EXPECT_SCM__music_function_chord_body_arglist__embedded_scm_chord_body(
        self, p
    ):
        "music_function_chord_body_arglist : EXPECT_SCM music_function_chord_body_arglist embedded_scm_chord_body"
        p[0] = p[2] + [p[3]]

    def p_music_function_chord_body_arglist__function_arglist_bare(self, p):
        "music_function_chord_body_arglist : function_arglist_bare"
        p[0] = p[1]

    ### music_function_event ###

    def p_music_function_event__MUSIC_FUNCTION__function_arglist_closed(self, p):
        "music_function_event : MUSIC_FUNCTION function_arglist_closed"
        p[0] = SyntaxNode("music_function_event", p.__getslice__(1, None))

    ### music_list ###

    def p_music_list__Empty(self, p):
        "music_list :"
        p[0] = []

    def p_music_list__music_list__embedded_scm(self, p):
        "music_list : music_list embedded_scm"
        p[0] = p[1] + [p[2]]

    def p_music_list__music_list__error(self, p):
        "music_list : music_list error"
        p[0] = p[1] + [p[2]]

    def p_music_list__music_list__music(self, p):
        "music_list : music_list music"
        p[0] = p[1] + [p[2]]

    ### music_property_def ###

    def p_music_property_def__simple_music_property_def(self, p):
        "music_property_def : simple_music_property_def"
        p[0] = SyntaxNode("music_property_def", p.__getslice__(1, None))

    ### new_chord ###

    #    def p_new_chord__steno_tonic_pitch__optional_notemode_duration(self, p):
    #        'new_chord : steno_tonic_pitch optional_notemode_duration'
    #        p[0] = SyntaxNode('new_chord', p[1:])

    #    def p_new_chord__steno_tonic_pitch__optional_notemode_duration__chord_separator__chord_items(self, p):
    #        'new_chord : steno_tonic_pitch optional_notemode_duration chord_separator chord_items'
    #        p[0] = SyntaxNode('new_chord', p[1:])

    ### new_lyrics ###

    #    def p_new_lyrics__ADDLYRICS__composite_music(self, p):
    #        'new_lyrics : ADDLYRICS composite_music'
    #        p[0] = SyntaxNode('new_lyrics', p[1:])

    #    def p_new_lyrics__new_lyrics__ADDLYRICS__composite_music(self, p):
    #        'new_lyrics : new_lyrics ADDLYRICS composite_music'
    #        p[0] = SyntaxNode('new_lyrics', p[1:])

    ### note_chord_element ###

    def p_note_chord_element__chord_body__optional_notemode_duration__post_events(
        self, p
    ):
        "note_chord_element : chord_body optional_notemode_duration post_events"
        chord = _score.Chord([], p[2].duration, tag=self.tag)
        pitches = []
        post_events = []
        for node in p[1]:
            pitches.append(node[0].written_pitch)
            chord.note_heads.append(node[0])
            post_events.extend(node[1])
        post_events.extend(p[3])
        self.client._chord_pitch_orders[chord] = pitches
        if p[2].multiplier is not None:
            multiplier = fractions.Fraction(p[2].multiplier)
            chord.multiplier = _duration.pair(multiplier)
        self.client._process_post_events(chord, post_events)
        p[0] = chord

    ### number_expression ###

    def p_number_expression__number_expression__Chr43__number_term(self, p):
        "number_expression : number_expression '+' number_term"
        p[0] = float(p[1]) + p[3]

    def p_number_expression__number_expression__Chr45__number_term(self, p):
        "number_expression : number_expression '-' number_term"
        p[0] = float(p[1]) - p[3]

    def p_number_expression__number_term(self, p):
        "number_expression : number_term"
        p[0] = p[1]

    ### number_factor ###

    def p_number_factor__Chr45__number_factor(self, p):
        "number_factor : '-' number_factor"
        p[0] = -1 * p[2]

    def p_number_factor__bare_number(self, p):
        "number_factor : bare_number"
        p[0] = p[1]

    ### number_term ###

    def p_number_term__number_factor(self, p):
        "number_term : number_factor"
        p[0] = p[1]

    def p_number_term__number_factor__Chr42__number_factor(self, p):
        "number_term : number_factor '*' number_factor"
        p[0] = float(p[1]) * p[3]

    def p_number_term__number_factor__Chr47__number_factor(self, p):
        "number_term : number_factor '/' number_factor"
        p[0] = float(p[1]) / p[3]

    ### octave_check ###

    def p_octave_check__Chr61(self, p):
        "octave_check : '='"
        p[0] = SyntaxNode("octave_check", p.__getslice__(1, None))

    def p_octave_check__Chr61__sub_quotes(self, p):
        "octave_check : '=' sub_quotes"
        p[0] = SyntaxNode("octave_check", p.__getslice__(1, None))

    def p_octave_check__Chr61__sup_quotes(self, p):
        "octave_check : '=' sup_quotes"
        p[0] = SyntaxNode("octave_check", p.__getslice__(1, None))

    def p_octave_check__Empty(self, p):
        "octave_check :"
        p[0] = SyntaxNode("octave_check", p.__getslice__(1, None))

    ### optional_context_mod ###

    def p_optional_context_mod__Empty(self, p):
        "optional_context_mod :"
        p[0] = []

    def p_optional_context_mod__context_modification(self, p):
        "optional_context_mod : context_modification"
        p[0] = p[1]

    ### optional_id ###

    def p_optional_id__Chr61__simple_string(self, p):
        "optional_id : '=' simple_string"
        p[0] = p[2]

    def p_optional_id__Empty(self, p):
        "optional_id :"
        p[0] = None

    ### optional_notemode_duration ###

    def p_optional_notemode_duration__Empty(self, p):
        "optional_notemode_duration :"
        p[0] = self.client._default_duration

    def p_optional_notemode_duration__multiplied_duration(self, p):
        "optional_notemode_duration : multiplied_duration"
        p[0] = p[1]
        self.client._default_duration = p[1]

    ### optional_rest ###

    def p_optional_rest__Empty(self, p):
        "optional_rest :"
        p[0] = False

    def p_optional_rest__REST(self, p):
        "optional_rest : REST"
        p[0] = True

    ### output_def ###

    def p_output_def__output_def_body__Chr125(self, p):
        "output_def : output_def_body '}'"
        p[0] = p[1]
        self.client._pop_variable_scope()
        self.client._lexer.pop_state()
        self.client._relex_lookahead()

    ### output_def_body ###

    def p_output_def_body__output_def_body__assignment(self, p):
        "output_def_body : output_def_body assignment"
        self.client._assign_variable(p[2][0], p[2][1])
        setattr(p[1], p[2][0], p[2][1].value)
        p[0] = p[1]

    #    def p_output_def_body__output_def_body__context_def_spec_block(self, p):
    #        'output_def_body : output_def_body context_def_spec_block'
    #        p[0] = SyntaxNode('output_def_body', p[1:])

    #    def p_output_def_body__output_def_body__error(self, p):
    #        'output_def_body : output_def_body error'
    #        p[0] = SyntaxNode('output_def_body', p[1:])

    def p_output_def_body__output_def_head_with_mode_switch__Chr123(self, p):
        "output_def_body : output_def_head_with_mode_switch '{'"
        p[0] = p[1]

    def p_output_def_body__output_def_head_with_mode_switch__Chr123__OUTPUT_DEF_IDENTIFIER(
        self, p
    ):
        "output_def_body : output_def_head_with_mode_switch '{' OUTPUT_DEF_IDENTIFIER"
        p[0] = p[2]

    ### output_def_head ###

    def p_output_def_head__LAYOUT(self, p):
        "output_def_head : LAYOUT"
        p[0] = _lilypondfile.Block(name="layout")
        self.client._push_variable_scope()

    def p_output_def_head__MIDI(self, p):
        "output_def_head : MIDI"
        p[0] = _lilypondfile.Block(name="midi")
        self.client._push_variable_scope()

    def p_output_def_head__PAPER(self, p):
        "output_def_head : PAPER"
        p[0] = _lilypondfile.Block(name="paper")
        self.client._push_variable_scope()

    ### output_def_head_with_mode_switch ###

    def p_output_def_head_with_mode_switch__output_def_head(self, p):
        "output_def_head_with_mode_switch : output_def_head"
        p[0] = p[1]
        self.client._lexer.push_state("INITIAL")

    ### paper_block ###

    #    def p_paper_block__output_def(self, p):
    #        'paper_block : output_def'
    #        p[0] = p[1]

    ### pitch ###

    def p_pitch__PITCH_IDENTIFIER(self, p):
        "pitch : PITCH_IDENTIFIER"
        p[0] = p[1]

    def p_pitch__steno_pitch(self, p):
        "pitch : steno_pitch"
        p[0] = p[1]

    ### pitch_also_in_chords ###

    def p_pitch_also_in_chords__pitch(self, p):
        "pitch_also_in_chords : pitch"
        p[0] = p[1]

    def p_pitch_also_in_chords__steno_tonic_pitch(self, p):
        "pitch_also_in_chords : steno_tonic_pitch"
        p[0] = p[1]

    ### post_event ###

    def p_post_event__Chr45__fingering(self, p):
        "post_event : '-' fingering"
        p[0] = None

    def p_post_event__post_event_nofinger(self, p):
        "post_event : post_event_nofinger"
        p[0] = p[1]

    ### post_event_nofinger ###

    def p_post_event_nofinger__Chr94__fingering(self, p):
        "post_event_nofinger : '^' fingering"
        p[0] = None

    def p_post_event_nofinger__Chr95__fingering(self, p):
        "post_event_nofinger : '_' fingering"
        p[0] = None

    def p_post_event_nofinger__EXTENDER(self, p):
        "post_event_nofinger : EXTENDER"
        p[0] = None

    def p_post_event_nofinger__HYPHEN(self, p):
        "post_event_nofinger : HYPHEN"
        p[0] = None

    def p_post_event_nofinger__direction_less_event(self, p):
        "post_event_nofinger : direction_less_event"
        p[0] = p[1]

    def p_post_event_nofinger__script_dir__direction_less_event(self, p):
        "post_event_nofinger : script_dir direction_less_event"
        #        try:
        #            p[2].direction = p[1]
        #            direction = _string.to_tridirectional_lilypond_symbol(p[1])
        #        except AttributeError:
        #            direction = _string.to_tridirectional_lilypond_symbol(p[1])
        #            # assert hasattr(p[2], "_direction")
        #            # p[2]._direction = direction
        # p[0] = p[2]
        direction = _string.to_tridirectional_lilypond_symbol(p[1])
        p[0] = (p[2], direction)

    def p_post_event_nofinger__script_dir__direction_reqd_event(self, p):
        "post_event_nofinger : script_dir direction_reqd_event"
        #        if isinstance(p[2], _indicators.Markup):
        #            direction = _string.to_tridirectional_ordinal_constant(p[1])
        #            p[2].direction = direction
        #        else:
        #            try:
        #                p[2].direction = p[1]
        #            except AttributeError:
        #                direction = _string.to_tridirectional_ordinal_constant(p[1])
        #                assert hasattr(p[2], "_direction")
        #                p[2]._direction = direction
        #        p[0] = p[2]
        direction = _string.to_tridirectional_ordinal_constant(p[1])
        p[0] = (p[2], direction)

    def p_post_event_nofinger__script_dir__music_function_event(self, p):
        "post_event_nofinger : script_dir music_function_event"
        p[0] = p[2]

    def p_post_event_nofinger__string_number_event(self, p):
        "post_event_nofinger : string_number_event"
        p[0] = None

    ### post_events ###

    def p_post_events__Empty(self, p):
        "post_events :"
        p[0] = []

    def p_post_events__post_events__post_event(self, p):
        "post_events : post_events post_event"
        p[0] = p[1] + [p[2]]

    ### property_operation ###

    def p_property_operation__OVERRIDE__simple_string__property_path__Chr61__scalar(
        self, p
    ):
        "property_operation : OVERRIDE simple_string property_path '=' scalar"
        p[0] = LilyPondEvent(
            "PropertyOperation",
            keyword="override",
            context=p[2],
            property=p[3],
            value=p[5],
        )

    def p_property_operation__REVERT__simple_string__embedded_scm(self, p):
        "property_operation : REVERT simple_string embedded_scm"
        p[0] = LilyPondEvent(
            "PropertyOperation", keyword="revert", context=p[2], property=p[3]
        )

    def p_property_operation__STRING__Chr61__scalar(self, p):
        "property_operation : STRING '=' scalar"
        p[0] = LilyPondEvent(
            "PropertyOperation", keyword="set", property=p[1], value=p[2]
        )

    def p_property_operation__UNSET__simple_string(self, p):
        "property_operation : UNSET simple_string"
        p[0] = LilyPondEvent("PropertyOperation", keyword="unset", property=p[2])

    ### property_path ###

    def p_property_path__property_path_revved(self, p):
        "property_path : property_path_revved"
        p[0] = p[1]

    ### property_path_revved ###

    def p_property_path_revved__embedded_scm_closed(self, p):
        "property_path_revved : embedded_scm_closed"
        p[0] = [p[1]]

    def p_property_path_revved__property_path_revved__embedded_scm_closed(self, p):
        "property_path_revved : property_path_revved embedded_scm_closed"
        p[0] = p[1] + [p[2]]

    ### questions ###

    def p_questions__Empty(self, p):
        "questions :"
        p[0] = 0

    def p_questions__questions__Chr63(self, p):
        "questions : questions '?'"
        p[0] = p[1] + 1

    ### re_rhythmed_music ###

    #    def p_re_rhythmed_music__LYRICSTO__simple_string__music(self, p):
    #        're_rhythmed_music : LYRICSTO simple_string music'
    #        p[0] = SyntaxNode('re_rhythmed_music', p[1:])

    #    def p_re_rhythmed_music__composite_music__new_lyrics(self, p):
    #        're_rhythmed_music : composite_music new_lyrics %prec COMPOSITE'
    #        p[0] = SyntaxNode('re_rhythmed_music', p[1:])

    ### repeated_music ###

    #    def p_repeated_music__REPEAT__simple_string__unsigned_number__music(self, p):
    #        'repeated_music : REPEAT simple_string unsigned_number music'
    #        p[0] = SyntaxNode('repeated_music', p[1:])

    #    def p_repeated_music__REPEAT__simple_string__unsigned_number__music__ALTERNATIVE__braced_music_list(self, p):
    #        'repeated_music : REPEAT simple_string unsigned_number music ALTERNATIVE braced_music_list'
    #        p[0] = SyntaxNode('repeated_music', p[1:])

    ### scalar ###

    def p_scalar__bare_number(self, p):
        "scalar : bare_number"
        p[0] = p[1]

    def p_scalar__embedded_scm_arg(self, p):
        "scalar : embedded_scm_arg"
        p[0] = p[1]

    #    def p_scalar__lyric_element(self, p):
    #        'scalar : lyric_element'
    #        p[0] = p[1]

    ### scalar_closed ###

    def p_scalar_closed__bare_number(self, p):
        "scalar_closed : bare_number"
        p[0] = p[1]

    def p_scalar_closed__embedded_scm_arg_closed(self, p):
        "scalar_closed : embedded_scm_arg_closed"
        p[0] = p[1]

    #    def p_scalar_closed__lyric_element(self, p):
    #        'scalar_closed : lyric_element'
    #        p[0] = p[1]

    ### scm_function_call ###

    def p_scm_function_call__SCM_FUNCTION__function_arglist(self, p):
        "scm_function_call : SCM_FUNCTION function_arglist"
        p[0] = self.client._guile(p[1], p[2])

    ### scm_function_call_closed ###

    def p_scm_function_call_closed__SCM_FUNCTION__function_arglist_closed(self, p):
        "scm_function_call_closed : SCM_FUNCTION function_arglist_closed %prec FUNCTION_ARGLIST"
        p[0] = self.client._guile(p[1], p[2])

    ### score_block ###

    def p_score_block__SCORE__Chr123__score_body__Chr125(self, p):
        "score_block : SCORE '{' score_body '}'"
        score_block = _lilypondfile.Block(name="score")
        score_block.items.extend(p[3])
        p[0] = score_block

    ### score_body ###

    def p_score_body__SCORE_IDENTIFIER(self, p):
        "score_body : SCORE_IDENTIFIER"
        p[0] = [p[1]]

    def p_score_body__music(self, p):
        "score_body : music"
        p[0] = [p[1]]

    #    def p_score_body__score_body__error(self, p):
    #        'score_body : score_body error'
    #        p[0] = SyntaxNode('score_body', p[1:])

    def p_score_body__score_body__lilypond_header(self, p):
        "score_body : score_body lilypond_header"
        p[0] = p[1] + [p[2]]

    def p_score_body__score_body__output_def(self, p):
        "score_body : score_body output_def"
        p[0] = p[1] + [p[2]]

    ### script_abbreviation ###

    def p_script_abbreviation__ANGLE_CLOSE(self, p):
        "script_abbreviation : ANGLE_CLOSE"
        kind = self.client._current_module["dashLarger"]["articulation-type"]
        p[0] = _indicators.Articulation(kind)

    def p_script_abbreviation__Chr33(self, p):
        "script_abbreviation : '!'"
        # kind = self.client._current_module["dashBar"]["articulation-type"]
        kind = self.client._current_module["dashBang"]["articulation-type"]
        p[0] = _indicators.Articulation(kind)

    def p_script_abbreviation__Chr43(self, p):
        "script_abbreviation : '+'"
        kind = self.client._current_module["dashPlus"]["articulation-type"]
        p[0] = _indicators.Articulation(kind)

    def p_script_abbreviation__Chr45(self, p):
        "script_abbreviation : '-'"
        kind = self.client._current_module["dashDash"]["articulation-type"]
        p[0] = _indicators.Articulation(kind)

    def p_script_abbreviation__Chr46(self, p):
        "script_abbreviation : '.'"
        kind = self.client._current_module["dashDot"]["articulation-type"]
        p[0] = _indicators.Articulation(kind)

    def p_script_abbreviation__Chr94(self, p):
        "script_abbreviation : '^'"
        kind = self.client._current_module["dashHat"]["articulation-type"]
        p[0] = _indicators.Articulation(kind)

    def p_script_abbreviation__Chr95(self, p):
        "script_abbreviation : '_'"
        kind = self.client._current_module["dashUnderscore"]["articulation-type"]
        p[0] = _indicators.Articulation(kind)

    ### script_dir ###

    def p_script_dir__Chr45(self, p):
        "script_dir : '-'"
        p[0] = p[1]

    def p_script_dir__Chr94(self, p):
        "script_dir : '^'"
        p[0] = p[1]

    def p_script_dir__Chr95(self, p):
        "script_dir : '_'"
        p[0] = p[1]

    ### sequential_music ###

    def p_sequential_music__SEQUENTIAL__braced_music_list(self, p):
        "sequential_music : SEQUENTIAL braced_music_list"
        p[0] = self.client._construct_sequential_music(p[2])

    def p_sequential_music__braced_music_list(self, p):
        "sequential_music : braced_music_list"
        p[0] = self.client._construct_sequential_music(p[1])

    ### simple_chord_elements ###

    #    def p_simple_chord_elements__figure_spec__optional_notemode_duration(self, p):
    #        'simple_chord_elements : figure_spec optional_notemode_duration'
    #        p[0] = SyntaxNode('simple_chord_elements', p[1:])

    #    def p_simple_chord_elements__new_chord(self, p):
    #        'simple_chord_elements : new_chord'
    #        p[0] = SyntaxNode('simple_chord_elements', p[1:])

    def p_simple_chord_elements__simple_element(self, p):
        "simple_chord_elements : simple_element"
        p[0] = p[1]

    ### simple_element ###

    #    def p_simple_element__DRUM_PITCH__optional_notemode_duration(self, p):
    #        'simple_element : DRUM_PITCH optional_notemode_duration'
    #        message = 'drum pitches not supported.'
    #        raise Exception(message)

    def p_simple_element__RESTNAME__optional_notemode_duration(self, p):
        "simple_element : RESTNAME optional_notemode_duration"
        if p[1] == "r":
            rest = _score.Rest(p[2].duration, tag=self.tag)
        else:
            rest = _score.Skip(p[2].duration, tag=self.tag)
        if p[2].multiplier is not None:
            multiplier = fractions.Fraction(p[2].multiplier)
            rest.multiplier = _duration.pair(multiplier)
        p[0] = rest

    def p_simple_element__pitch__exclamations__questions__octave_check__optional_notemode_duration__optional_rest(
        self, p
    ):
        "simple_element : pitch exclamations questions octave_check optional_notemode_duration optional_rest"
        if not p[6]:
            leaf = _score.Note(p[1], p[5].duration, tag=self.tag)
            leaf.note_head.is_forced = bool(p[2])
            leaf.note_head.is_cautionary = bool(p[3])
        else:
            leaf = _score.Rest(p[5].duration, tag=self.tag)
        if p[5].multiplier is not None:
            multiplier = fractions.Fraction(p[5].multiplier)
            leaf.multiplier = _duration.pair(multiplier)
        # TODO: handle exclamations, questions, octave_check
        p[0] = leaf

    ### simple_markup ###

    #    def p_simple_markup__LYRIC_MARKUP_IDENTIFIER(self, p):
    #        'simple_markup : LYRIC_MARKUP_IDENTIFIER'
    #        p[0] = SyntaxNode('simple_markup', p[1:])

    def p_simple_markup__MARKUP_FUNCTION__markup_command_basic_arguments(self, p):
        "simple_markup : MARKUP_FUNCTION markup_command_basic_arguments"
        command = p[1][1:]
        arguments = p[2]
        p[0] = MarkupCommand(command, *arguments)

    def p_simple_markup__MARKUP_IDENTIFIER(self, p):
        "simple_markup : MARKUP_IDENTIFIER"
        p[0] = p[1]

    def p_simple_markup__SCORE__Chr123__score_body__Chr125(self, p):
        "simple_markup : SCORE '{' score_body '}'"
        p[0] = SyntaxNode("simple_markup", p.__getslice__(1, None))

    def p_simple_markup__STRING(self, p):
        "simple_markup : STRING"
        p[0] = p[1]

    def p_simple_markup__STRING_IDENTIFIER(self, p):
        "simple_markup : STRING_IDENTIFIER"
        p[0] = p[1]

    ### simple_music ###

    def p_simple_music__context_change(self, p):
        "simple_music : context_change"
        p[0] = p[1]

    def p_simple_music__event_chord(self, p):
        "simple_music : event_chord"
        p[0] = p[1]

    def p_simple_music__music_property_def(self, p):
        "simple_music : music_property_def"
        p[0] = p[1]

    ### simple_music_property_def ###

    def p_simple_music_property_def__OVERRIDE__context_prop_spec__property_path__Chr61__scalar(
        self, p
    ):
        "simple_music_property_def : OVERRIDE context_prop_spec property_path '=' scalar"
        p[0] = LilyPondEvent(
            "PropertyOperation",
            keyword="override",
            context=p[2],
            property=p[3],
            value=p[5],
        )

    def p_simple_music_property_def__REVERT__context_prop_spec__embedded_scm(self, p):
        "simple_music_property_def : REVERT context_prop_spec embedded_scm"
        p[0] = SyntaxNode("simple_music_property_def", p.__getslice__(1, None))

    def p_simple_music_property_def__SET__context_prop_spec__Chr61__scalar(self, p):
        "simple_music_property_def : SET context_prop_spec '=' scalar"
        p[0] = SyntaxNode("simple_music_property_def", p.__getslice__(1, None))

    def p_simple_music_property_def__UNSET__context_prop_spec(self, p):
        "simple_music_property_def : UNSET context_prop_spec"
        p[0] = SyntaxNode("simple_music_property_def", p.__getslice__(1, None))

    ### simple_string ###

    #    def p_simple_string__LYRICS_STRING(self, p):
    #        'simple_string : LYRICS_STRING'
    #        p[0] = p[1]

    def p_simple_string__STRING(self, p):
        "simple_string : STRING"
        p[0] = p[1]

    def p_simple_string__STRING_IDENTIFIER(self, p):
        "simple_string : STRING_IDENTIFIER"
        p[0] = p[1]

    ### simultaneous_music ###

    def p_simultaneous_music__DOUBLE_ANGLE_OPEN__music_list__DOUBLE_ANGLE_CLOSE(
        self, p
    ):
        "simultaneous_music : DOUBLE_ANGLE_OPEN music_list DOUBLE_ANGLE_CLOSE"
        p[0] = self.client._construct_simultaneous_music(p[2])

    def p_simultaneous_music__SIMULTANEOUS__braced_music_list(self, p):
        "simultaneous_music : SIMULTANEOUS braced_music_list"
        p[0] = self.client._construct_simultaneous_music(p[2])

    ### steno_duration ###

    def p_steno_duration__DURATION_IDENTIFIER__dots(self, p):
        "steno_duration : DURATION_IDENTIFIER dots"
        dots = p[2].value
        duration = p[1].duration
        multiplier = p[1].multiplier
        if dots:
            duration = duration.lilypond_duration_string
            duration += "." * dots
            duration = _duration.Duration.from_lilypond_duration_string(duration)
        p[0] = LilyPondDuration(duration, multiplier)

    def p_steno_duration__bare_unsigned__dots(self, p):
        "steno_duration : bare_unsigned dots"
        assert _duration.Duration.is_token(p[1])
        dots = p[2].value
        token = str(p[1]) + "." * dots
        duration = _duration.Duration.from_lilypond_duration_string(token)
        p[0] = LilyPondDuration(duration, None)

    ### steno_pitch ###

    def p_steno_pitch__NOTENAME_PITCH(self, p):
        "steno_pitch : NOTENAME_PITCH"
        if isinstance(p[1], _pitch.NamedPitchClass):
            p[0] = _pitch.NamedPitch(p[1].name)
        elif p[1] in _lyconst.drums:
            p[0] = p[1]

    def p_steno_pitch__NOTENAME_PITCH__sub_quotes(self, p):
        "steno_pitch : NOTENAME_PITCH sub_quotes"
        p[0] = _pitch.NamedPitch(p[1].name + "," * p[2])

    def p_steno_pitch__NOTENAME_PITCH__sup_quotes(self, p):
        "steno_pitch : NOTENAME_PITCH sup_quotes"
        p[0] = _pitch.NamedPitch(p[1].name + "'" * p[2])

    ### steno_tonic_pitch ###

    def p_steno_tonic_pitch__TONICNAME_PITCH(self, p):
        "steno_tonic_pitch : TONICNAME_PITCH"
        p[0] = SyntaxNode("steno_tonic_pitch", p.__getslice__(1, None))

    def p_steno_tonic_pitch__TONICNAME_PITCH__sub_quotes(self, p):
        "steno_tonic_pitch : TONICNAME_PITCH sub_quotes"
        p[0] = SyntaxNode("steno_tonic_pitch", p.__getslice__(1, None))

    def p_steno_tonic_pitch__TONICNAME_PITCH__sup_quotes(self, p):
        "steno_tonic_pitch : TONICNAME_PITCH sup_quotes"
        p[0] = SyntaxNode("steno_tonic_pitch", p.__getslice__(1, None))

    ### step_number ###

    #    def p_step_number__bare_unsigned(self, p):
    #        'step_number : bare_unsigned'
    #        p[0] = SyntaxNode('step_number', p[1:])

    #    def p_step_number__bare_unsigned__CHORD_MINUS(self, p):
    #        'step_number : bare_unsigned CHORD_MINUS'
    #        p[0] = SyntaxNode('step_number', p[1:])

    #    def p_step_number__bare_unsigned__Chr43(self, p):
    #        "step_number : bare_unsigned '+'"
    #        p[0] = SyntaxNode('step_number', p[1:])

    ### step_numbers ###

    #    def p_step_numbers__step_number(self, p):
    #        'step_numbers : step_number'
    #        p[0] = SyntaxNode('step_numbers', p[1:])

    #    def p_step_numbers__step_numbers__Chr46__step_number(self, p):
    #        "step_numbers : step_numbers '.' step_number"
    #        p[0] = SyntaxNode('step_numbers', p[1:])

    ### string ###

    def p_string__STRING(self, p):
        "string : STRING"
        p[0] = p[1]

    def p_string__STRING_IDENTIFIER(self, p):
        "string : STRING_IDENTIFIER"
        p[0] = p[1]

    def p_string__string__Chr43__string(self, p):
        "string : string '+' string"
        p[0] = p[1] + p[3]

    ### string_number_event ###

    def p_string_number_event__E_UNSIGNED(self, p):
        "string_number_event : E_UNSIGNED"
        p[0] = SyntaxNode("string_number_event", p[1:])

    ### sub_quotes ###

    def p_sub_quotes__Chr44(self, p):
        "sub_quotes : ','"
        p[0] = 1

    def p_sub_quotes__sub_quotes__Chr44(self, p):
        "sub_quotes : sub_quotes ','"
        p[0] = p[1] + 1

    ### sup_quotes ###

    def p_sup_quotes__Chr39(self, p):
        "sup_quotes : '\\''"
        p[0] = 1

    def p_sup_quotes__sup_quotes__Chr39(self, p):
        "sup_quotes : sup_quotes '\\''"
        p[0] = p[1] + 1

    ### tempo_event ###

    def p_tempo_event__TEMPO__scalar(self, p):
        "tempo_event : TEMPO scalar"
        if " " in p[2]:
            string = f'"{p[2]}"'
        else:
            string = p[2]
        p[0] = _indicators.MetronomeMark(textual_indication=string)

    def p_tempo_event__TEMPO__scalar_closed__steno_duration__Chr61__tempo_range(
        self, p
    ):
        "tempo_event : TEMPO scalar_closed steno_duration '=' tempo_range"
        if " " in p[2]:
            string = f'"{p[2]}"'
        else:
            string = p[2]
        p[0] = _indicators.MetronomeMark(
            reference_duration=p[3].duration,
            units_per_minute=p[5],
            textual_indication=string,
        )

    def p_tempo_event__TEMPO__steno_duration__Chr61__tempo_range(self, p):
        "tempo_event : TEMPO steno_duration '=' tempo_range"
        p[0] = _indicators.MetronomeMark(
            reference_duration=p[2].duration, units_per_minute=p[4]
        )

    ### tempo_range ###

    def p_tempo_range__bare_unsigned(self, p):
        "tempo_range : bare_unsigned"
        p[0] = p[1]

    def p_tempo_range__bare_unsigned__Chr45__bare_unsigned(self, p):
        "tempo_range : bare_unsigned '-' bare_unsigned"
        p[0] = (p[1], p[3])

    ### toplevel_expression ###

    #    def p_toplevel_expression__book_block(self, p):
    #        'toplevel_expression : book_block'
    #        p[0] = p[1]

    #    def p_toplevel_expression__bookpart_block(self, p):
    #        'toplevel_expression : bookpart_block'
    #        p[0] = p[1]

    def p_toplevel_expression__composite_music(self, p):
        "toplevel_expression : composite_music"
        p[0] = p[1]

    def p_toplevel_expression__full_markup(self, p):
        "toplevel_expression : full_markup"
        p[0] = p[1]

    def p_toplevel_expression__full_markup_list(self, p):
        "toplevel_expression : full_markup_list"
        p[0] = p[1]

    def p_toplevel_expression__lilypond_header(self, p):
        "toplevel_expression : lilypond_header"
        p[0] = p[1]

    def p_toplevel_expression__output_def(self, p):
        "toplevel_expression : output_def"
        p[0] = p[1]

    def p_toplevel_expression__score_block(self, p):
        "toplevel_expression : score_block"
        p[0] = p[1]

    ### tremolo_type ###

    def p_tremolo_type__Chr58(self, p):
        "tremolo_type : ':'"
        p[0] = None

    def p_tremolo_type__Chr58__bare_unsigned(self, p):
        "tremolo_type : ':' bare_unsigned"
        p[0] = _indicators.StemTremolo(p[2])

    ### unsigned_number ###

    #    def p_unsigned_number__NUMBER_IDENTIFIER(self, p):
    #        'unsigned_number : NUMBER_IDENTIFIER'
    #        p[0] = p[1]

    #    def p_unsigned_number__UNSIGNED(self, p):
    #        'unsigned_number : UNSIGNED'
    #        p[0] = p[1]

    ### PLY error ###

    def p_error(self, p):
        # print p
        raise _exceptions.LilyPondParserError(p)


class SequentialMusic(Music):
    """
    Abjad model of the LilyPond AST sequential music node.
    """

    __slots__ = ()

    def construct(self) -> _score.Container:
        """
        Constructs sequential music.
        """
        container = _score.Container()
        for x in self.music:
            if isinstance(x, _score.Component):
                container.append(x)
            elif isinstance(x, type(self)):
                container.extend(x.construct())
        return container


class SimultaneousMusic(Music):
    """
    Abjad model of the LilyPond AST simultaneous music node.
    """

    __slots__ = ()


class SyntaxNode:
    """
    A node in an abstract syntax tree (AST).

    Not composer-safe.

    Used internally by LilyPondParser.
    """

    __slots__ = ("type", "value")

    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Returns item or slice.
        """
        if isinstance(self.value, list | tuple):
            return self.value.__getitem__(argument)
        raise Exception(f"can not get: {argument!r}.")

    def __len__(self):
        """
        Gets length.
        """
        if isinstance(self.value, list | tuple):
            return len(self.value)
        raise Exception("value must be list or tuple.")

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.type}, {type(self.value)})"

    def _format(self, obj, indent=0):
        space = ".  " * indent
        result = []
        if isinstance(obj, type(self)):
            if isinstance(obj.value, list | tuple):
                result.append(f"{space}<{obj.type}>: [")
                for x in obj.value:
                    result.extend(self._format(x, indent + 1))
                result[-1] += " ]"
            else:
                result.append(f"{space}<{obj.type}>: {obj.value!r}")
        elif isinstance(obj, (list, tuple)):
            result.append(f"{space}[")
            for x in obj:
                result.extend(self._format(x, indent + 1))
            result[-1] += " ]"
        else:
            result.append(f"{space}{obj!r}")
        return result
