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

    __slots__ = ('_addresses', '_primary_classes', '_recurse_into_submodules',
        '_root_class')

    # TODO: what default should this take?
    #_default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self, addresses, recurse_into_submodules=True, root_class=None):

        self._recurse_into_submodules = bool(recurse_into_submodules)

        visited_modules = set([])
        def submodule_recurse(module):
            result = []
            for obj in module.__dict__.values():
                if isinstance(obj, types.TypeType):
                    result.append(obj)
                elif isinstance(obj, types.ModuleType) and obj not in visited_modules:
                    visited_modules.add(obj)
                    result.extend(submodule_recurse(obj))
            return result 

        # cache args as a tuple of strings or None in self.addresses,
        # to make _default_positional_input_arguments happy
        klasses = []
        primary_classes = set([])
        cached_addresses = []
        assert 0 < len(addresses)
        for x in addresses:
            if isinstance(x, (types.TypeType, types.InstanceType)) or \
                (isinstance(x, tuple) and len(x) == 2):

                if isinstance(x, types.TypeType):
                    klass = x
                elif isinstance(x, types.InstanceType):
                    klass = x.__class__        
                else:
                    module_name, class_name = x
                    module = importlib.import_module(module_name)
                    klass = getattr(module, class_name)
                klasses.append(klass)
                primary_classes.add(klass)
                address = (klass.__module__, klass.__name__)

            elif isinstance(x, (str, types.ModuleType)):
                if isinstance(x, types.ModuleType):
                    module = x
                else:
                    module = importlib.import_module(x)
                for y in module.__dict__.itervalues():
                    if isinstance(y, types.TypeType):
                        klasses.append(y)
                        primary_classes.add(y)
                    elif isinstance(y, types.ModuleType) and self.recurse_into_submodules:
                        klasses.extend(submodule_recurse(y))
                address = module.__name__
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
            primary_classes.add(root_class)
        elif isinstance(root_class, types.TypeType):
            self._root_class = (root_class.__module__, root_class.__name__)
            primary_classes.add(root_class)
        elif isinstance(root_class, type(None)):
            self._root_class = None
        else:
            raise ValueError

        self._primary_classes = frozenset(primary_classes)

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

        def make_unique(name):
            parts = name.split('.')
            name = [parts[0]]
            for part in parts[1:]:
                if part != name[-1]:
                    name.append(part)
            if name[0] in ('abjad', 'experimental'):
                return '.'.join(name[2:])
            return '.'.join(name)

        def get_klass_name(klass):
            return make_unique(klass.__module__ + '.' + klass.__name__)

        if self.root_class is None:
            root = '__builtin__.object'
        else:
            root = make_unique('.'.join(self.root_class))
        result += ['\tgraph [ranksep=3, root="{}"]'.format(root)]

        for klass in sorted(self, key=lambda x: (x.__module__, x.__name__)):
            name = get_klass_name(klass)
            label = '\\n'.join(name.split('.'))
            # abstract / concrete
            if inspect.isabstract(klass):
                shape = 'oval'
            else:
                shape = 'box'
            # primary
            if klass in self.primary_classes:
                style = 'bold'
            else:
                style = 'dashed'
            # root package
            #if klass.__module__.startswith('abjad.'):
            #    color = 'blue'
            #elif klass.__module__.startswith('experimental.'):
            #    color = 'red'
            #else:
            #    color = 'black'
            #result += ['\t"{}" [shape={}, label="{}", style={}, color={}, fontcolor={}];'.format(
            #    name, shape, label, style, color, color)]
            result += ['\t"{}" [shape={}, label="{}", style={}];'.format(
                name, shape, label, style)]

        for parent in sorted(self, key=lambda x: (x.__module__, x.__name__)):
            children = sorted(self[parent], key=lambda x: (x.__module__, x.__name__))
            for child in children:
                parent_name = get_klass_name(parent)
                child_name = get_klass_name(child)
                #if child.__module__.startswith('abjad.'):
                #    color = 'blue'
                #elif child.__module__.startswith('experimental.'):
                #    color = 'red'
                #else:
                #    color = 'black'
                #result += ['\t"{}" -> "{}" [color={}];'.format(parent_name, child_name, color)]
                result += ['\t"{}" -> "{}";'.format(parent_name, child_name)]

        result += ['}']

        return '\n'.join(result)
        
    @property
    def primary_classes(self):
        return self._primary_classes

    @property
    def recurse_into_submodules(self):
        return self._recurse_into_submodules

    @property
    def root_class(self):
        return self._root_class
