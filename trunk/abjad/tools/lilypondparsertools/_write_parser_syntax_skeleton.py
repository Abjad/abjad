from _extract_productions_from_parser_output \
    import _extract_productions_from_parser_output
from _extract_token_names_from_parser_tab_hh \
    import _extract_token_names_from_parser_tab_hh
from _extract_token_values_from_parser_output \
    import _extract_token_values_from_parser_output
from _generate_production_map \
    import _generate_production_map
from _match_token_names_with_token_values \
    import _match_token_names_with_token_values


def _write_parser_syntax_skeleton(skeleton_path, parser_output_path, parser_tab_hh_path):

    productions = _generate_production_map(parser_output_path, parser_tab_hh_path)

    f = open(skeleton_path, 'w')

    f.write('from abjad import *\n')
    f.write('from abjad.tools import durationtools\n')
    f.write('from abjad.tools.lilypondparsertools._SyntaxNode._SyntaxNode \\\n')
    f.write('    import _SyntaxNode as Node\n\n\n')
    f.write('class _LilyPondSyntacticalDefinition(object):\n\n')
    f.write('    def __init__(self, client):\n')
    f.write('        self.client = client\n')
    f.write('        self.tokens = self.client.lexdef.tokens\n\n\n')
    f.write("    start_symbol = 'start_symbol'\n\n\n")

    # how to extract associativity from parser?
    f.write("    precedence = (\n")
    f.write("        ('nonassoc', 'COMPOSITE'),\n")
    f.write("        ('nonassoc', 'REPEAT'),\n")
    f.write("        ('nonassoc', 'ALTERNATIVE'),\n")
    f.write("        ('left', 'ADDLYRICS'),\n")
    f.write("        ('nonassoc', 'DEFAULT'),\n")
    f.write("        ('nonassoc', 'FUNCTION_ARGLIST'),\n")
    f.write("        ('right', 'PITCH_IDENTIFIER', 'NOTENAME_PITCH', 'TONICNAME_PITCH', 'UNSIGNED', 'REAL', 'DURATION_IDENTIFIER', ':'),\n")
    f.write("        ('nonassoc', 'NUMBER_IDENTIFIER', '/'),\n")
    f.write("    )\n\n\n")

    f.write('    ### SYNTACTICAL RULES (ALPHABETICAL) ###\n\n\n')

    current_nonterminal = 'start_symbol'

    ly_keys = sorted(filter(lambda x: x.startswith('p_start_symbol'), productions.keys( )))
    for key in ly_keys:
        funcname = key
        docstring = productions[key]
        f.write('    def %s(self, p):\n' % funcname)
        f.write("        %r\n" % docstring)
        f.write("        p[0] = Node('%s', p[1:])\n\n\n" % current_nonterminal)

    for funcname, docstring in sorted(productions.iteritems( )):
        nonterminal = funcname.split('__')[0][2:]    
        if nonterminal == 'start_symbol':
            continue
        if nonterminal != current_nonterminal:
            current_nonterminal = nonterminal
            f.write('    ### %s ###\n\n\n' % current_nonterminal)
        f.write('    def %s(self, p):\n' % funcname)
        f.write("        %r\n" % docstring)
        f.write("        p[0] = Node('%s', p[1:])\n\n\n" % current_nonterminal)


    f.write('    def p_error(self, p):\n')
    f.write('        pass\n\n')

    f.close( )
