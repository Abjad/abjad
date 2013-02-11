from collections import OrderedDict
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextDictionary(AbjadObject, OrderedDict):
    '''Context dictionary.
    '''

    ### INITIALIZER ###

    def __init__(self, score):
        assert isinstance(score, scoretools.Score), repr(score)
        OrderedDict.__init__(self)
        self._score = score
        self._initialize_single_context_set_expressions_by_context()

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if expr is None:
            return OrderedDict.__getitem__(self, self.score_name)
        else:
            return OrderedDict.__getitem__(self, expr)
            
    def __repr__(self):
        contents = ', '.join([repr(x) for x in self])
        return '{}([{}])'.format(self._class_name, contents)

    def __setitem__(self, key, value):
        from experimental.tools import specificationtools
        assert isinstance(key, str), repr(key)
        assert isinstance(value, specificationtools.ContextProxy), repr(value)
        OrderedDict.__setitem__(self, key, value)

    ### PRIVATE METHODS ###

    def _initialize_single_context_set_expressions_by_context(self):
        from experimental.tools import specificationtools
        context_names = []
        if self.score is not None:
            for context in iterationtools.iterate_contexts_in_expr(self.score):
                assert context.context_name is not None, context.name_name
                context_names.append(context.name)
        for context_name in sorted(context_names):
            self[context_name] = specificationtools.ContextProxy()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score(self):
        '''Context dictionary score.
        
        Return score.
        '''
        return self._score

    @property
    def score_name(self):
        '''Context dictionary score name.

        Return string or none.
        '''
        for context in iterationtools.iterate_contexts_in_expr(self.score):
            if isinstance(context, scoretools.Score):
                return context.name

    @property
    def score_proxy(self):
        '''Context dictionary score proxy.

        Return context proxy.
        '''
        return self[self.score_name]
