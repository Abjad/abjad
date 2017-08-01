# -*- coding: utf-8 -*-
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTGraphvizDirective(ReSTDirective):
    r'''A ReST Graphviz directive.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    __slots__ = (
        '_graph',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        graph=None,
        name=None,
        options=None,
        ):
        from abjad.tools import graphtools
        if graph is not None:
            assert isinstance(graph, graphtools.GraphvizGraph)
        self._graph = graph
        ReSTDirective.__init__(
            self,
            name=name,
            options=options,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _children_rest_format_contributions(self):
        result = ['']
        graphviz_format = str(self.graph)
        for line in graphviz_format.splitlines():
            line = '   {}'.format(line)
            result.append(line)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def directive(self):
        r'''Gets directive of ReST Graphviz directive.

        Returns string.
        '''
        return 'graphviz'

    @property
    def graph(self):
        r'''Gets graph of ReST Graphviz directive.

        Returns Graphviz graph.
        '''
        return self._graph
