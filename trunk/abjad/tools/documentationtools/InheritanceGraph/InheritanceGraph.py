import importlib
import inspect
import types
from abjad.tools.abctools.AbjadObject import AbjadObject


class InheritanceGraph(AbjadObject):
    '''Generates a graph of a class or collection of 
    klasses as a dictionary of parent-children relationships:

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

        >>> graph = documentationtools.InheritanceGraph(addresses=(F, E))

    ``InheritanceGraph`` may be instantiated from one or more instances, klasses or
    modules.  If instantiated from a module, all public klasses in that module
    will be taken into the graph.

    A `root_class` keyword may be defined at instantiation, which filters out
    all klasses from the graph which do not inherit from that `root_class` (or
    are not already the `root_class`):

    ::

        >>> graph = documentationtools.InheritanceGraph(
        ...     (A, B, C, D, E, F), root_addresses=(B,))

    Returns ``InheritanceGraph`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_addresses',
        '_class_lookup',
        '_immediate_klasses',
        '_inheritance_graph',
        '_lineage_addresses',
        '_lineage_klasses',
        '_recurse_into_submodules',
        '_root_addresses',
        '_root_klasses'
        )

    # TODO: what default should this take?
    #_default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self,
        addresses=('abjad',),
        lineage_addresses=None,
        recurse_into_submodules=True,
        root_addresses=None,
        ):

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

        def collect_klasses(addresses, recurse_into_submodules):
            all_klasses = set([])
            immediate_klasses = set([])
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
                    all_klasses.add(klass)
                    immediate_klasses.add(klass)
                    address = (klass.__module__, klass.__name__)
                elif isinstance(x, (str, types.ModuleType)):
                    if isinstance(x, types.ModuleType):
                        module = x
                    else:
                        module = importlib.import_module(x)
                    for y in module.__dict__.itervalues():
                        if isinstance(y, types.TypeType):
                            all_klasses.add(y)
                            immediate_klasses.add(y)
                        elif isinstance(y, types.ModuleType) and recurse_into_submodules:
                            all_klasses.update(submodule_recurse(y))
                    address = module.__name__
                cached_addresses.append(address)
            return all_klasses, immediate_klasses, tuple(cached_addresses)

        # main addresses
        if addresses is None:
            addresses = ('abjad',)
        main_all_klasses, main_immediate_klasses, main_cached_addresses = \
            collect_klasses(addresses, self.recurse_into_submodules)
        self._addresses = main_cached_addresses

        # lineage addresses
        if lineage_addresses is not None: 
            lineage_all_klasses, lineage_immediate_klasses, lineage_cached_addresses = \
                collect_klasses(lineage_addresses, False)
            self._lineage_addresses = lineage_cached_addresses
        else:
            self._lineage_addresses = None

        # root addresses
        if root_addresses is not None:
            root_all_klasses, root_immediate_klasses, root_cached_addresses = \
                collect_klasses(root_addresses, False)
            self._root_addresses = root_cached_addresses
        else:
            self._root_addresses = None

        # inspect.getmro()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def addresses(self):
        return self._addresses

    @property
    def class_lookup(self):
        return self._class_lookup

    @property
    def graphviz_format(self):
        return self.graphviz_graph.graphviz_format        

    @property
    def graphviz_graph(self):

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

        raise NotImplemented

    @property
    def immediate_klasses(self):
        return self._immediate_klasses

    @property
    def inheritance_graph(self):
        return self._inheritance_graph

    @property
    def lineage_addresses(self):
        return self._lineage_addresses

    @property
    def lineage_klasses(self):
        return self._lineage_klasses

    @property
    def recurse_into_submodules(self):
        return self._recurse_into_submodules

    @property
    def root_addresses(self):
        return self._root_addresses

    @property
    def root_klasses(self):
        return self._root_klasses
