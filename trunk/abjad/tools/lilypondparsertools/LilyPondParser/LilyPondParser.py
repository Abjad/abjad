import os
from ply import yacc
from abjad.tools.durationtools import Duration

from abjad.ly.py.current_module import current_module
from abjad.ly.py.language_pitch_names import language_pitch_names
from abjad.ly.py.markup_functions import markup_functions
from abjad.ly.py.markup_functions import markup_list_functions

from abjad.tools.lilypondparsertools._LexerProxy._LexerProxy import _LexerProxy
from abjad.tools.lilypondparsertools._LilyPondLexicalDefinition._LilyPondLexicalDefinition \
    import _LilyPondLexicalDefinition
from abjad.tools.lilypondparsertools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition \
    import _LilyPondSyntacticalDefinition
from abjad.tools.lilypondparsertools._LilyPondSyntaxNode._LilyPondSyntaxNode \
    import _LilyPondSyntaxNode as Node


class LilyPondParser(object):

    def __init__(self):
        self.lexdef = _LilyPondLexicalDefinition(self)
        self.syndef = _LilyPondSyntacticalDefinition(self)
        self.output_path = os.path.dirname(__file__)
        self.pickle_path = os.path.join(self.output_path, '_parsetab.pkl')

        self.lexer = _LexerProxy(object=self.lexdef)
        self.parser = yacc.yacc(
            debug=0,
            module=self.syndef,
            outputdir=self.output_path,
            picklefile=self.pickle_path)

        self.current_module = current_module
        self.language_pitch_names = language_pitch_names
        self.markup_functions = markup_functions
        self.markup_list_functions = markup_list_functions

        self._reset( )

    ### OVERRIDES ###

    def __call__(self, input_string):
        self._reset( )
        concrete_syntax_tree = self.parser.parse(input_string, lexer=self.lexer)
        return concrete_syntax_tree

    ### PRIVATE METHODS ###

    def _reset(self):
        try:
            self.parser.restart( )
        except:
            pass

        self.lexer.push_state('notes')

        self.assignments = { }
        self.spanner_attachments = { }
        self.parser_variables = {
            'default_duration': Node('multiplied_duration', [Duration(1, 4)]),
            'language': 'english',
        }

    def _build_chain_from_zero(self, p, node_name):
        if len(p) == 1:
            p[0] = Node(node_name, [ ])
        else:
            items = list(p[1].value)
            if p[2] is not None:
                items.append(p[2])
            p[0] = Node(node_name, items)

    def _build_chain_from_one(self, p, node_name):
        if len(p) == 2:
            p[0] = Node(node_name, [p[1]])
        else:
            items = list(p[1].value)
            if p[2] is not None:
                items.append(p[2])
            p[0] = Node(node_name, items)

    def _build_right_hand_side(self, p):
        rh = [ ]
        for x in p[1:]:
            if hasattr(x, 'type'):
                rh.append(x.type)
            else:
                rh.append(x)
        return tuple(rh)

    def _resolve_identifier(self, identifier):
        name = identifier[1:]
        if name in self.client.assignments:
            return self.client.assignments[name]
        else:
            return self.client.current_module[name]
        raise Exception('Unknown identifer: %s' % identifier)
