# -*- encoding: utf-8 -*-
import importlib
import inspect
from abjad.tools.documentationtools.Documenter import Documenter


class ClassDocumenter(Documenter):
    r'''Generates an ReST API entry for a given class.

    ::

        >>> cls = documentationtools.ClassDocumenter
        >>> documenter = documentationtools.ClassDocumenter(cls)
        >>> restructured_text = documenter()

    '''

    ### CLASS VARIABLES ###

    _ignored_special_methods = (
        '__getattribute__',
        '__getnewargs__',
        '__getstate__',
        '__init__',
        '__reduce__',
        '__reduce_ex__',
        '__setstate__',
        '__sizeof__',
        '__subclasshook__',
        'fromkeys',
        'pipe_cloexec',
        )

    ### INITIALIZER ###

    def __init__(self, subject=None, prefix='abjad.tools.'):
        if subject is None:
            subject = type(None)
        assert isinstance(subject, type)
        Documenter.__init__(self, subject, prefix)
        class_methods = []
        data = []
        inherited_attributes = []
        methods = []
        readonly_properties = []
        readwrite_properties = []
        special_methods = []
        static_methods = []
        attrs = inspect.classify_class_attrs(self.subject)
        for attr in attrs:
            if attr.defining_class is object:
                continue
            if self._attribute_is_inherited(attr):
                inherited_attributes.append(attr)
            if attr.kind == 'method':
                if attr.name not in self._ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        methods.append(attr)
            elif attr.kind == 'class method':
                if attr.name not in self._ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        class_methods.append(attr)
            elif attr.kind == 'static method':
                if attr.name not in self._ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        static_methods.append(attr)
            elif attr.kind == 'property' and not attr.name.startswith('_'):
                if attr.object.fset is None:
                    readonly_properties.append(attr)
                else:
                    readwrite_properties.append(attr)
            elif attr.kind == 'data' and not attr.name.startswith('_') \
                and attr.name not in getattr(self.subject, '__slots__', ()):
                data.append(attr)
        self._class_methods = tuple(sorted(class_methods))
        self._data = tuple(sorted(data))
        self._inherited_attributes = tuple(sorted(inherited_attributes))
        self._methods = tuple(sorted(methods))
        self._readonly_properties = tuple(sorted(readonly_properties))
        self._readwrite_properties = tuple(sorted(readwrite_properties))
        self._special_methods = tuple(sorted(special_methods))
        self._static_methods = tuple(sorted(static_methods))

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls class documenter.

        Generates documentation.

        Returns string.
        '''
        from abjad.tools import documentationtools

        stripped_class_name = self._shrink_module_name(self.subject.__module__)
        parts = self.subject.__module__.split('.')
        tools_package_path = '.'.join(parts[:3])
        tools_package_name, sep, class_name = stripped_class_name.partition('.')
        banner = '{}.{}'.format(tools_package_name, class_name)
#        banner = ':py:mod:`{} <{}>`.{}'.format(
#            tools_package_name,
#            tools_package_path,
#            class_name,
#            )
        document = documentationtools.ReSTDocument()
        document.append(documentationtools.ReSTHeading(
            level=2,
            text=banner,
            ))
#        document.append(documentationtools.ReSTLineageDirective(
#            argument=self.module_name,
#            ))
        document.append(documentationtools.ReSTAutodocDirective(
            argument=self.module_name,
            directive='autoclass',
            options={
                #'noindex': True,
                },
            ))

        lineage_heading = documentationtools.ReSTHeading(
            level=3,
            text='Lineage',
            )
        document.append(lineage_heading)
        lineage_graph = self._build_lineage_graph(self.subject)
        lineage_graph.attributes['background'] = 'transparent'
        lineage_graph.attributes['rankdir'] = 'LR'
        graphviz_directive = documentationtools.GraphvizDirective(
            graph=lineage_graph,
            )
        document.append(graphviz_directive)

        document.extend(self._build_attributes_autosummary())
        document.extend(self._build_bases_section())
#        document.extend(self._build_attribute_section(
#            self.data,
#            'Class variables',
#            'autodata',
#            ))
        document.extend(self._build_attribute_section(
            self.readonly_properties,
            'Read-only properties',
            'autoattribute',
            ))
        document.extend(self._build_attribute_section(
            self.readwrite_properties,
            'Read/write properties',
            'autoattribute',
            ))
        document.extend(self._build_attribute_section(
            self.methods,
            'Methods',
            'automethod',
            ))
        document.extend(self._build_attribute_section(
            self.class_methods,
            'Class methods',
            'automethod',
            ))
        document.extend(self._build_attribute_section(
            self.static_methods,
            'Static methods',
            'automethod',
            ))
        document.extend(self._build_attribute_section(
            self.special_methods,
            'Special methods',
            'automethod',
            ))
        return document.rest_format

    ### PRIVATE METHODS ###

    def _attribute_is_inherited(self, attr):
        if attr.defining_class is not self.subject:
            return True
        return False

    def _build_attribute_section(self, attrs, title, directive):
        from abjad.tools import documentationtools
        result = []
        if attrs:
            result.append(documentationtools.ReSTHeading(
                level=3,
                text=title,
                ))
            for attr in attrs:
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(
                        self.module_name,
                        attr.name,
                        ),
                    directive=directive,
                    options={
                        'noindex': True,
                        },
                    )
                result.append(autodoc)
        return result

    def _build_attributes_autosummary(self):
        from abjad.tools import documentationtools
        pieces = []
        attributes = []
        attributes.extend(self.readonly_properties)
        attributes.extend(self.readwrite_properties)
        attributes.extend(self.methods)
        attributes.extend(self.class_methods)
        attributes.extend(self.static_methods)
        attributes.sort(key=lambda x: x.name)
        attributes.extend(self.special_methods)
        autosummary = documentationtools.ReSTAutosummaryDirective()
        for attribute in attributes:
            autosummary.append('~{}.{}'.format(
                self.module_name,
                attribute.name,
                ))
        html_only = documentationtools.ReSTOnlyDirective(argument='html')
        html_only.append(documentationtools.ReSTHeading(
            level=3,
            text='Attribute summary',
            ))
        html_only.append(autosummary)
        pieces.append(html_only)
        return pieces

    def _build_bases_section(self):
        from abjad.tools import documentationtools
        pieces = []
        pieces.append(documentationtools.ReSTHeading(
            level=3,
            text='Bases',
            ))
        mro = inspect.getmro(self.subject)[1:]
        for cls in mro:
            packagesystem_path = '.'.join((cls.__module__, cls.__name__))
            stripped_packagesystem_path = self._shrink_module_name(
                packagesystem_path)
            if packagesystem_path.startswith('__builtin__'):
                packagesystem_path = \
                    packagesystem_path.partition('__builtin__.')[-1]
            text = '- :py:class:`{} <{}>`'.format(
                stripped_packagesystem_path,
                packagesystem_path,
                )
            paragraph = documentationtools.ReSTParagraph(
                text=text,
                wrap=False,
                )
            pieces.append(paragraph)
        return pieces

    @staticmethod
    def _build_lineage_graph(cls):
        from abjad.tools import documentationtools
        addresses = ['abjad']
        try:
            import experimental
            addresses.append('experimental')
        except ImportError:
            pass
        try:
            import ide
            addresses.append('ide')
        except ImportError:
            pass
        module_name, _, class_name = cls.__module__.rpartition('.')
        importlib.import_module(module_name)
        lineage = documentationtools.InheritanceGraph(
            addresses=addresses,
            lineage_addresses=((module_name, class_name),)
            )
        graph = lineage.__graph__()
        maximum_node_count = 30
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=2,
                )
            graph = lineage.__graph__()
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=1,
                )
            graph = lineage.__graph__()
        node_name = ClassDocumenter._get_node_name(
            module_name + '.' + class_name)
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=((module_name, class_name),),
                )
            graph = lineage.__graph__()
            graph_node = graph[node_name]
            graph_node.attributes['color'] = 'black'
            graph_node.attributes['fontcolor'] = 'white'
            graph_node.attributes['style'] = ('filled', 'rounded')
        graph_node = graph[node_name]
        graph_node.attributes['label'] = \
            '<<B>{}</B>>'.format(graph_node.attributes['label'])
        return graph

    @staticmethod
    def _get_node_name(original_name):
        parts = original_name.split('.')
        name = [parts[0]]
        for part in parts[1:]:
            if part != name[-1]:
                name.append(part)
        if name[0] in ('abjad', 'experimental', 'ide') and \
            name[1] in ('tools',):
            return str('.'.join(name[2:]))
        return str('.'.join(name))

    ### PUBLIC PROPERTIES ###

    @property
    def class_methods(self):
        r'''Class methods.
        '''
        return self._class_methods

    @property
    def data(self):
        r'''Data.
        '''
        return self._data

    @property
    def inherited_attributes(self):
        r'''Inherited attributes.
        '''
        return self._inherited_attributes

    @property
    def is_abstract(self):
        r'''Is true when class is abstract. Otherwise false.

        Returns boolean.
        '''
        return inspect.isabstract(self.subject)

    @property
    def methods(self):
        r'''Methods of class.
        '''
        return self._methods

    @property
    def readonly_properties(self):
        r'''Read-only properties of class.
        '''
        return self._readonly_properties

    @property
    def readwrite_properties(self):
        r'''The read / write properties of class.
        '''
        return self._readwrite_properties

    @property
    def special_methods(self):
        r'''Special methods of class.
        '''
        return self._special_methods

    @property
    def static_methods(self):
        r'''Static methods of class.
        '''
        return self._static_methods