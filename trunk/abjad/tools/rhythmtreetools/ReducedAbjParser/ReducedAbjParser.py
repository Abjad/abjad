import copy
from abjad.tools import abctools
from abjad.tools import chordtools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import marktools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import resttools
from abjad.tools import sequencetools
from abjad.tools import tietools
from abjad.tools import tuplettools


class ReducedAbjParser(abctools.Parser):
    r'''Parses the "reduced-ly" syntax, a modified subset of LilyPond syntax:

    ::

        >>> parser = rhythmtreetools.ReducedAbjParser()

    Understands LilyPond-like representation of notes, chords and rests:

    ::

        >>> string = "c'4 r8. <b d' fs'>16"
        >>> result = parser(string)
        >>> f(result)
        {
            c'4
            r8.
            <b d' fs'>16
        }

    Also parses bare duration as notes on middle-C, and negative bare durations
    as rests:

    ::

        >>> string = '4 -8 16. -32'
        >>> result = parser(string)
        >>> f(result)
        {
            c'4
            r8
            c'16.
            r32
        }

    Note that the leaf syntax is greedy, and therefore duration specifiers
    following pitch specifiers will be treated as part of the same expression.
    The following produces 2 leaves, rather than 3:

    ::

        >>> string = "4 d' 4"
        >>> result = parser(string)
        >>> f(result)
        {
            c'4
            d'4
        }

    Understands LilyPond-like default durations:
    
    ::
    
        >>> string = "c'4 d' e' f'"
        >>> result = parser(string)
        >>> f(result)
        {
            c'4
            d'4
            e'4
            f'4
        }
    
    Also understands various types of container specifications.
    
    Can create arbitrarily nested tuplets:
    
    ::
    
        >>> string = "2/3 { 4 4 3/5 { 8 8 8 } }"
        >>> result = parser(string)
        >>> f(result)
        {
            \times 2/3 {
                c'4
                c'4
                \fraction \times 3/5 {
                    c'8
                    c'8
                    c'8
                }
            }
        }

    Can also create empty `FixedDurationContainers`:

    ::

        >>> string = '(1 4) (2 4) (3 4) (4 4)'
        >>> result = parser(string)
        >>> for x in result: x
        ... 
        FixedDurationContainer(Duration(1, 4), [])
        FixedDurationContainer(Duration(1, 2), [])
        FixedDurationContainer(Duration(3, 4), [])
        FixedDurationContainer(Duration(1, 1), [])

    Can create measures too:

    ::

        >>> string = '| 4/4 4 4 4 4 || 3/8 8 8 8 |'
        >>> result = parser(string)
        >>> for x in result: x
        ...
        Measure(4/4, [c'4, c'4, c'4, c'4])
        Measure(3/8, [c'8, c'8, c'8])

    Finally, understands ties:

    ::

        >>> string = '4 ~ 4'
        >>> result = parser(string)
        >>> f(result)
        {
            c'4 ~
            c'4
        }

    Return `ReducedAbjParser` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, debug=False):
        abctools.Parser.__init__(self, debug=debug)
        self._default_duration = durationtools.Duration((1, 4))

    ### LEX SETUP ###

    tokens = (
        'APOSTROPHE',
        'BRACE_L',
        'BRACE_R',
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
        t.value = pitchtools.NamedChromaticPitchClass(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    ### YACC METHODS ###

    def p_apostrophes__APOSTROPHE(self, p):
        '''apostrophes : APOSTROPHE'''
        p[0] = 1

    def p_apostrophes__apostrophes__APOSTROPHE(self, p):
        '''apostrophes : apostrophes APOSTROPHE'''
        p[0] = p[1] + 1 

    def p_chord_body__chord_pitches(self, p):
        '''chord_body : chord_pitches'''
        p[0] = chordtools.Chord(p[1], self._default_duration)

    def p_chord_body__chord_pitches__positive_leaf_duration(self, p):
        '''chord_body : chord_pitches positive_leaf_duration'''
        p[0] = chordtools.Chord(p[1], p[2])

    def p_chord_pitches__CARAT_L__pitches__CARAT_R(self, p):
        '''chord_pitches : CARAT_L pitches CARAT_R'''
        p[0] = p[2]

    def p_commas__COMMA(self, p):
        '''commas : COMMA'''
        p[0] = 1

    def p_commas__commas__commas(self, p):
        '''commas : commas COMMA'''
        p[0] = p[1] + 1 

    def p_component__container(self, p):
        '''component : container'''
        p[0] = p[1]

    def p_component__fixed_duration_container(self, p):
        '''component : fixed_duration_container'''
        p[0] = p[1]

    def p_component__leaf(self, p):
        '''component : leaf'''
        p[0] = p[1]

    def p_component__tuplet(self, p):
        '''component : tuplet'''
        p[0] = p[1]

    def p_component_list__EMPTY(self, p):
        '''component_list : '''
        p[0] = []

    def p_component_list__component_list__component(self, p):
        '''component_list : component_list component'''
        p[0] = p[1] + [p[2]]

    def p_container__BRACE_L__component_list__BRACE_R(self, p):
        '''container : BRACE_L component_list BRACE_R'''
        p[0] = containertools.Container()
        for component in p[2]:
            p[0].append(component)

    def p_dots__dots__DOT(self, p):
        '''dots : dots DOT'''
        p[0] = p[1] + 1

    def p_dots__EMPTY(self, p):
        '''dots : '''
        p[0] = 0

    def p_fixed_duration_container__pair(self, p):
        '''fixed_duration_container : pair'''
        p[0] = containertools.FixedDurationContainer(p[1])

    def p_leaf__leaf_body__post_events(self, p):
        '''leaf : leaf_body post_events'''
        p[0] = p[1]
        if p[2]:
            marktools.Annotation('post events', tuple(p[2]))(p[0])

    def p_leaf_body__chord_body(self, p):
        '''leaf_body : chord_body'''
        p[0] = p[1]

    def p_leaf_body__note_body(self, p):
        '''leaf_body : note_body'''
        p[0] = p[1]

    def p_leaf_body__rest_body(self, p):
        '''leaf_body : rest_body'''
        p[0] = p[1]

    def p_measure__PIPE__FRACTION__component_list__PIPE(self, p):
        '''measure : PIPE FRACTION component_list PIPE'''
        p[0] = measuretools.Measure(p[2].pair)
        for x in p[3]:
            p[0].append(x)

    def p_negative_leaf_duration__INTEGER_N__dots(self, p):
        '''negative_leaf_duration : INTEGER_N dots'''
        duration_log = p[1]
        dots = '.' * p[2]
        duration = durationtools.Duration('{}{}'.format(abs(duration_log), dots))
        self._default_duration = duration
        p[0] = duration

    def p_note_body__pitch(self, p):
        '''note_body : pitch'''
        p[0] = notetools.Note(p[1], self._default_duration)

    def p_note_body__pitch__positive_leaf_duration(self, p):
        '''note_body : pitch positive_leaf_duration'''
        p[0] = notetools.Note(p[1], p[2])

    def p_note_body__positive_leaf_duration(self, p):
        '''note_body : positive_leaf_duration'''
        p[0] = notetools.Note(0, p[1])

    def p_pair__PAREN_L__INTEGER_P__INTEGER_P__PAREN_R(self, p):
        '''pair : PAREN_L INTEGER_P INTEGER_P PAREN_R'''
        p[0] = durationtools.Duration(p[2], p[3])

    def p_pitch__PITCHNAME(self, p):
        '''pitch : PITCHNAME'''
        p[0] = pitchtools.NamedChromaticPitch(str(p[1]))

    def p_pitch__PITCHNAME__apostrophes(self, p):
        '''pitch : PITCHNAME apostrophes'''
        p[0] = pitchtools.NamedChromaticPitch(str(p[1]) + "'" * p[2])

    def p_pitch__PITCHNAME__commas(self, p):
        '''pitch : PITCHNAME commas'''
        p[0] = pitchtools.NamedChromaticPitch(str(p[1]) + ',' * p[2])

    def p_pitches__pitch(self, p):
        '''pitches : pitch'''
        p[0] = [p[1]]

    def p_pitches__pitches__pitch(self, p):
        '''pitches : pitches pitch'''
        p[0] = p[1] + [p[2]]

    def p_positive_leaf_duration__INTEGER_P__dots(self, p):
        '''positive_leaf_duration : INTEGER_P dots'''
        duration_log = p[1]
        dots = '.' * p[2]
        duration = durationtools.Duration('{}{}'.format(abs(duration_log), dots))
        self._default_duration = duration
        p[0] = duration       

    def p_post_event__tie(self, p):
        '''post_event : tie'''
        p[0] = p[1]

    def p_post_events__EMPTY(self, p):
        '''post_events : '''
        p[0] = []

    def p_post_events__post_events__post_event(self, p):
        '''post_events : post_events post_event'''
        p[0] = p[1] + [p[2]]

    def p_rest_body__negative_leaf_duration(self, p):
        '''rest_body : negative_leaf_duration'''
        p[0] = resttools.Rest(p[1])

    def p_rest_body__RESTNAME(self, p):
        '''rest_body : RESTNAME'''
        p[0] = resttools.Rest(self._default_duration) 

    def p_rest_body__RESTNAME__positive_leaf_duration(self, p):
        '''rest_body : RESTNAME positive_leaf_duration'''
        p[0] = resttools.Rest(p[2])

    def p_start__EMPTY(self, p):
        '''start : '''
        p[0] = []

    def p_start__start__component(self, p):
        '''start : start component'''
        p[0] = p[1] + [p[2]]

    def p_start__start__measure(self, p):
        '''start : start measure'''
        p[0] = p[1] + [p[2]]

    def p_tie__TILDE(self, p):
        '''tie : TILDE'''
        p[0] = tietools.TieSpanner

    def p_tuplet__FRACTION__container(self, p):
        '''tuplet : FRACTION container'''
        p[0] = tuplettools.Tuplet(p[1], p[2][:])

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        return self

    @property
    def parser_rules_object(self):
        return self

    ### PRIVATE METHODS ###

    def _cleanup(self, parsed):
        '''Post-parsing cleanup.

        Apply TieSpanners where necessary.

        Detach all Annotations.

        Return parsed expression.
        '''

        container = containertools.Container()
        for x in parsed:
            container.append(x)
        parsed = container
        leaves = parsed.leaves

        for first_leaf, second_leaf in sequencetools.iterate_sequence_pairwise_strict(leaves):
            annotations = marktools.get_annotations_attached_to_component(first_leaf)
            post_events = [x for x in annotations if x.name == 'post events']
            if not post_events:
                continue
            
            if tietools.TieSpanner in post_events[0].value:
                previous_ties = [x for x in first_leaf.spanners if isinstance(x, tietools.TieSpanner)]
                if previous_ties:
                    previous_ties[0].append(second_leaf)
                else:
                    tietools.TieSpanner([first_leaf, second_leaf])

        for leaf in leaves:
            marktools.detach_annotations_attached_to_component(leaf)

        return parsed

    def _setup(self):
        self._default_duration = durationtools.Duration((1, 4))
