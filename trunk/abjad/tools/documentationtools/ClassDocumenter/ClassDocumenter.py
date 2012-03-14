import inspect
from abjad.tools.abctools import AbjadObject


class ClassDocumenter(AbjadObject):
    '''ClassDocumenter generates an ReST API entry for a given class:

    ::

        abjad> from abjad import Note
        abjad> from abjad.tools.documentationtools import ClassDocumenter
    
    ::

        abjad> documenter = ClassDocumenter(Note)
        abjad> rest = documenter()

    Returns ``ClassDocumenter`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    _ignored_special_methods = (
        '__copy__', '__deepcopy__', '__format__', '__getattribute__',
        '__getnewargs__', '__init__', '__reduce__', '__reduce_ex__', 
        '__sizeof__', '__subclasshook__'
    )

    __slots__ = ('_cls', '_data', '_inherited_attributes', 
        '_methods', '_prefix', '_readonly_properties', 
        '_readwrite_properties', '_special_methods')

    ### INITIALIZER ###

    def __init__(self, cls, prefix = 'abjad.tools.'):
        assert isinstance(cls, type)
        assert isinstance(prefix, (str, type(None)))
        self._cls = cls
        self._prefix = prefix

        data = []
        inherited_attributes = []
        methods = []
        readonly_properties = []
        readwrite_properties = []
        special_methods = []

        attrs = inspect.classify_class_attrs(self._cls)
        for attr in attrs:
            if self._attribute_is_inherited(attr):
                inherited_attributes.append(attr)
            if attr.kind == 'method':
                if inspect.isroutine(attr.object):
                    if attr.name not in self._ignored_special_methods:
                        if attr.name.startswith('_'):
                            if attr.name.startswith('__'):
                                special_methods.append(attr)
                        else:
                            special_methods.append(attr)
                else:
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
        stripped_class_name = self._shrink_module_name(self.cls.__module__)
        module_name = '%s.%s' % (self.cls.__module__, self.cls.__name__)

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
        if attr.defining_class is not self._cls:
            return True
        return False

    def _format_attribute(self, attr, kind):
        module_name = '%s.%s' % (self.cls.__module__, self.cls.__name__)
        result = []
        result.append('.. auto%s:: %s.%s' % (kind, module_name, attr.name))
        result.append('')
        if attr in self.inherited_attributes:
            result.append('   .. note:: Inherited from %s' %
                self._shrink_module_name('%s.%s' %
                    (attr.defining_class.__module__, attr.defining_class.__name__)))
            result.append('')
        return result

    def _format_heading(self, text, character='='):
        return [text, character * len(text), '']

    def _format_inheritance_diagram(self):
        module_name = '%s.%s' % (self.cls.__module__, self.cls.__name__)
        return [
            '.. inheritance-diagram:: %s' % module_name,
            '   :private-bases:',
            '',
        ]

    def _shrink_module_name(self, module):
        if self.prefix and module.startswith(self.prefix):
            module = module.partition(self.prefix)[-1]
        parts = module.split('.')
        unique = [parts[0]]
        for part in parts[1:]:
            if part != unique[-1]:
                unique.append(part)
        return '.'.join(unique)

    ### PUBLIC ATTRIBUTES ###

    @property
    def cls(self):
        return self._cls

    @property
    def data(self):
        return self._data

    @property
    def inherited_attributes(self):
        return self._inherited_attributes

    @property
    def methods(self):
        return self._methods

    @property
    def prefix(self):
        return self._prefix

    @property
    def readonly_properties(self):
        return self._readonly_properties

    @property
    def readwrite_properties(self):
        return self._readwrite_properties

    @property
    def special_methods(self):
        return self._special_methods

