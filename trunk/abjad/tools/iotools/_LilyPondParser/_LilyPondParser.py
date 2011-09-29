from abjad.tools.iotools._LilyPondAbjadCodeGenerator._LilyPondAbjadCodeGenerator \
    import _LilyPondAbjadCodeGenerator
from abjad.tools.iotools._LilyPondGrammar._LilyPondGrammar \
    import _LilyPondGrammar
from abjad.tools.iotools._LilyPondLexicalAnalyzer._LilyPondLexicalAnalyzer \
    import _LilyPondLexicalAnalyzer
from abjad.tools.iotools._LilyPondSyntacticalAnalyzer._LilyPondSyntacticalAnalyzer \
    import _LilyPondSyntacticalAnalyzer


class _LilyPondParser(object):

    def __init__(self):
        self._code_generator = _LilyPondAbjadCodeGenerator(self)
        self._grammar = _LilyPondGrammar( )
        self._input_string = ''
        self._lexical_analyzer = _LilyPondLexicalAnalyzer(self)
        self._symbol_table = { }
        self._syntactical_analyzer = _LilyPondSyntacticalAnalyzer(self)

    ### OVERRIDES ###

    def __call__(self, input_string):
        self.input_string = input_string # store for error reporting, later
        tokens = self._lexical_analyzer(input_string)
        syntax_tree = self._syntactical_analyzer(tokens)
        abjad_tree = self._code_generator(syntax_tree)
        return abjad_tree
        
    ### PUBLIC ATTRIBUTES ###

    @property
    def input_string(self):
        return self._input_string

    @input_string.setter
    def input_string(self, arg):
        if not isinstance(arg, str) or not len(arg):
            raise ValueError
        self._input_string = arg
