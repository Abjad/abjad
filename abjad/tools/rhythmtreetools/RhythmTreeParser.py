# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools import Parser


class RhythmTreeParser(Parser):
    r'''A rhythm-tree syntax parser.

    Abjad’s rhythm-tree parser parses a micro-language resembling Ircam’s RTM
    Lisp syntax, and generates a sequence of RhythmTree structures, which can
    be furthered manipulated by composers, before being converted into an Abjad
    score object:

    ::

        >>> parser = rhythmtreetools.RhythmTreeParser()

    ::

        >>> string = '(3 (1 (1 ((2 (1 1 1)) 2 2 1))))'
        >>> rhythm_tree_list = parser(string)
        >>> rhythm_tree_container = rhythm_tree_list[0]
        >>> rhythm_tree_container.rtm_format
        '(3 (1 (1 ((2 (1 1 1)) 2 2 1))))'

    ::

        >>> print(format(rhythm_tree_container))
        rhythmtreetools.RhythmTreeContainer(
            children=(
                rhythmtreetools.RhythmTreeLeaf(
                    preprolated_duration=durationtools.Duration(1, 1),
                    is_pitched=True,
                    ),
                rhythmtreetools.RhythmTreeContainer(
                    children=(
                        rhythmtreetools.RhythmTreeContainer(
                            children=(
                                rhythmtreetools.RhythmTreeLeaf(
                                    preprolated_duration=durationtools.Duration(1, 1),
                                    is_pitched=True,
                                    ),
                                rhythmtreetools.RhythmTreeLeaf(
                                    preprolated_duration=durationtools.Duration(1, 1),
                                    is_pitched=True,
                                    ),
                                rhythmtreetools.RhythmTreeLeaf(
                                    preprolated_duration=durationtools.Duration(1, 1),
                                    is_pitched=True,
                                    ),
                                ),
                            preprolated_duration=durationtools.Duration(2, 1),
                            ),
                        rhythmtreetools.RhythmTreeLeaf(
                            preprolated_duration=durationtools.Duration(2, 1),
                            is_pitched=True,
                            ),
                        rhythmtreetools.RhythmTreeLeaf(
                            preprolated_duration=durationtools.Duration(2, 1),
                            is_pitched=True,
                            ),
                        rhythmtreetools.RhythmTreeLeaf(
                            preprolated_duration=durationtools.Duration(1, 1),
                            is_pitched=True,
                            ),
                        ),
                    preprolated_duration=durationtools.Duration(1, 1),
                    ),
                ),
            preprolated_duration=durationtools.Duration(3, 1),
            )

    ::

        >>> base_duration = (1, 4)
        >>> component_list = rhythm_tree_container(base_duration)
        >>> tuplet = component_list[0]
        >>> show(tuplet) # doctest: +SKIP

    ..  doctest::

        >>> print(format(tuplet))
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'2
            \times 4/7 {
                \times 2/3 {
                    c'8
                    c'8
                    c'8
                }
                c'4
                c'4
                c'8
            }
        }

    Returns `RhythmTreeParser` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        return self

    @property
    def parser_rules_object(self):
        return self

    ### LEX SETUP ###

    tokens = (
        'DURATION',
        'LPAREN',
        'RPAREN'
    )

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = ' \n\t\r'

    ### YACC SETUP ###

    start = 'toplevel'

    ### LEX METHODS ###

    def t_DURATION(self, t):
        r'-?[1-9]\d*(/[1-9]\d*)?'
        parts = t.value.partition('/')
        if not parts[2]:
            t.value = durationtools.Duration(int(parts[0]))
        else:
            numerator, denominator = int(parts[0]), int(parts[2])
            fraction = mathtools.NonreducedFraction(numerator, denominator)
            preprolated_duration = durationtools.Duration(fraction)
            if fraction.numerator == preprolated_duration.numerator:
                t.value = preprolated_duration
            else:
                t.value = fraction
        return t

    def t_error(self, t):
        print(("Illegal character '%s'" % t.value[0]))
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    ### YACC METHODS ###

    def p_container__LPAREN__DURATION__node_list_closed__RPAREN(self, p):
        r'''container : LPAREN DURATION node_list_closed RPAREN
        '''
        from abjad.tools import rhythmtreetools
        p[0] = rhythmtreetools.RhythmTreeContainer(
            children=p[3],
            preprolated_duration=abs(p[2]),
            )

    def p_error(self, p):
        if p:
            print(("Syntax error at '%s'" % p.value))
        else:
            print("Syntax error at EOF")

    def p_leaf__INTEGER(self, p):
        r'''leaf : DURATION
        '''
        from abjad.tools import rhythmtreetools
        p[0] = rhythmtreetools.RhythmTreeLeaf(
            preprolated_duration=abs(p[1]),
            is_pitched=0 < p[1],
            )

    def p_node__container(self, p):
        r'''node : container
        '''
        p[0] = p[1]

    def p_node__leaf(self, p):
        r'''node : leaf
        '''
        p[0] = p[1]

    def p_node_list__node_list__node_list_item(self, p):
        r'''node_list : node_list node_list_item
        '''
        p[0] = p[1] + [p[2]]

    def p_node_list__node_list_item(self, p):
        r'''node_list : node_list_item
        '''
        p[0] = [p[1]]

    def p_node_list_closed__LPAREN__node_list__RPAREN(self, p):
        r'''node_list_closed : LPAREN node_list RPAREN
        '''
        p[0] = p[2]

    def p_node_list_item__node(self, p):
        r'''node_list_item : node
        '''
        p[0] = p[1]

    def p_toplevel__EMPTY(self, p):
        r'''toplevel :
        '''
        p[0] = []

    def p_toplevel__toplevel__node(self, p):
        r'''toplevel : toplevel node
        '''
        p[0] = p[1] + [p[2]]
