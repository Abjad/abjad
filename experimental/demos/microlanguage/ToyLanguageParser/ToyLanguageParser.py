from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools.abctools.Parser import Parser


class ToyLanguageParser(Parser):
    '''An idiosyncratic, super-compact pitch processing micro-language parser:

    ::

        >>> from experimental.demos import microlanguage
        >>> parser = microlanguage.ToyLanguageParser()
        >>> input_string = "(c' bf, dqs);"
        >>> result = parser(input_string)

    Return ``ToyLanguageParser`` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        Parser.__init__(self, *args, **kwargs)
        self.assignments = {}

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        return self

    @property
    def parser_rules_object(self):
        return self

    ### PRIVATE METHODS ###

    def _setup(self):
        self.assignments.clear()

    ### LEX SETUP ###

    tokens = (
        'APOSTROPHE',
        'COMMA',
        #'COLON',
        #'COUNT',
        'EQUALS',
        'IDENTIFIER',
        #'MINUS',
        'PARENTHESIS_L',
        'PARENTHESIS_R',
        'PITCHNAME',
        #'PLUS',
        'SEMICOLON',
    )

    t_APOSTROPHE = "'"
    t_COMMA = ","
    #t_COLON = ':'
    t_EQUALS = '='
    #t_MINUS = '-'
    t_PARENTHESIS_L = '\('
    t_PARENTHESIS_R = '\)'
    t_PITCHNAME = r'[a-g](ff|ss|f|s|tqf|tqs|qs|qf)?'
    #t_PLUS = '\+'
    t_SEMICOLON = ';'

    t_ignore = ' \n\t\r'

    ### LEX METHODS ###

    #def t_COUNT(self, t):
    #    r'[1-9][0-9]*'
    #    t.value = int(t.value)
    #    return t

    def t_IDENTIFIER(self, t):
        r'\\[a-z]'
        t.value = t.value[1]
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    ### YACC SETUP ###

    start = 'start'

    ### YACC METHODS ###

    ### creating a single pitch ###

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

    def p_pitch__PITCHNAME(self, p):
        '''pitch : PITCHNAME'''
        p[0] = pitchtools.NamedChromaticPitch(p[1])

    def p_pitch__PITCHNAME__apostrophes(self, p):
        '''pitch : PITCHNAME apostrophes'''
        p[0] = pitchtools.NamedChromaticPitch(p[1] + "'" * p[2])

    def p_pitch__PITCHNAME__commas(self, p):
        '''pitch : PITCHNAME commas'''
        p[0] = pitchtools.NamedChromaticPitch(p[1] + ',' * p[2])

    ### creating pitch cells ###

    def p_pitch_cell__PARENTHESIS_L__pitches__PARENTHESIS_R(self, p):
        '''pitch_cell : PARENTHESIS_L pitches PARENTHESIS_R'''
        p[0] = pitchtools.NamedChromaticPitchSegment(p[2])

    def p_pitches__pitch(self, p):
        '''pitches : pitch'''
        p[0] = [p[1]]

    def p_pitches__pitches__pitch(self, p):
        '''pitches : pitches pitch'''
        p[0] = p[1] + [p[2]]

    ### expressions ###

    def p_expression__IDENTIFIER(self, p):
        '''expression : IDENTIFIER'''
        p[0] = self.assignments[p[1]]

    def p_expression__pitch_cell(self, p):
        '''expression : pitch_cell'''
        p[0] = p[1]

    ### variable assignment ###

    def p_assignment__IDENTIFIER__EQUALS__expression(self, p):
        '''assignment : IDENTIFIER EQUALS expression'''
        identifier = p[1]
        expression = p[3]
        self.assignments[identifier] = expression
        p[0] = None

    ### statements ###

    def p_statement__assignment__SEMICOLON(self, p):
        '''statement : assignment SEMICOLON'''
        p[0] = None

    def p_statement__expression__SEMICOLON(self, p):
        '''statement : expression SEMICOLON'''
        p[0] = p[1]

    ### start symbol ###

    def p_start__EMPTY(self, p):
        '''start : statement'''
        p[0] = p[1]

    def p_start__start__statement(self, p):
        '''start : start statement'''
        if p[2] is not None:
            p[0] = p[2]
        else:
            p[0] = p[1]

    ### errors ###

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
