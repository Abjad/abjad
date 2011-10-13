import os
from ply import lex
from ply import yacc
from abjad.tools.iotools._LilyPondLexicalDefinition._LilyPondLexicalDefinition \
    import _LilyPondLexicalDefinition
from abjad.tools.iotools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition \
    import _LilyPondSyntacticalDefinition


class _LilyPondParser(object):

    ### OVERRIDES ###

    def __call__(self, input_string):

        output_path = os.path.dirname(__file__)
        pickle_path = os.path.join(output_path, '_parsetab.pkl')

        lexdef = _LilyPondLexicalDefinition( )
        syndef = _LilyPondSyntacticalDefinition( )

        lexer = lex.lex(
            object=lexdef)

        parser = yacc.yacc(
            debug=0,
            module=syndef,
            outputdir=output_path,
            picklefile=pickle_path)

        lexer.push_state('notes')

        concrete_syntax_tree = parser.parse(input_string, lexer=lexer)

        return concrete_syntax_tree
