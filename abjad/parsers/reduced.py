from .. import _iterlib
from .. import bind as _bind
from .. import duration as _duration
from .. import enums as _enums
from .. import exceptions as _exceptions
from .. import indicators as _indicators
from .. import pitch as _pitch
from .. import score as _score
from .. import select as _select
from .base import Parser


class ReducedLyParser(Parser):
    r"""
    Parses the "reduced-ly" syntax, a modified subset of LilyPond syntax.

    ..  container:: example

        >>> from abjad.parsers.reduced import ReducedLyParser
        >>> parser = ReducedLyParser()

        Understands LilyPond-like representation of notes, chords and rests:

        >>> string = "c'4 r8. <b d' fs'>16"
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                r8.
                <b d' fs'>16
            }

        Also parses bare duration as notes on middle-C, and negative bare
        durations as rests:

        >>> string = '4 -8 16. -32'
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                r8
                c'16.
                r32
            }

    ..  container:: example

        Note that the leaf syntax is greedy, and therefore duration specifiers
        following pitch specifiers will be treated as part of the same
        expression. The following produces 2 leaves, rather than 3:

        >>> string = "4 d' 4"
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                d'4
            }

        Understands LilyPond-like default durations:

        >>> string = "c'4 d' e' f'"
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                d'4
                e'4
                f'4
            }

    Also understands various types of container specifications.

    ..  container:: example

        Can create arbitrarily nested tuplets:

        >>> string = "2/3 { 4 4 3/5 { 8 8 8 } }"
        >>> tuplet = parser(string)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak edge-height #'(0.7 . 0)
            \tuplet 3/2
            {
                c'4
                c'4
                \tweak text #tuplet-number::calc-fraction-text
                \tweak edge-height #'(0.7 . 0)
                \tuplet 5/3
                {
                    c'8
                    c'8
                    c'8
                }
            }

    ..  container:: example

        Can create measures too:

        >>> string = '| 4/4 4 4 4 4 || 3/8 8 8 8 |'
        >>> container = parser(string)
        >>> staff = abjad.Staff([container])
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                {
                    {
                        \time 4/4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                    {
                        \time 3/8
                        c'8
                        c'8
                        c'8
                    }
                }
            }

    ..  container:: example

        Finally, understands ties, slurs and beams:

        >>> string = 'c16 [ ( d ~ d ) f ]'
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c16
                [
                (
                d16
                ~
                d16
                )
                f16
                ]
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_default_duration", "_toplevel_component_count")

    ### INITIALIZER ###

    def __init__(self, debug=False):
        self._default_duration = _duration.Duration((1, 4))
        self._toplevel_component_count = None
        Parser.__init__(self, debug=debug)

    ### LEX SETUP ###

    tokens = (
        "APOSTROPHE",
        "BRACE_L",
        "BRACE_R",
        "BRACKET_L",
        "BRACKET_R",
        "CARAT_L",
        "CARAT_R",
        "COMMA",
        "DOT",
        "FRACTION",
        "INTEGER_N",
        "INTEGER_P",
        "PAREN_L",
        "PAREN_R",
        "PIPE",
        "PITCHNAME",
        "RESTNAME",
        "TILDE",
    )

    t_APOSTROPHE = "'"
    t_BRACE_L = "{"
    t_BRACE_R = "}"
    t_BRACKET_L = r"\["
    t_BRACKET_R = r"\]"
    t_CARAT_L = r"\<"
    t_CARAT_R = r"\>"
    t_COMMA = ","
    t_DOT = r"\."
    t_PAREN_L = r"\("
    t_PAREN_R = r"\)"
    t_PIPE = r"\|"
    t_RESTNAME = "r"
    t_TILDE = "~"

    t_ignore = " \t\r"

    ### YACC SETUP ###

    start = "start"

    ### LEX METHODS ###

    def t_FRACTION(self, t):
        r"([1-9]\d*/[1-9]\d*)"
        parts = t.value.split("/")
        t.value = int(parts[0]), int(parts[1])
        return t

    def t_INTEGER_N(self, t):
        r"(-[1-9]\d*)"
        t.value = int(t.value)
        return t

    def t_INTEGER_P(self, t):
        r"([1-9]\d*)"
        t.value = int(t.value)
        return t

    def t_PITCHNAME(self, t):
        r"[a-g](ff|ss|f|s|tqf|tqs|qs|qf)?"
        t.value = _pitch.NamedPitchClass(t.value)
        return t

    def t_error(self, t):
        print(("Illegal character '%s'" % t.value[0]))
        t.lexer.skip(1)

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    ### YACC METHODS ###

    def p_apostrophes__APOSTROPHE(self, p):
        """
        apostrophes : APOSTROPHE
        """
        p[0] = 1

    def p_apostrophes__apostrophes__APOSTROPHE(self, p):
        """
        apostrophes : apostrophes APOSTROPHE
        """
        p[0] = p[1] + 1

    def p_beam__BRACKET_L(self, p):
        """
        beam : BRACKET_L
        """
        p[0] = (_indicators.StartBeam, _enums.LEFT)

    def p_beam__BRACKET_R(self, p):
        """
        beam : BRACKET_R
        """
        p[0] = (_indicators.StopBeam, _enums.RIGHT)

    def p_chord_body__chord_pitches(self, p):
        """
        chord_body : chord_pitches
        """
        p[0] = _score.Chord(p[1], self._default_duration)

    def p_chord_body__chord_pitches__positive_leaf_duration(self, p):
        """
        chord_body : chord_pitches positive_leaf_duration
        """
        p[0] = _score.Chord(p[1], p[2])

    def p_chord_pitches__CARAT_L__pitches__CARAT_R(self, p):
        """
        chord_pitches : CARAT_L pitches CARAT_R
        """
        p[0] = p[2]

    def p_commas__COMMA(self, p):
        """
        commas : COMMA
        """
        p[0] = 1

    def p_commas__commas__commas(self, p):
        """
        commas : commas COMMA
        """
        p[0] = p[1] + 1

    def p_component__container(self, p):
        """
        component : container
        """
        p[0] = p[1]

    def p_component__fixed_duration_container(self, p):
        """
        component : fixed_duration_container
        """
        p[0] = p[1]

    def p_component__leaf(self, p):
        """
        component : leaf
        """
        p[0] = p[1]

    def p_component__tuplet(self, p):
        """
        component : tuplet
        """
        p[0] = p[1]

    def p_component_list__EMPTY(self, p):
        """
        component_list :
        """
        p[0] = []

    def p_component_list__component_list__component(self, p):
        """
        component_list : component_list component
        """
        p[0] = p[1] + [p[2]]

    def p_container__BRACE_L__component_list__BRACE_R(self, p):
        r"""container : BRACE_L component_list BRACE_R"""
        p[0] = _score.Container()
        for component in p[2]:
            p[0].append(component)

    def p_dots__EMPTY(self, p):
        """
        dots :
        """
        p[0] = 0

    def p_dots__dots__DOT(self, p):
        """
        dots : dots DOT
        """
        p[0] = p[1] + 1

    def p_error(self, p):
        if p:
            print(("Syntax error at '%s'" % p.value))
        else:
            print("Syntax error at EOF")

    def p_fixed_duration_container__BRACE_L__FRACTION__BRACE_R(self, p):
        """
        fixed_duration_container : BRACE_L FRACTION BRACE_R
        """
        raise Exception("fixed-duration containers no longer supported.")

    def p_leaf__leaf_body__post_events(self, p):
        """
        leaf : leaf_body post_events
        """
        p[0] = p[1]
        if p[2]:
            annotation = {"post events": p[2]}
            _bind._unsafe_attach(annotation, p[0])

    def p_leaf_body__chord_body(self, p):
        """
        leaf_body : chord_body
        """
        p[0] = p[1]

    def p_leaf_body__note_body(self, p):
        """
        leaf_body : note_body
        """
        p[0] = p[1]

    def p_leaf_body__rest_body(self, p):
        """
        leaf_body : rest_body
        """
        p[0] = p[1]

    def p_measure__PIPE__FRACTION__component_list__PIPE(self, p):
        """
        measure : PIPE FRACTION component_list PIPE
        """
        measure = _score.Container()
        for x in p[3]:
            measure.append(x)
        leaf = _iterlib._get_leaf(measure, 0)
        time_signature = _indicators.TimeSignature(p[2])
        try:
            _bind._unsafe_attach(time_signature, leaf)
        except _exceptions.MissingContextError:
            score = _score.Score([measure])
            _bind._unsafe_attach(time_signature, leaf)
            score[:] = []
        p[0] = measure

    def p_negative_leaf_duration__INTEGER_N__dots(self, p):
        """
        negative_leaf_duration : INTEGER_N dots
        """
        duration_log = p[1]
        dots = "." * p[2]
        string = f"{abs(duration_log)}{dots}"
        duration = _duration.Duration.from_lilypond_duration_string(string)
        self._default_duration = duration
        p[0] = duration

    def p_note_body__pitch(self, p):
        """
        note_body : pitch
        """
        p[0] = _score.Note(p[1], self._default_duration)

    def p_note_body__pitch__positive_leaf_duration(self, p):
        """
        note_body : pitch positive_leaf_duration
        """
        p[0] = _score.Note(p[1], p[2])

    def p_note_body__positive_leaf_duration(self, p):
        """
        note_body : positive_leaf_duration
        """
        p[0] = _score.Note(0, p[1])

    def p_pitch__PITCHNAME(self, p):
        """
        pitch : PITCHNAME
        """
        p[0] = _pitch.NamedPitch(p[1].name)

    def p_pitch__PITCHNAME__apostrophes(self, p):
        """
        pitch : PITCHNAME apostrophes
        """
        p[0] = _pitch.NamedPitch(p[1].name + "'" * p[2])

    def p_pitch__PITCHNAME__commas(self, p):
        """
        pitch : PITCHNAME commas
        """
        p[0] = _pitch.NamedPitch(p[1].name + "," * p[2])

    def p_pitches__pitch(self, p):
        """
        pitches : pitch
        """
        p[0] = [p[1]]

    def p_pitches__pitches__pitch(self, p):
        """
        pitches : pitches pitch
        """
        p[0] = p[1] + [p[2]]

    def p_positive_leaf_duration__INTEGER_P__dots(self, p):
        """
        positive_leaf_duration : INTEGER_P dots
        """
        duration_log = p[1]
        dots = "." * p[2]
        duration = _duration.Duration.from_lilypond_duration_string(
            f"{abs(duration_log)}{dots}"
        )
        self._default_duration = duration
        p[0] = duration

    def p_post_event__beam(self, p):
        """
        post_event : beam
        """
        p[0] = p[1]

    def p_post_event__slur(self, p):
        """
        post_event : slur
        """
        p[0] = p[1]

    def p_post_event__tie(self, p):
        """
        post_event : tie
        """
        p[0] = p[1]

    def p_post_events__EMPTY(self, p):
        """
        post_events :
        """
        p[0] = {}

    def p_post_events__post_events__post_event(self, p):
        """
        post_events : post_events post_event
        """
        kind, direction = p[2]
        if kind in p[1]:
            p[1][kind].append(direction)
        else:
            p[1][kind] = [direction]
        p[0] = p[1]

    def p_rest_body__RESTNAME(self, p):
        """
        rest_body : RESTNAME
        """
        p[0] = _score.Rest(self._default_duration)

    def p_rest_body__RESTNAME__positive_leaf_duration(self, p):
        """
        rest_body : RESTNAME positive_leaf_duration
        """
        p[0] = _score.Rest(p[2])

    def p_rest_body__negative_leaf_duration(self, p):
        """
        rest_body : negative_leaf_duration
        """
        p[0] = _score.Rest(p[1])

    def p_slur__PAREN_L(self, p):
        """
        slur : PAREN_L
        """
        p[0] = (_indicators.StartSlur, _enums.LEFT)

    def p_slur__PAREN_R(self, p):
        """
        slur : PAREN_R
        """
        p[0] = (_indicators.StopSlur, _enums.RIGHT)

    def p_start__EMPTY(self, p):
        """
        start :
        """
        self._toplevel_component_count = 0
        p[0] = []

    def p_start__start__component(self, p):
        """
        start : start component
        """
        self._toplevel_component_count += 1
        p[0] = p[1] + [p[2]]

    def p_start__start__measure(self, p):
        """
        start : start measure
        """
        self._toplevel_component_count += 1
        p[0] = p[1] + [p[2]]

    def p_tie__TILDE(self, p):
        """
        tie : TILDE
        """
        p[0] = (_indicators.Tie, _enums.LEFT)

    def p_tuplet__FRACTION__container(self, p):
        """
        tuplet : FRACTION container
        """
        assert isinstance(p[2], _score.Container)
        leaves = p[2][:]
        p[2][:] = []
        p[0] = _score.Tuplet(p[1], leaves)

    ### PRIVATE METHODS ###

    def _attach_indicators(self, leaves):
        for leaf in leaves:
            span_events = self._get_span_events(leaf)
            for current_class, directions in span_events.items():
                if current_class in (
                    _indicators.StartSlur,
                    _indicators.StopSlur,
                ):
                    indicator = current_class()
                    _bind._unsafe_attach(indicator, leaf)
                    continue
                if current_class in (
                    _indicators.StartBeam,
                    _indicators.StopBeam,
                ):
                    indicator = current_class()
                    _bind._unsafe_attach(indicator, leaf)
                    continue
                if current_class is _indicators.Tie:
                    indicator = current_class()
                    _bind._unsafe_attach(indicator, leaf)
                    continue

    def _cleanup(self, parsed):
        container = _score.Container()
        for x in parsed:
            container.append(x)
        parsed = container
        leaves = _select.leaves(parsed)
        if leaves:
            self._attach_indicators(leaves)
        for leaf in leaves:
            _bind.detach(dict, leaf)
        if 1 < self._toplevel_component_count:
            return parsed
        return parsed[0]

    def _get_span_events(self, leaf):
        annotations = leaf._get_indicators(dict)
        _bind.detach(dict, leaf)
        annotations = [x for x in annotations if "post events" in x]
        if annotations:
            return annotations[0]["post events"]
        return {}

    def _setup(self):
        self._toplevel_component_count = 0
        self._default_duration = _duration.Duration((1, 4))

    ### PUBLIC PROPERTIES ###

    @property
    def debug(self):
        """
        Gets debug boolean of reduced ly parser.

        Returns true or false.
        """
        return self._debug

    @property
    def lexer_rules_object(self):
        """
        Lexer rules object of reduced ly parser.
        """
        return self

    @property
    def parser_rules_object(self):
        """
        Parser rules object of reduced ly parser.
        """
        return self


### FUNCTIONS ###


def parse_reduced_ly_syntax(string) -> _score.Container:
    """
    Parse the reduced LilyPond rhythmic syntax:

    ..  container:: example

        >>> string = '4 -4. 8.. 5/3 { } 4'
        >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(string)
        >>> container
        Container("c'4 r4. c'8.. { 3:5 } c'4")

        >>> for component in container:
        ...     component
        ...
        Note("c'4")
        Rest('r4.')
        Note("c'8..")
        Tuplet('3:5', '')
        Note("c'4")

    """
    return ReducedLyParser()(string)
