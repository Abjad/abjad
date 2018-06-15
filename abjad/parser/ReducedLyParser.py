from abjad import Left, Right
from abjad import utilities
from abjad import mathtools
from abjad import pitch as abjad_pitch
from abjad import core
from abjad import spanners
from abjad.top import attach
from abjad.top import detach
from abjad.system import Parser


class ReducedLyParser(Parser):
    r"""
    Parses the "reduced-ly" syntax, a modified subset of LilyPond syntax.

    ..  container:: example

        >>> parser = abjad.parser.ReducedLyParser()

        Understands LilyPond-like representation of notes, chords and rests:

        >>> string = "c'4 r8. <b d' fs'>16"
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
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

            >>> abjad.f(container)
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

            >>> abjad.f(container)
            {
                c'4
                d'4
            }

        Understands LilyPond-like default durations:

        >>> string = "c'4 d' e' f'"
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
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

            >>> abjad.f(tuplet)
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
                c'4
                \tweak text #tuplet-number::calc-fraction-text
                \tweak edge-height #'(0.7 . 0)
                \times 3/5 {
                    c'8
                    c'8
                    c'8
                }
            }

    ..  container:: example

        Can create measures too:

        >>> string = '| 4/4 4 4 4 4 || 3/8 8 8 8 |'
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
            {
                {   % measure
                    \time 4/4
                    c'4
                    c'4
                    c'4
                    c'4
                }   % measure
                {   % measure
                    \time 3/8
                    c'8
                    c'8
                    c'8
                }   % measure
            }

    ..  container:: example

        Finally, understands ties, slurs and beams:

        >>> string = 'c16 [ ( d ~ d ) f ]'
        >>> container = parser(string)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(container)
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

    __slots__ = (
        '_default_duration',
        '_toplevel_component_count',
        )

    ### INITIALIZER ###

    def __init__(self, debug=False):
        self._default_duration = utilities.Duration((1, 4))
        self._toplevel_component_count = None
        Parser.__init__(self, debug=debug)

    ### LEX SETUP ###

    tokens = (
        'APOSTROPHE',
        'BRACE_L',
        'BRACE_R',
        'BRACKET_L',
        'BRACKET_R',
        'CARAT_L',
        'CARAT_R',
        'COMMA',
        'DOT',
        'FRACTION',
        'INTEGER_N',
        'INTEGER_P',
        'PAREN_L',
        'PAREN_R',
        'PIPE',
        'PITCHNAME',
        'RESTNAME',
        'TILDE',
    )

    t_APOSTROPHE = "'"
    t_BRACE_L = '{'
    t_BRACE_R = '}'
    t_BRACKET_L = '\['
    t_BRACKET_R = '\]'
    t_CARAT_L = '\<'
    t_CARAT_R = '\>'
    t_COMMA = ','
    t_DOT = '\.'
    t_PAREN_L = '\('
    t_PAREN_R = '\)'
    t_PIPE = '\|'
    t_RESTNAME = 'r'
    t_TILDE = '~'

    t_ignore = ' \t\r'

    ### YACC SETUP ###

    start = 'start'

    ### LEX METHODS ###

    def t_FRACTION(self, t):
        r'([1-9]\d*/[1-9]\d*)'
        parts = t.value.split('/')
        t.value = mathtools.NonreducedFraction(int(parts[0]), int(parts[1]))
        return t

    def t_INTEGER_N(self, t):
        r'(-[1-9]\d*)'
        t.value = int(t.value)
        return t

    def t_INTEGER_P(self, t):
        r'([1-9]\d*)'
        t.value = int(t.value)
        return t

    def t_PITCHNAME(self, t):
        r'[a-g](ff|ss|f|s|tqf|tqs|qs|qf)?'
        t.value = abjad_pitch.NamedPitchClass(t.value)
        return t

    def t_error(self, t):
        print(("Illegal character '%s'" % t.value[0]))
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

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
        import abjad
        p[0] = (abjad.Beam, Left)

    def p_beam__BRACKET_R(self, p):
        """
        beam : BRACKET_R
        """
        import abjad
        p[0] = (abjad.Beam, Right)

    def p_chord_body__chord_pitches(self, p):
        """
        chord_body : chord_pitches
        """
        p[0] = core.Chord(p[1], self._default_duration)

    def p_chord_body__chord_pitches__positive_leaf_duration(self, p):
        """
        chord_body : chord_pitches positive_leaf_duration
        """
        p[0] = core.Chord(p[1], p[2])

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
        r"""container : BRACE_L component_list BRACE_R
        """
        p[0] = core.Container()
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
        raise Exception('fixed-duration containers no longer supported.')

    def p_leaf__leaf_body__post_events(self, p):
        """
        leaf : leaf_body post_events
        """
        p[0] = p[1]
        if p[2]:
            annotation = {'post events': p[2]}
            attach(annotation, p[0])

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
        measure = core.Measure(p[2].pair)
        for x in p[3]:
            measure.append(x)
        p[0] = measure

    def p_negative_leaf_duration__INTEGER_N__dots(self, p):
        """
        negative_leaf_duration : INTEGER_N dots
        """
        duration_log = p[1]
        dots = '.' * p[2]
        duration = utilities.Duration.from_lilypond_duration_string(
            '{}{}'.format(abs(duration_log), dots))
        self._default_duration = duration
        p[0] = duration

    def p_note_body__pitch(self, p):
        """
        note_body : pitch
        """
        p[0] = core.Note(p[1], self._default_duration)

    def p_note_body__pitch__positive_leaf_duration(self, p):
        """
        note_body : pitch positive_leaf_duration
        """
        p[0] = core.Note(p[1], p[2])

    def p_note_body__positive_leaf_duration(self, p):
        """
        note_body : positive_leaf_duration
        """
        p[0] = core.Note(0, p[1])

    def p_pitch__PITCHNAME(self, p):
        """
        pitch : PITCHNAME
        """
        p[0] = abjad_pitch.NamedPitch(str(p[1]))

    def p_pitch__PITCHNAME__apostrophes(self, p):
        """
        pitch : PITCHNAME apostrophes
        """
        p[0] = abjad_pitch.NamedPitch(str(p[1]) + "'" * p[2])

    def p_pitch__PITCHNAME__commas(self, p):
        """
        pitch : PITCHNAME commas
        """
        p[0] = abjad_pitch.NamedPitch(str(p[1]) + ',' * p[2])

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
        dots = '.' * p[2]
        duration = utilities.Duration.from_lilypond_duration_string(
            '{}{}'.format(abs(duration_log), dots))
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
        p[0] = core.Rest(self._default_duration)

    def p_rest_body__RESTNAME__positive_leaf_duration(self, p):
        """
        rest_body : RESTNAME positive_leaf_duration
        """
        p[0] = core.Rest(p[2])

    def p_rest_body__negative_leaf_duration(self, p):
        """
        rest_body : negative_leaf_duration
        """
        p[0] = core.Rest(p[1])

    def p_slur__PAREN_L(self, p):
        """
        slur : PAREN_L
        """
        import abjad
        p[0] = (abjad.Slur, Left)

    def p_slur__PAREN_R(self, p):
        """
        slur : PAREN_R
        """
        import abjad
        p[0] = (abjad.Slur, Right)

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
        import abjad
        p[0] = (abjad.Tie, Left)

    def p_tuplet__FRACTION__container(self, p):
        """
        tuplet : FRACTION container
        """
        assert isinstance(p[2], core.Container)
        leaves = p[2][:]
        p[2][:] = []
        p[0] = core.Tuplet(p[1], leaves)

    ### PRIVATE METHODS ###

    def _apply_spanners(self, leaves):
        import abjad

        spanner_references = {
            abjad.Beam: None,
            abjad.Slur: None,
        }

        first_leaf = leaves[0]
        pairs = abjad.sequence(leaves).nwise(wrapped=True)
        for leaf, next_leaf in pairs:
            span_events = self._get_span_events(leaf)
            for current_class, directions in span_events.items():
                starting, stopping = [], []
                for direction in directions:
                    if direction is Left:
                        starting.append(Left)
                    else:
                        stopping.append(Right)

                # apply undirected events immediately,
                # and do not maintain a reference to them
                if current_class is abjad.Tie:
                    if next_leaf is first_leaf:
                        message = 'unterminated {} at {}.'
                        message = message.format(current_class.__name__, leaf)
                        raise Exception(message)
                    previous_tie = [
                        x for x in leaf._get_spanners()
                        if isinstance(x, abjad.Tie)
                        ]
                    if previous_tie:
                        previous_tie[0]._append(next_leaf)
                    else:
                        tie = abjad.Tie()
                        selection = abjad.select([leaf, next_leaf])
                        attach(tie, selection)

                elif current_class is abjad.Beam:
                    # A beam may begin and end on the same leaf
                    # but only one beam spanner may cover any given leaf,
                    # and starting events are processed before ending ones
                    for _ in starting:
                        if spanner_references[current_class] is not None:
                            message = 'already have beam.'
                            raise Exception(message)
                        else:
                            spanner_references[current_class] = current_class()
                    for _ in stopping:
                        if spanner_references[current_class] is not None:
                            spanner_references[current_class]._append(leaf)
                            spanner_references[current_class] = None

                elif current_class is spanners.Slur:
                    # Slurs process stop events before start events,
                    # they must contain more than one leaf,
                    # but they can stop on a leaf and start on the same leaf.
                    for _ in stopping:
                        if spanner_references[current_class] is not None:
                            spanner_references[current_class]._append(leaf)
                            spanner_references[current_class] = None
                        else:
                            message = 'can not end: {}.'
                            message = message.format(current_class.__name)
                            raise Exception(message)
                    for _ in starting:
                        if spanner_references[current_class] is None:
                            spanner_references[current_class] = current_class()
                        else:
                            message = 'already have: {}.'
                            message = message.format(current_class.__name)
                            raise Exception(message)

            # append leaf to all tracked spanners,
            for current_class, instance in spanner_references.items():
                if instance is not None:
                    instance._append(leaf)

        # check for unterminated spanners
        for current_class, instance in spanner_references.items():
            if instance is not None:
                message = 'unterminated {}.'
                message = message.format(current_class.__name__)
                raise Exception(message)

    def _cleanup(self, parsed):
        import abjad
        container = core.Container()
        for x in parsed:
            container.append(x)
        parsed = container
        leaves = abjad.select(parsed).leaves()
        if leaves:
            self._apply_spanners(leaves)
        for leaf in leaves:
            detach(dict, leaf)
        if 1 < self._toplevel_component_count:
            return parsed
        return parsed[0]

    def _get_span_events(self, leaf):
        annotations = leaf._get_indicators(dict)
        detach(dict, leaf)
        annotations = [x for x in annotations if 'post events' in x]
        if annotations:
            return annotations[0]['post events']
        return {}

    def _setup(self):
        self._toplevel_component_count = 0
        self._default_duration = utilities.Duration((1, 4))

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
