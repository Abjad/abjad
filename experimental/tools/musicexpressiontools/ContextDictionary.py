# -*- encoding: utf-8 -*-
import collections
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextDictionary(AbjadObject, collections.OrderedDict):
    r'''Context dictionary.
    '''

    ### INITIALIZER ###

    def __init__(self, score):
        assert isinstance(score, scoretools.Score), repr(score)
        collections.OrderedDict.__init__(self)
        self._score = score
        self._initialize_single_context_set_expressions_by_context()

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if expr is None:
            return collections.OrderedDict.__getitem__(self, self.score_name)
        else:
            return collections.OrderedDict.__getitem__(self, expr)

    def __repr__(self):
        contents = ', '.join([repr(x) for x in self])
        return '{}([{}])'.format(type(self).__name__, contents)

    def __setitem__(self, key, value):
        from experimental.tools import musicexpressiontools
        assert isinstance(key, str)
        assert isinstance(value, musicexpressiontools.ContextProxy)
        collections.OrderedDict.__setitem__(self, key, value)

    ### PRIVATE METHODS ###

    def _initialize_single_context_set_expressions_by_context(self):
        from experimental.tools import musicexpressiontools
        context_names = []
        if self.score is not None:
            for context in \
                iterationtools.iterate_contexts_in_expr(self.score):
                assert context.context_name is not None, context.name_name
                context_names.append(context.name)
        for context_name in sorted(context_names):
            self[context_name] = musicexpressiontools.ContextProxy()

    ### PUBLIC PROPERTIES ###

    @property
    def score(self):
        r'''Context dictionary score.

        Returns score.
        '''
        return self._score

    @property
    def score_name(self):
        r'''Context dictionary score name.

        Returns string or none.
        '''
        for context in iterationtools.iterate_contexts_in_expr(self.score):
            if isinstance(context, scoretools.Score):
                return context.name

    @property
    def score_proxy(self):
        r'''Context dictionary score proxy.

        Returns context proxy.
        '''
        return self[self.score_name]
