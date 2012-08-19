import inspect
import types
from abjad.tools.datastructuretools import ImmutableDictionary


class InheritanceGraph(ImmutableDictionary):
    '''Generates a graph of a class or collection of 
    classes as a dictionary of parent-children relationships::

        >>> from abjad.tools.documentationtools import InheritanceGraph

    ::

        >>> class A(object): pass
        ...
        >>> class B(A): pass
        ...
        >>> class C(B): pass
        ...
        >>> class D(B): pass
        ...
        >>> class E(C, D): pass
        ...
        >>> class F(A): pass
        ...

    ::

        >>> graph = InheritanceGraph(F, E)

    ::

        >>> result = sorted(graph.items(), key=lambda x: x[0].__name__)
        >>> for parent, children in result: # doctest: +SKIP
        ...     parent, tuple(sorted(children, key=lambda x: x.__name__))
        (<class '__main__.A'>, (<class '__main__.B'>, <class '__main__.F'>))
        (<class '__main__.B'>, (<class '__main__.C'>, <class '__main__.D'>))
        (<class '__main__.C'>, (<class '__main__.E'>,))
        (<class '__main__.D'>, (<class '__main__.E'>,))
        (<class '__main__.E'>, ())
        (<class '__main__.F'>, ())
        (<type 'object'>, (<class '__main__.A'>,))

    ``InheritanceGraph`` may be instantiated from one or more instances, classes or
    modules.  If instantiated from a module, all public classes in that module
    will be taken into the graph.

    A `root_class` keyword may be defined at instantiation, which filters out
    all klasses from the graph which do not inherit from that `root_class` (or
    are not already the `root_class`):

    ::

        >>> graph = InheritanceGraph(A, B, C, D, E, F, root_class=B)
        >>> for parent, children in sorted(graph.items()): # doctest: +SKIP
        ...     parent, tuple(sorted(children))
        (<class '__main__.B'>, (<class '__main__.C'>, <class '__main__.D'>))
        (<class '__main__.C'>, (<class '__main__.E'>,))
        (<class '__main__.D'>, (<class '__main__.E'>,))
        (<class '__main__.E'>, ())

    Returns ``InheritanceGraph`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_root_class')

    # TODO: what default should this take?
    #_default_mandatory_input_arguments = ()

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

    ### PUBLIC PROPERTIES ###

    @property
    def graphviz_format(self):
        result = ['digraph I {']

        def get_klass_name(klass):
            parts = klass.__module__.split('.') + [klass.__name__]
            name = [parts[0]]
            for part in parts[1:]:
                if part != name[-1]:
                    name.append(part)
            if name[0] in ('abjad', 'experimental'):
                return '.'.join(name[-2:])
            return '.'.join(name)

        for klass in self:
            name = get_klass_name(klass)
            if inspect.isabstract(klass):
                result += ['\t"{}" [shape=diamond];'.format(name)]
            else:
                result += ['\t"{}" [shape=box];'.format(name)]

        for parent, children in self.iteritems():
            for child in children:
                parent_name = get_klass_name(parent)
                child_name = get_klass_name(child)
                result += ['\t"{}" -> "{}";'.format(parent_name, child_name)]

        result += ['}']

        return '\n'.join(result)
        


    @property
    def root_class(self):
        return self._root_class
