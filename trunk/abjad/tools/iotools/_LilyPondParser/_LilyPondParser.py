from abjad.tools.iotools._LilyPondSyntaxTranslator._LilyPondSyntaxTranslator \
    import _LilyPondSyntaxTranslator
from abjad.tools.iotools._LilyPondGrammar._LilyPondGrammar \
    import _LilyPondGrammar
from abjad.tools.iotools._LilyPondLexicalAnalyzer._LilyPondLexicalAnalyzer \
    import _LilyPondLexicalAnalyzer
from abjad.tools.iotools._LilyPondSemanticAnalyzer._LilyPondSemanticAnalyzer \
    import _LilyPondSemanticAnalyzer
from abjad.tools.iotools._LilyPondSyntacticalAnalyzer._LilyPondSyntacticalAnalyzer \
    import _LilyPondSyntacticalAnalyzer


class _LilyPondParser(object):

    def __init__(self):
        self._grammar = _LilyPondGrammar( )
        self._input_string = ''
        self._lexical_analyzer = _LilyPondLexicalAnalyzer(self)
        self._semantic_analyzer = _LilyPondSemanticAnalyzer(self)
        self._symbol_table = [ ]
        self._syntactical_analyzer = _LilyPondSyntacticalAnalyzer(self)
        self._syntax_translator = _LilyPondSyntaxTranslator(self)

    ### OVERRIDES ###

    def __call__(self, input_string):
        self.input_string = input_string # store for error reporting, later

        # convert input string into token stream
        tokens = self._lexical_analyzer(input_string)

        # create concrete syntax tree, using simplified LilyPond context-free grammar
        parse_tree = self._syntactical_analyzer(tokens)

        # create abstract syntax tree, to cook out alternate syntaxes
        syntax_tree = self._semantic_analyzer(parse_tree)

        # translate abstract syntax tree into Abjad component tree
        lily_file = self._syntax_translator(syntax_tree)

        # reduce component tree to smallest necessary container
        components = self._reduce_lily_file(lily_file)

        return abjad_tree

    ### PRIVATE METHODS ###

    def _reduce_lily_file(self, lily_file):
        return lily_file

    ### PUBLIC ATTRIBUTES ###

    @property
    def input_string(self):
        return self._input_string

    @input_string.setter
    def input_string(self, arg):
        if not isinstance(arg, str) or not len(arg):
            raise ValueError
        self._input_string = arg
