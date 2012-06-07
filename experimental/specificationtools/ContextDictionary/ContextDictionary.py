from abjad.tools import contexttools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from specificationtools.ContextProxy import ContextProxy
from specificationtools.ResolvedSetting import ResolvedSetting
from collections import OrderedDict


class ContextDictionary(AbjadObject, OrderedDict):

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

    ### PRIVATE METHODS ###

    def _initialize_context_proxies(self):
        context_names = []
        if self.score is not None:
            for context in contexttools.iterate_contexts_forward_in_expr(self.score):
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
        for context in contexttools.iterate_contexts_forward_in_expr(self.score):
            if isinstance(context, scoretools.Score):
                return context.name

    ### PUBLIC METHODS ###

    def all_are_context_names(self, expr):
        try:
            return all([x in self for x in expr])
        except:
            return False

    def get_settings(self, attribute_name=None, context_name=None, scope=None):
        if context_name is None:
            context_proxies = list(self.itervalues())
        else:
            context_proxies = [self[context_name]]
        settings = []
        for context_proxy in context_proxies:
            settings.extend(context_proxy.get_settings(attribute_name=attribute_name, scope=scope))
        return settings 

    def show(self):
        for context_name in self:
            print context_name
            for setting_name in self[context_name]:
                item = self[context_name][setting_name]
                if isinstance(item, ResolvedSetting):
                    print '\t{}'.format(self[context_name][setting_name])
                else:
                    print '\t{}: {}'.format(setting_name, self[context_name][setting_name])
