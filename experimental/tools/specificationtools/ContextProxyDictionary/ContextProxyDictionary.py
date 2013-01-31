from collections import OrderedDict
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextProxyDictionary(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    def __init__(self, score):
        assert isinstance(score, scoretools.Score), repr(score)
        OrderedDict.__init__(self)
        self._score = score
        self._initialize_context_proxies()

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

    def _initialize_context_proxies(self):
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
        return self._score

    @property
    def score_context_proxy(self):
        return self[self.score_name]

    @property
    def score_name(self):
        for context in iterationtools.iterate_contexts_in_expr(self.score):
            if isinstance(context, scoretools.Score):
                return context.name

    ### PUBLIC METHODS ###

    def all_are_context_names(self, expr):
        try:
            return all([x in self for x in expr])
        except:
            return False

    # TODO: remove in favor of some Specification property (or method)
    def get_set_expressions(self, attribute=None):
        #raise Exception('deprecated')
        from experimental.tools import specificationtools
        set_expressions = []
        for context_proxy in self.itervalues():
            assert isinstance(context_proxy, specificationtools.ContextProxy), repr(context_proxy)
            set_expressions.extend(context_proxy.single_context_set_expressions_by_attribute.get(attribute, []))
        return set_expressions 
