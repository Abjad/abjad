import abc
from abjad.tools.documentationtools.Documenter import Documenter
import inspect


class ClassDocumenter(Documenter):
    '''ClassDocumenter generates an ReST API entry for a given class:

    ::

        >>> from abjad.tools import notetools
        >>> from abjad.tools.documentationtools import ClassDocumenter
    
    ::

        >>> documenter = ClassDocumenter(notetools.Note)
        >>> rest = documenter()

    Returns ``ClassDocumenter`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    _ignored_special_methods = (
        '__copy__', '__deepcopy__', '__format__', '__getattribute__',
        '__getnewargs__', '__init__', '__reduce__', '__reduce_ex__', 
        '__sizeof__', '__subclasshook__', 'fromkeys', 'pipe_cloexec',
    )

    __slots__ = ('_data', '_inherited_attributes', 
        '_methods', '_object', '_prefix', '_readonly_properties', 
        '_readwrite_properties', '_special_methods')

    ### INITIALIZER ###

    def __init__(self, obj, prefix='abjad.tools.'):
        assert isinstance(obj, type)
        Documenter.__init__(self, obj, prefix)

        data = []
        inherited_attributes = []
        methods = []
        readonly_properties = []
        readwrite_properties = []
        special_methods = []

        attrs = inspect.classify_class_attrs(self._object)
        for attr in attrs:
            if attr.defining_class is object:
                continue
            if self._attribute_is_inherited(attr):
                inherited_attributes.append(attr)
            if attr.kind in ('class method', 'method'):
                if attr.name not in self._ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        methods.append(attr)
            elif attr.kind == 'property' and not attr.name.startswith('_'):
                if attr.object.fset is None:
                    readonly_properties.append(attr)
                else:
                    readwrite_properties.append(attr)
            elif attr.kind == 'data' and not attr.name.startswith('_'):
                data.append(attr)

        self._data = tuple(sorted(data))
        self._inherited_attributes = tuple(sorted(inherited_attributes))
        self._methods = tuple(sorted(methods))
        self._readonly_properties = tuple(sorted(readonly_properties))
        self._readwrite_properties = tuple(sorted(readwrite_properties))
        self._special_methods = tuple(sorted(special_methods))

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Generate documentation.

        Returns string.
        '''

        stripped_class_name = self._shrink_module_name(self.object.__module__)
        module_name = '%s.%s' % (self.object.__module__, self.object.__name__)

        result = []
        result.extend(self._format_heading(stripped_class_name, '='))
        result.extend(self._format_inheritance_diagram())
        result.append('.. autoclass:: %s' % module_name)
        result.append('')

        if self.readonly_properties:
            result.extend(self._format_heading('Read-only Properties', '-'))
            for attr in self.readonly_properties:
                result.extend(self._format_attribute(attr, 'attribute'))

        if self.readwrite_properties:
            result.extend(self._format_heading('Read/write Properties', '-'))
            for attr in self.readwrite_properties:
                result.extend(self._format_attribute(attr, 'attribute'))

        if self.methods:
            result.extend(self._format_heading('Methods', '-'))
            for attr in self.methods:
                result.extend(self._format_attribute(attr, 'method'))

        if self.special_methods:
            result.extend(self._format_heading('Special Methods', '-'))
            for attr in self.special_methods:
                result.extend(self._format_attribute(attr, 'method'))

        return '\n'.join(result)

    ### PRIVATE METHODS ###

    def _attribute_is_inherited(self, attr):
        if attr.defining_class is not self._object:
            return True
        return False

    def _format_attribute(self, attr, kind):
        module_name = '%s.%s' % (self._object.__module__, self._object.__name__)
        result = []
        result.append('.. auto%s:: %s.%s' % (kind, module_name, attr.name))
        result.append('')
        if attr in self.inherited_attributes:
            defining_module = '%s.%s' % (attr.defining_class.__module__, attr.defining_class.__name__)
            if defining_module.startswith(('abjad', 'experimental')):
                parts = defining_module.split('.')
                result.append('    Inherited from :py:class:`%s.%s <%s>`' %
                    (parts[2], parts[3], defining_module))
            elif defining_module.startswith('experimental'):
                parts = defining_module.split('.')
                result.append('    Inherited from :py:class:`%s.%s <%s>`' %
                    (parts[1], parts[2], defining_module))
            else:
                result.append('    Inherited from :py:class:`%s`' % defining_module)
            result.append('')
        return result

    def _format_inheritance_diagram(self):
        module_name = '%s.%s' % (self._object.__module__, self._object.__name__)
        return [
            '.. inheritance-diagram:: %s' % module_name,
            '   :private-bases:',
            '',
        ]

    ### PUBLIC PROPERTIES ###

    @property
    def data(self):
        return self._data

    @property
    def inherited_attributes(self):
        return self._inherited_attributes

    @property
    def is_abstract(self):
        return inspect.isabstract(self.object)

    @property
    def methods(self):
        return self._methods

    @property
    def readonly_properties(self):
        return self._readonly_properties

    @property
    def readwrite_properties(self):
        return self._readwrite_properties

    @property
    def special_methods(self):
        return self._special_methods

