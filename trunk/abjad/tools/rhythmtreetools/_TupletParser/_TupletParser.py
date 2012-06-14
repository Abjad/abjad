import copy
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import marktools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import sequencetools
from abjad.tools import tuplettools
from abjad.tools.rhythmtreetools._Parser import _Parser


class _TupletParser(_Parser):

    ### LEX SETUP ###

    tokens = (
        'BRACE_L',
        'BRACE_R',
        'COMMA',
        'DOT',
        'FRACTION',
        'INTEGER',
        'PAREN_L',
        'PAREN_R',
        'PIPE',
        'TILDE',
    )

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

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    ### YACC METHODS ###

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

    def p_leaf__INTEGER__dots__post_events(self, p):
        '''leaf : INTEGER dots post_events'''
        dots = '.' * p[2]
        post_events = p[3]
        if 0 < p[1]:
            p[0] = notetools.Note("c'{}{}".format(p[1], dots))
        else:
            p[0] = resttools.Rest('{}{}'.format(abs(p[1]), dots))
        if post_events:
            marktools.Annotation('post events', post_events)(p[0])

    def p_pair__PAREN_L__INTEGER__COMMA__INTEGER__PAREN_R(self, p):
        '''pair : PAREN_L INTEGER COMMA INTEGER PAREN_R'''
        p[0] = durationtools.Duration(p[2], p[4])

    def p_measure__PIPE__FRACTION__component_list__PIPE(self, p):
        '''measure : PIPE FRACTION component_list PIPE'''
        p[0] = measuretools.Measure(p[2].pair)
        for x in p[3]:
            p[0].append(x)

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
