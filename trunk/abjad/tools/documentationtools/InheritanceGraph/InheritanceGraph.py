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
        '_child_parents_mapping',
        '_immediate_klasses',
        '_lineage_addresses',
        '_lineage_klasses',
        '_parent_children_mapping',
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

        # main addresses
        if addresses is None:
            addresses = ('abjad',)
        all_main_klasses, main_immediate_klasses, main_cached_addresses = \
            self._collect_klasses(addresses, self.recurse_into_submodules)
        self._addresses = main_cached_addresses

        # lineage addresses
        if lineage_addresses is not None: 
            all_lineage_klasses, lineage_immediate_klasses, lineage_cached_addresses = \
                self._collect_klasses(lineage_addresses, False)
            self._lineage_addresses = lineage_cached_addresses
            self._lineage_klasses = frozenset(all_lineage_klasses)
        else:
            self._lineage_addresses = None
            self._lineage_klasses = frozenset([])

        # root addresses
        if root_addresses is not None:
            all_root_klasses, root_immediate_klasses, root_cached_addresses = \
                self._collect_klasses(root_addresses, False)
            self._root_addresses = root_cached_addresses
            self._root_klasses = frozenset(all_root_klasses)
        else:
            self._root_addresses = None
            self._root_klasses = frozenset([object])

        child_parents_mapping, parent_children_mapping = self._build_basic_mappings(all_main_klasses)
        self._strip_nonlineage_klasses(child_parents_mapping, parent_children_mapping)

        self._child_parents_mapping = child_parents_mapping
        self._parent_children_mapping = parent_children_mapping

    ### PRIVATE METHODS ###

    def _build_basic_mappings(self, klasses):
        child_parents_mapping = {}
        parent_children_mapping = {}
        invalid_klasses = set([])
        def recurse(klass):
            if klass in child_parents_mapping:
                return True
            elif klass in invalid_klasses:
                return False
            mro = list(inspect.getmro(klass))
            while len(mro) and mro[-1] not in self.root_klasses:
                mro.pop()
            if not mro:
                invalid_klasses.add(klass)
                return False
            parents = [x for x in klass.__bases__ if recurse(x)]
            child_parents_mapping[klass] = set(parents)
            parent_children_mapping[klass] = set([])
            for parent in parents:
                parent_children_mapping[parent].add(klass)
            return True
        for klass in klasses:
            recurse(klass)        
        return child_parents_mapping, parent_children_mapping

    def _collect_klasses(self, addresses, recurse_into_submodules):
        all_klasses = set([])
        cached_addresses = []
        immediate_klasses = set([])
        visited_modules = set([])
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
                        all_klasses.update(self._submodule_recurse(y, visited_modules))
                address = module.__name__
            cached_addresses.append(address)
        return all_klasses, immediate_klasses, tuple(cached_addresses)

    def _strip_nonlineage_klasses(self, child_parents_mapping, parent_children_mapping):
        if not self.lineage_klasses:
            return
        def recurse_upward(klass, invalid_klasses):
            for parent in child_parents_mapping[klass]:
                if parent in invalid_klasses:
                    invalid_klasses.remove(parent)
                    recurse_upward(parent, invalid_klasses)

        def recurse_downward(klass, invalid_klasses):
            for child in parent_children_mapping[klass]:
                if child in invalid_klasses:
                    invalid_klasses.remove(child)
                    recurse_downward(child, invalid_klasses)
        invalid_klasses = set(child_parents_mapping.keys() + parent_children_mapping.keys())
        for klass in self.lineage_klasses:
            recurse_upward(klass, invalid_klasses)
            recurse_downward(klass, invalid_klasses)
        for klass in invalid_klasses:
            for child in parent_children_mapping[klass]:
                child_parents_mapping[child].remove(klass)
            for parent in child_parents_mapping[klass]:
                parent_children_mapping[parent].remove(klass)
            del(parent_children_mapping[klass])
            del(child_parents_mapping[klass]) 

    def _submodule_recurse(self, module, visited_modules):
        result = []
        for obj in module.__dict__.values():
            if isinstance(obj, types.TypeType):
                result.append(obj)
            elif isinstance(obj, types.ModuleType) and obj not in visited_modules:
                visited_modules.add(obj)
                result.extend(self._submodule_recurse(obj, visited_modules))
        return result 

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def addresses(self):
        return self._addresses

    @property
    def child_parents_mapping(self):
        return self._child_parents_mapping

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
    def lineage_addresses(self):
        return self._lineage_addresses

    @property
    def lineage_klasses(self):
        return self._lineage_klasses

    @property
    def parent_children_mapping(self):
        return self._parent_children_mapping

    @property
    def recurse_into_submodules(self):
        return self._recurse_into_submodules

    @property
    def root_addresses(self):
        return self._root_addresses

    @property
    def root_klasses(self):
        return self._root_klasses
