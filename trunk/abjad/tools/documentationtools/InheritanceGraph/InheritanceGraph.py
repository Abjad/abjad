import inspect
import types
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
        abjad> class C(B): pass
        ...
        abjad> class D(B): pass
        ...
        abjad> class E(C, D): pass
        ...
        abjad> class F(A): pass
        ...

    ::

        abjad> graph = InheritanceGraph(F, E)

    ::

        abjad> for parent, children in sorted(graph.items()):
        ...     parent, tuple(sorted(children))
        (<type 'object'>, (<class '__main__.A'>,))
        (<class '__main__.A'>, (<class '__main__.B'>, <class '__main__.F'>))
        (<class '__main__.B'>, (<class '__main__.C'>, <class '__main__.D'>))
        (<class '__main__.C'>, (<class '__main__.E'>,))
        (<class '__main__.D'>, (<class '__main__.E'>,))
        (<class '__main__.E'>, ())
        (<class '__main__.F'>, ())

    ``InheritanceGraph`` may be instantiated from one or more instances, classes or
    modules.  If instantiated from a module, all public classes in that module
    will be taken into the graph.

    A `root_class` keyword may be defined at instantiation, which filters out
    all klasses from the graph which do not inherit from that `root_class` (or
    are not already the `root_class`):

    ::

        abjad> graph = InheritanceGraph(A, B, C, D, E, F, root_class=B)
        abjad> for parent, children in sorted(graph.items()):
        ...     parent, tuple(sorted(children))
        (<class '__main__.B'>, (<class '__main__.C'>, <class '__main__.D'>))
        (<class '__main__.C'>, (<class '__main__.E'>,))
        (<class '__main__.D'>, (<class '__main__.E'>,))
        (<class '__main__.E'>, ())

    Returns ``InheritanceGraph`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_root_class')

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        assert 0 < len(args)

        if 'root_class' in kwargs:
            assert isinstance(kwargs['root_class'], types.TypeType)
            self._root_class = kwargs['root_class']
        else:
            self._root_class = None

        klasses = []
        for x in args:
            if isinstance(x, types.TypeType):
                klasses.append(x)
            elif type(x).__name__ == 'module':
                klasses.extend([klass for klass in x.__dict__.values() if isinstance(klass, types.TypeType)])
            else:
                klasses.append(x.__class__)

        if self.root_class is None:
            graph = {}

            def _recurse(klass):
                if klass not in graph:
                    graph[klass] = []
                for base in klass.__bases__:
                    if base not in graph:
                        graph[base] = []
                        _recurse(base)
                    if klass not in graph[base]:
                        graph[base].append(klass)

            for klass in klasses:
                _recurse(klass)

        else:
            graph = {self.root_class: []}

            def _recurse(klass):
                if self.root_class in inspect.getmro(klass) and klass not in graph:                    
                    graph[klass] = []
                for base in klass.__bases__:
                    if base in graph:
                        if klass not in graph[base]:
                            graph[base].append(klass)
                    elif self.root_class in inspect.getmro(base):
                        graph[base] = [klass]
                        _recurse(base)

            for klass in klasses:
                _recurse(klass)

        for k, v in graph.iteritems():
            graph[k] = tuple(sorted(v))

        dict.__init__(self, graph)

    ### PUBLIC ATTRIBUTES ###

    @property
    def root_class(self):
        return self._root_class
