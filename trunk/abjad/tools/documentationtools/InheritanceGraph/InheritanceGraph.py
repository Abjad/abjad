from abjad.tools.datastructuretools import ImmutableDictionary


class InheritanceGraph(ImmutableDictionary):
    '''Generates a graph of a class or collection of classes as a dictionary
    of parent:children relationships:

    ::

        abjad> from abjad.tools.documentationtools import InheritanceGraph

    ::

        abjad> class A(object): pass
        ...
        abjad> class B(A): pass
        ...
        abjad> class C(A): pass
        ...
        abjad> class D(B, C): pass
        ...
        abjad> class E(object): pass
        ...
        abjad> graph = InheritanceGraph(D, E)
        abjad> for parent, children in sorted(graph.items()):
        ...     parent, children
        (<type 'object'>, (<class '__main__.A'>, <class '__main__.E'>))
        (<class '__main__.A'>, (<class '__main__.B'>, <class '__main__.C'>))
        (<class '__main__.B'>, (<class '__main__.D'>,))
        (<class '__main__.C'>, (<class '__main__.D'>,))
        (<class '__main__.D'>, ())
        (<class '__main__.E'>, ())

    ``InheritanceGraph`` may be instantiated from or more instances, classes or
    modules.  If instantiated from a module, all public classes in that module
    will be taken into the graph.

    Return ``InheritanceGraph`` instance.
    '''

    def __init__(self, *args):
        assert 0 < len(args)

        klasses = []
        for x in args:
            if isinstance(x, type):
                klasses.append(x)
            elif type(x).__name__ == 'module':
                klasses.extend([klass for klass in x.__dict__.values() if isinstance(klass, type)])
            else:
                klasses.append(x.__class__)

        graph = { }

        def _recurse(klass):
            if klass not in graph:
                graph[klass] = [ ]
            for base in klass.__bases__:
                if base not in graph:
                    graph[base] = [ ]
                if klass not in graph[base]:
                    graph[base].append(klass)
                _recurse(base)

        for klass in klasses:
            _recurse(klass)

        for k, v in graph.iteritems():
            graph[k] = tuple(sorted(v))

        dict.__init__(self, graph)
