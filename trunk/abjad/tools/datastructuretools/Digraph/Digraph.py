import copy
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class Digraph(AbjadObject):
    '''A digraph, built out of edges - pairs of hashable objects:

    ::

        >>> from abjad.tools.datastructuretools import Digraph

    ::

        >>> edges = [('a', 'b'), ('a', 'c'), ('a', 'f'), ('c', 'd'), ('d', 'e'), ('e', 'c')]
        >>> digraph = Digraph(edges)
        >>> digraph
        Digraph(edges=[('a', 'c'), ('a', 'b'), ('a', 'f'), ('c', 'd'), ('d', 'e'), ('e', 'c')])

    ::

        >>> digraph.root_nodes
        ('a',)
        >>> digraph.terminal_nodes
        ('b', 'f')
        >>> digraph.cyclic_nodes
        ('c', 'd', 'e')
        >>> digraph.is_cyclic
        True

    Return `Digraph` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_child_graph', '_cyclic_nodes', '_parent_graph', '_root_nodes', '_terminal_nodes')

    ### INITIALIZER ###

    def __init__(self, edges=None):
        from abjad.tools import datastructuretools

        if edges is not None:
            assert sequencetools.all_are_pairs(edges)

        parent_graph = { }
        child_graph = { }

        edges = set([tuple(edge) for edge in edges])

        for parent, child in edges:
            # populate parent-wise graph
            if parent not in parent_graph:
                parent_graph[parent] = set([child])
            else:
                parent_graph[parent].add(child)
            if child not in parent_graph:
                parent_graph[child] = set([])

            # populate child-wise graph
            if child not in child_graph:
                child_graph[child] = set([parent])
            else:
                child_graph[child].add(parent)
            if parent not in child_graph:
                child_graph[parent] = set([])

        self._parent_graph = datastructuretools.ImmutableDictionary(parent_graph)
        self._child_graph = datastructuretools.ImmutableDictionary(child_graph)
        self._cyclic_nodes = self._find_cyclic_nodes()
        self._root_nodes = tuple(sorted([child for child in child_graph if not child_graph[child]]))
        self._terminal_nodes = tuple(sorted([parent for parent in parent_graph if not parent_graph[parent]]))

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other):
            if self.edges == other.edges:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    ### PUBLIC PROPERTIES ###

    @property
    def child_graph(self):
        '''A dictionary representation of the digraph where the keys are
        child nodes, and where each value is the set of that child's parents.'''
        return self._child_graph

    @property
    def cyclic_nodes(self):
        '''A tuple of those nodes which partake in a cycle.'''
        return self._cyclic_nodes

    @property
    def edges(self):
        '''A tuple of all edges in the graph.'''
        edges = []
        for node in self.nodes:
            for child in self.parent_graph[node]:
                edges.append((node, child))
        return edges

    @property
    def is_cyclic(self):
        '''Return True if the digraph contains any cycles.'''
        if self.cyclic_nodes:
            return True
        return False

    @property
    def nodes(self):
        '''A tuple of all nodes in the graph.'''
        return tuple(sorted(self.parent_graph.keys()))

    @property
    def parent_graph(self):
        '''A dictionary representation of the digraph where the keys are
        parent nodes, and where each value is the set of that parent's children.'''
        return self._parent_graph

    @property
    def root_nodes(self):
        '''A tuple of those nodes which have no parents.'''
        return self._root_nodes

    @property
    def terminal_nodes(self):
        '''A tuple of those nodes which have no children.'''
        return self._terminal_nodes

    ### PRIVATE METHODS ###

    def _find_cyclic_nodes(self):

        parent_graph = { }
        for k, v in self.parent_graph.iteritems():
            parent_graph[k] = copy.copy(v)

        child_graph = { }
        for k, v in self.child_graph.iteritems():
            child_graph[k] = copy.copy(v)

        roots = [child for child in child_graph if not child_graph[child]]
        terminals = [parent for parent in parent_graph if not parent_graph[parent]]

        while roots or terminals:
            for terminal in terminals:
                parents = child_graph[terminal]
                for parent in parents:
                    parent_graph[parent].remove(terminal)
                if terminal in roots:
                    roots.remove(terminal)
                del(parent_graph[terminal])
                del(child_graph[terminal])

            for root in roots:
                children = parent_graph[root]
                for child in children:
                    child_graph[child].remove(root)
                del(parent_graph[root])
                del(child_graph[root])

            roots = [child for child in child_graph if not child_graph[child]]
            terminals = [parent for parent in parent_graph if not parent_graph[parent]]
            
            if not roots and not terminals and parent_graph:
                return tuple(sorted(parent_graph.keys()))

        if parent_graph:
           return tuple(sorted(parent_graph.keys()))
        return ()

    ### PUBLIC METHODS ###

    def partition(self):
        '''Partition the digraph into a list of digraphs according to connectivity:

        ::

            >>> from abjad.tools.datastructuretools import Digraph

        ::

            >>> edges = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'd'), ('d', 'e')]
            >>> edges.extend([('f', 'h'), ('g', 'h')])
            >>> edges.append(('i', 'j'))
            >>> digraph = Digraph(edges)
            >>> for graph in digraph.partition(): graph
            ... 
            Digraph(edges=[('a', 'c'), ('a', 'b'), ('b', 'c'), ('b', 'd'), ('d', 'e')])
            Digraph(edges=[('f', 'h'), ('g', 'h')])
            Digraph(edges=[('i', 'j')])

        Return list of `Digraph` instances.
        '''

        remaining = self.parent_graph.keys()
        graphs = []

        def recurse(node):
            if node not in remaining:
                return []
            remaining.remove(node)
            result = [node]
            for child in self.parent_graph[node]:
                result.extend(recurse(child))
            for parent in self.child_graph[node]:
                result.extend(recurse(parent))
            return result

        while remaining:
            node = remaining[0]
            graph = list(sorted(recurse(node)))
            edges = []
            for node in graph:
                for child in self.parent_graph[node]:
                    edges.append((node, child))
            graphs.append(type(self)(edges))

        return graphs

    def reverse(self):
        '''Reverse all edges in the graph:

        ::

            >>> from abjad.tools.datastructuretools import Digraph

        ::

            >>> edges = [('a', 'b'), ('b', 'c'), ('b', 'd')]
            >>> digraph = Digraph(edges)
            >>> digraph
            Digraph(edges=[('a', 'b'), ('b', 'c'), ('b', 'd')])

        ::

            >>> digraph.reverse()
            Digraph(edges=[('b', 'a'), ('c', 'b'), ('d', 'b')])

        Return `Digraph` instance.
        '''
        return type(self)([(tail, head) for head, tail in self.edges])
