import os
from ply import lex
from ply import yacc
from abjad.tools.iotools._LilyPondLexicalDefinition._LilyPondLexicalDefinition \
    import _LilyPondLexicalDefinition
from abjad.tools.iotools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition \
    import _LilyPondSyntacticalDefinition


class _LilyPondParser(object):

    def __init__(self):
        self.table_path = os.path.join(os.path.dirname(__file__), '_tab.py')

    ### OVERRIDES ###

    def __call__(self, input_string):

        lexdef = _LilyPondLexicalDefinition( )
        syndef = _LilyPondSyntacticalDefinition( )

        lexer = lex.lex(object=lexdef)
        parser = yacc.yacc(
            debug=0,
            module=syndef,
            outputdir=os.path.dirname(__file__),
            tabmodule='_parser_tables',)

        lexer.push_state('notes')

        return parser.parse(input_string, lexer=lexer)
