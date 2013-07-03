import importlib
import inspect
import types
from abjad.tools.abctools.AbjadObject import AbjadObject


class InheritanceGraph(AbjadObject):
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

        >>> graph = documentationtools.InheritanceGraph(addresses=(F, E))

    ``InheritanceGraph`` may be instantiated from one or more instances, 
    classes or modules. If instantiated from a module, all public classes 
    in that module will be taken into the graph.

    A `root_class` keyword may be defined at instantiation, which filters out
    all classes from the graph which do not inherit from that `root_class`
    (or are not already the `root_class`):

    ::

        >>> graph = documentationtools.InheritanceGraph(
        ...     (A, B, C, D, E, F), root_addresses=(B,))

    The class is intended for use in documenting packages.

    To document all of Abjad, use this formulation:

    ::

        >>> graph = documentationtools.InheritanceGraph(
        ...     addresses=('abjad',))

    To document only those classes descending from Container, 
    use this formulation:

    ::

        >>> graph = documentationtools.InheritanceGraph(
        ...     addresses=('abjad',),
        ...     root_addresses=(Container,)
        ...     )

    To document only those classes whose lineage pass through componenttools,
    use this formulation:

    ::

        >>> graph = documentationtools.InheritanceGraph(
        ...     addresses=('abjad',),
        ...     lineage_addresses=(componenttools,),
        ...     )

    When creating the Graphviz representation, classes in the inheritance 
    graph may be hidden, based on their distance from any defined lineage 
    class:

    ::

        >>> graph = documentationtools.InheritanceGraph(
        ...     addresses=('abjad',),
        ...     lineage_addresses=(marktools.Mark,),
        ...     lineage_prune_distance=1,
        ...     )

    Returns ``InheritanceGraph`` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_addresses',
        '_child_parents_mapping',
        '_immediate_classes',
        '_lineage_addresses',
        '_lineage_classes',
        '_lineage_distance_mapping',
        '_lineage_prune_distance',
        '_parent_children_mapping',
        '_recurse_into_submodules',
        '_root_addresses',
        '_root_classes',
        '_use_clusters',
        '_use_groups',
        )

    # TODO: what default should this take?
    #_default_positional_input_arguments = ()

    ### INITIALIZER ###

    def __init__(self,
        addresses=('abjad',),
        lineage_addresses=None,
        lineage_prune_distance=None,
        recurse_into_submodules=True,
        root_addresses=None,
        use_clusters=True,
        use_groups=True,
        ):

        self._recurse_into_submodules = bool(recurse_into_submodules)
        if lineage_prune_distance is not None:
            lineage_prune_distance = int(lineage_prune_distance)
            assert 0 < lineage_prune_distance
        self._lineage_prune_distance = lineage_prune_distance
        self._use_clusters = bool(use_clusters)
        self._use_groups = bool(use_groups)

        # main addresses
        if addresses is None:
            addresses = ('abjad',)
        for i, x in enumerate(addresses):
            if isinstance(x, unicode):
                addresses[i] = str(x)
        all_main_classes, main_immediate_classes, main_cached_addresses = \
            self._collect_classes(addresses, self.recurse_into_submodules)
        self._addresses = main_cached_addresses

        # lineage addresses
        if lineage_addresses is not None:
            all_lineage_classes, lineage_immediate_classes, lineage_cached_addresses = \
                self._collect_classes(lineage_addresses, False)
            self._lineage_addresses = lineage_cached_addresses
            self._lineage_classes = frozenset(all_lineage_classes)
        else:
            self._lineage_addresses = None
            self._lineage_classes = frozenset([])

        # root addresses
        if root_addresses is not None:
            all_root_classes, root_immediate_classes, root_cached_addresses = \
                self._collect_classes(root_addresses, False)
            self._root_addresses = root_cached_addresses
            self._root_classes = frozenset(all_root_classes)
        else:
            self._root_addresses = None
            self._root_classes = frozenset([object])

        child_parents_mapping, parent_children_mapping = \
            self._build_basic_mappings(all_main_classes)
        self._strip_nonlineage_classes(
            child_parents_mapping, parent_children_mapping)

        self._child_parents_mapping = child_parents_mapping
        self._parent_children_mapping = parent_children_mapping

        self._immediate_classes = main_immediate_classes.intersection(
            self._parent_children_mapping.viewkeys())

        self._lineage_distance_mapping = self._find_lineage_distances()

    ### PRIVATE METHODS ###

    def _build_basic_mappings(self, classes):
        child_parents_mapping = {}
        parent_children_mapping = {}
        invalid_classes = set([])
        def recurse(klass):
            if klass in child_parents_mapping:
                return True
            elif klass in invalid_classes:
                return False
            mro = list(inspect.getmro(klass))
            while len(mro) and mro[-1] not in self.root_classes:
                mro.pop()
            if not mro:
                invalid_classes.add(klass)
                return False
            parents = [x for x in klass.__bases__ if recurse(x)]
            child_parents_mapping[klass] = set(parents)
            parent_children_mapping[klass] = set([])
            for parent in parents:
                parent_children_mapping[parent].add(klass)
            return True
        for klass in classes:
            recurse(klass)
        return child_parents_mapping, parent_children_mapping

    def _collect_classes(self, addresses, recurse_into_submodules):
        all_classes = set([])
        cached_addresses = []
        immediate_classes = set([])
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
                all_classes.add(klass)
                immediate_classes.add(klass)
                address = (klass.__module__, klass.__name__)
            elif isinstance(x, (str, types.ModuleType)):
                if isinstance(x, types.ModuleType):
                    module = x
                else:
                    module = importlib.import_module(x)
                for y in module.__dict__.itervalues():
                    if isinstance(y, types.TypeType):
                        all_classes.add(y)
                        immediate_classes.add(y)
                    elif isinstance(y, types.ModuleType) and \
                        recurse_into_submodules:
                        all_classes.update(
                            self._submodule_recurse(y, visited_modules))
                address = module.__name__
            cached_addresses.append(address)
        return all_classes, immediate_classes, tuple(cached_addresses)

    def _find_lineage_distances(self):
        if not self.lineage_classes:
            return None
        if not self.lineage_prune_distance:
            return None
        distance_mapping = {}
        def recurse_downward(klass, distance=0):
            if klass not in self.parent_children_mapping:
                return
            for child in self.parent_children_mapping[klass]:
                if child not in distance_mapping:
                    distance_mapping[child] = distance + 1
                    recurse_downward(child, distance + 1)
                elif (distance + 1) < distance_mapping[child]:
                    distance_mapping[child] = distance + 1
                    recurse_downward(child, distance + 1)
        for klass in self.lineage_classes:
            recurse_downward(klass)
        return distance_mapping

    def _strip_nonlineage_classes(self, 
        child_parents_mapping, parent_children_mapping):
        if not self.lineage_classes:
            return
        def recurse_upward(klass, invalid_classes):
            if klass not in child_parents_mapping:
                return
            for parent in child_parents_mapping[klass]:
                if parent in invalid_classes:
                    invalid_classes.remove(parent)
                    recurse_upward(parent, invalid_classes)
        def recurse_downward(klass, invalid_classes):
            if klass not in parent_children_mapping:
                return
            for child in parent_children_mapping[klass]:
                if child in invalid_classes:
                    invalid_classes.remove(child)
                    recurse_downward(child, invalid_classes)
        invalid_classes = set(
            child_parents_mapping.keys() + parent_children_mapping.keys())
        for klass in self.lineage_classes:
            if klass in invalid_classes:
                invalid_classes.remove(klass)
            recurse_upward(klass, invalid_classes)
            recurse_downward(klass, invalid_classes)
        for klass in invalid_classes:
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
            elif isinstance(obj, types.ModuleType) and \
                obj not in visited_modules:
                visited_modules.add(obj)
                result.extend(self._submodule_recurse(obj, visited_modules))
        return result

    ### PUBLIC PROPERTIES ###

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
        from abjad.tools import documentationtools

        def get_class_name_pieces(klass):
            parts = (klass.__module__ + '.' + klass.__name__).split('.')
            name = [parts[0]]
            for part in parts[1:]:
                if part != name[-1]:
                    name.append(part)
            if name[0] in ('abjad', 'experimental'):
                return name[2:]
            return name

        class_nodes = {}

        graph = documentationtools.GraphvizGraph(
            name='InheritanceGraph',
            attributes={
                'color': 'lightslategrey',
                'fontname': 'Arial',
                'overlap': 'prism',
                'penwidth': 2,
                #'ranksep': 0.5,
                'splines': 'spline',
                'style': ('dotted', 'rounded'),
            },
            edge_attributes={
                'penwidth': 2,
            },
            node_attributes={
                'colorscheme': 'pastel19',
                'fontname': 'Arial',
                'fontsize': 12,
                'penwidth': 2,
                'style': ('filled', 'rounded'),
            },
            )

        for klass in sorted(self.parent_children_mapping,
            key=lambda x: (x.__module__, x.__name__)):
            pieces = get_class_name_pieces(klass)

            try:
                cluster = graph[pieces[0]]
            except KeyError:
                cluster = documentationtools.GraphvizSubgraph(
                    name=pieces[0],
                    attributes={
                        'label': pieces[0],
                    },
                    )
                graph.append(cluster)

            node = documentationtools.GraphvizNode(
                name='.'.join(pieces),
                )
            node.attributes['label'] = '\\n'.join(pieces)

            if klass in self.immediate_classes:
                pass
            if klass in self.root_classes:
                pass
            if inspect.isabstract(klass):
                node.attributes['shape'] = 'oval'
                node.attributes['style'] = 'bold'
            else:
                node.attributes['shape'] = 'box'
            if klass in self.lineage_classes:
                node.attributes['color'] = 'black'
                node.attributes['fontcolor'] = 'white'
                node.attributes['style'] = ('filled', 'rounded')

            if self.lineage_prune_distance is None:
                cluster.append(node)
                class_nodes[klass] = node
            elif klass not in self.lineage_distance_mapping:
                cluster.append(node)
                class_nodes[klass] = node
            else:
                ok_distance = self.lineage_prune_distance + 1
                distance = self.lineage_distance_mapping[klass]
                if distance < ok_distance:
                    cluster.append(node)
                    class_nodes[klass] = node
                elif distance == ok_distance:
                    node.attributes['shape'] = 'invis'
                    node.attributes['style'] = 'transparent'
                    node.attributes['label'] = ' '
                    cluster.append(node)
                    class_nodes[klass] = node
                elif ok_distance < distance:
                    pass

        distances = self.lineage_distance_mapping
        for parent, children in self.parent_children_mapping.iteritems():
            for child in children:
                ok_to_join = False
                if self.lineage_prune_distance is None:
                    ok_to_join = True
                elif parent not in distances:
                    if child not in distances:
                        ok_to_join = True
                    elif child in distances and \
                        distances[child] <= ok_distance:
                        ok_to_join = True
                elif child not in distances:
                    if parent not in distances:
                        ok_to_join = True
                    elif parent in distances and \
                        distances[parent] <= ok_distance:
                        ok_to_join = True
                elif distances[child] <= ok_distance and \
                    distances[parent] <= ok_distance:
                    ok_to_join = True
                if ok_to_join:
                    parent_node = class_nodes[parent]
                    child_node = class_nodes[child]
                    documentationtools.GraphvizEdge()(parent_node, child_node)

        for i, cluster in enumerate(
            sorted(graph.children, key=lambda x: x.name)):
            color = i % 9 + 1
            for node in cluster:
                if 'color' not in node.attributes:
                    node.attributes['color'] = color
                if self.use_groups:
                    node.attributes['group'] = i
            if not self.use_clusters:
                graph.extend(cluster[:])
                graph.remove(cluster)

        if self.root_addresses is None:
            graph.attributes['root'] = '__builtin__.object'

        return graph

    @property
    def immediate_classes(self):
        return self._immediate_classes

    @property
    def lineage_addresses(self):
        return self._lineage_addresses

    @property
    def lineage_distance_mapping(self):
        return self._lineage_distance_mapping

    @property
    def lineage_classes(self):
        return self._lineage_classes

    @property
    def lineage_prune_distance(self):
        return self._lineage_prune_distance

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
    def root_classes(self):
        return self._root_classes

    @property
    def use_clusters(self):
        return self._use_clusters

    @property
    def use_groups(self):
        return self._use_groups
