import copy
from abjad.tools import *


class _TupletParser(abctools.Parser):

    ### LEX SETUP ###

    tokens = (
        'APOSTROPHE',
        'BRACE_L',
        'BRACE_R',
        'COMMA',
        'DOT',
        'FRACTION',
        'INTEGER',
        'PAREN_L',
        'PAREN_R',
        'PIPE',
        'PITCHNAME',
        'TILDE',
    )

    t_APOSTROPHE = "'"
    t_BRACE_L = '{'
    t_BRACE_R = '}'
    t_COMMA = ','
    t_DOT = '\.'
    t_PAREN_L = '\('
    t_PAREN_R = '\)'
    t_PIPE = '\|'
    t_TILDE = '~'

    t_ignore = ' \t\r'

    ### YACC SETUP ###

    start = 'start'

    ### LEX METHODS ###

    def t_FRACTION(self, t):
        r'(-?[1-9]\d*/[1-9]\d*)'
        parts = t.value.split('/')
        t.value = mathtools.NonreducedFraction(int(parts[0]), int(parts[1]))
        return t

    def t_INTEGER(self, t):
        r'(-?[1-9]\d*)'
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

    def p_leaf__leaf_duration__post_events(self, p):
        '''leaf : leaf_duration post_events'''
        leaf_duration = p[1]
        post_events = p[2]
        if 0 < p[1]:
            p[0] = notetools.Note(0, leaf_duration)
        else:
            p[0] = resttools.Rest(abs(leaf_duration))
        if post_events:
            marktools.Annotation('post events', post_events)(p[0])

    def p_leaf__pitch__leaf_duration__post_events(self, p):
        '''leaf : pitch leaf_duration post_events'''
        pitch = p[1]
        leaf_duration = abs(p[2])
        post_events = p[3]
        p[0] = notetools.Note(pitch, leaf_duration)
        if post_events:
            marktools.Annotation('post events', post_events)(p[0])

    def p_leaf_duration__INTEGER__dots__post_events(self, p):
        '''leaf_duration : INTEGER dots'''
        duration_log = p[1]
        dots = '.' * p[2]
        if duration_log < 0:
            p[0] = -durationtools.Duration('{}{}'.format(abs(duration_log), dots))
        else:
            p[0] = durationtools.Duration('{}{}'.format(abs(duration_log), dots))
        
    def p_measure__PIPE__FRACTION__component_list__PIPE(self, p):
        '''measure : PIPE FRACTION component_list PIPE'''
        p[0] = measuretools.Measure(p[2].pair)
        for x in p[3]:
            p[0].append(x)

    def p_pair__PAREN_L__INTEGER__INTEGER__PAREN_R(self, p):
        '''pair : PAREN_L INTEGER INTEGER PAREN_R'''
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

    def p_post_event__tie(self, p):
        '''post_event : tie'''
        p[0] = p[1]

    def p_post_events__EMPTY(self, p):
        '''post_events : '''
        p[0] = []

    def p_post_events__post_events__post_event(self, p):
        '''post_events : post_events post_event'''
        p[0] = p[1] + [p[2]]

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

    ### PUBLIC METHODS ###

    def cleanup(self, parsed):

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
