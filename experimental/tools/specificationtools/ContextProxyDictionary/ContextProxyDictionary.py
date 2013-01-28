from collections import OrderedDict
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import expressiontools
from experimental.tools.specificationtools.ContextProxy import ContextProxy


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
        #self._debug(key, 'key')
        #self._debug(value, 'value')
        assert isinstance(key, str), repr(key)
        assert isinstance(value, ContextProxy), repr(value)
        OrderedDict.__setitem__(self, key, value)

    ### PRIVATE METHODS ###

    def _initialize_context_proxies(self):
        context_names = []
        if self.score is not None:
            for context in iterationtools.iterate_contexts_in_expr(self.score):
                assert context.context_name is not None, context.name_name
                context_names.append(context.name)
        for context_name in sorted(context_names):
            self[context_name] = ContextProxy()

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

    def get_set_expressions(self, attribute=None, context_name=None):
        #self._debug(attribute, 'attribute')
        #self._debug(context_name, 'context_name')
        if context_name is None:
            context_proxies = list(self.itervalues())
        else:
            context_proxies = [self[context_name]]
        #for context_proxy in context_proxies:
        #    self._debug(context_proxy)
        set_expressions = []
        for context_proxy in context_proxies:
            # old behavior
            if isinstance(context_proxy, ContextProxy):
                set_expressions.extend(context_proxy.get_set_expressions(attribute=attribute))
            # new behavior
            elif isinstance(context_proxy, list):
                for set_expression in context_proxy:
                    if set_expression.attribute == attribute or attribute is None:
                        set_expressions.append(set_expression)
            else:
                raise ValueError
        #self._debug(set_expressions, 'set_expressions')
        #print ''
        return set_expressions 

    def show(self):
        for context_name in self:
            print context_name
            for set_expression_name in self[context_name]:
                item = self[context_name][set_expression_name]
                if isinstance(item, expressiontools.InputSetExpression):
                    print '\t{}'.format(self[context_name][set_expression_name])
                else:
                    print '\t{}: {}'.format(set_expression_name, self[context_name][set_expression_name])
