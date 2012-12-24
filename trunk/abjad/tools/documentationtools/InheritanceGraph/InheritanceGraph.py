import importlib
import inspect
import types
from abjad.tools import abctools
from abjad.tools.datastructuretools.ImmutableDictionary import ImmutableDictionary


class InheritanceGraph(ImmutableDictionary):
    '''Generates a graph of a class or collection of 
    classes as a dictionary of parent-children relationships:

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

        >>> graph = documentationtools.InheritanceGraph((F, E))

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

        >>> graph = documentationtools.InheritanceGraph(
        ...     (A, B, C, D, E, F), root_class=B)
        >>> for parent, children in sorted(graph.items()): # doctest: +SKIP
        ...     parent, tuple(sorted(children))
        (<class '__main__.B'>, (<class '__main__.C'>, <class '__main__.D'>))
        (<class '__main__.C'>, (<class '__main__.E'>,))
        (<class '__main__.D'>, (<class '__main__.E'>,))
        (<class '__main__.E'>, ())

    Returns ``InheritanceGraph`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_addresses', '_root_class')

    # TODO: what default should this take?
    #_default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, addresses, root_class=None):

        # cache args as a tuple of strings or None in self.addresses,
        # to make _default_positional_input_arguments happy
        klasses = []
        cached_addresses = []
        assert 0 < len(addresses)
        for x in addresses:
            if isinstance(x, types.TypeType):
                klasses.append(x)
                address = (x.__module__, x.__name__)
            elif isinstance(x, types.ModuleType):
                klasses.extend(klass for klass in x.__dict__.values()
                    if isinstance(klass, types.TypeType))
                address = (x.__name__,)
            elif isinstance(x, types.InstanceType):
                klasses.append(x.__class__)
                address = (x.__class__.__module__, x.__class__.__name__)
            elif isinstance(x, tuple):
                assert len(x) in (1, 2)
                assert all(isinstance(y, str) for y in x)
                if len(x) == 1:
                    module_name, class_name = x[0], None
                else:
                    module_name, class_name = x
                module = importlib.import_module(module_name)
                if class_name:
                    klasses.append(getattr(module, class_name))
                else:
                    klasses.extend(klass for klass in module.__dict__.values()
                        if isinstance(klass, types.TypeType))
                address = x
            else:
                raise ValueError
            cached_addresses.append(address)
        self._addresses = tuple(cached_addresses)

        # cache root class as a tuple of strings or None,
        # to make _default_positional_input_arguments happy
        if isinstance(root_class, tuple):
            assert len(root_class) == 2
            assert all(isinstance(x, str) for x in root_class)
            module_name, class_name = root_class
            module = importlib.import_module(module_name)
            klass = getattr(module, class_name)
            self._root_class = root_class
            root_class = klass
        elif isinstance(root_class, types.TypeType):
            self._root_class = (root_class.__module__, root_class.__name__)
        elif isinstance(root_class, type(None)):
            self._root_class = None
        else:
            raise ValueError

        # collect klasses into a {parent: children} graph
        if root_class is None:
            graph = {}
            def recurse(klass):
                if klass not in graph:
                    graph[klass] = []
                for base in klass.__bases__:
                    if base not in graph:
                        graph[base] = []
                        recurse(base)
                    if klass not in graph[base]:
                        graph[base].append(klass)
            for klass in klasses:
                recurse(klass)
        else:
            graph = {root_class: []}
            def recurse(klass):
                if root_class in inspect.getmro(klass) and klass not in graph:      
                    graph[klass] = []
                for base in klass.__bases__:
                    if base in graph:
                        if klass not in graph[base]:
                            graph[base].append(klass)
                    elif root_class in inspect.getmro(base):
                        graph[base] = [klass]
                        recurse(base)
            for klass in klasses:
                recurse(klass)
        for parent, children in graph.iteritems():
            graph[parent] = tuple(sorted(children,
                key=lambda x: (x.__module__, x.__name__)))

        dict.__init__(self, graph)

    ### SPECIAL METHODS ###

    __repr__ = abctools.AbjadObject.__repr__

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def addresses(self):
        return self._addresses

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
            split_name = '\\n'.join(name.split('.'))
            if inspect.isabstract(klass):
                result += ['\t"{}" [shape=oval, label="{}"];'.format(name, split_name)]
            else:
                result += ['\t"{}" [shape=box, label="{}"];'.format(name, split_name)]

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
