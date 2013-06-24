import abc
import inspect
from abjad.tools.documentationtools.Documenter import Documenter


class ClassDocumenter(Documenter):
    '''ClassDocumenter generates an ReST API entry for a given class:

    ::

        >>> documenter = documentationtools.ClassDocumenter(notetools.Note)
        >>> rest = documenter()

    Returns ``ClassDocumenter`` instance.
    '''

    ### CLASS VARIABLES ###

    _ignored_special_methods = (
        '__format__', '__getattribute__',
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
            if attr.kind in ('class method', 'method', 'static method'):
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
        from abjad.tools import documentationtools

        stripped_class_name = self._shrink_module_name(self.object.__module__)

        module_name = '{}.{}'.format(self.object.__module__, self.object.__name__)

        document = documentationtools.ReSTDocument()

        document.append(documentationtools.ReSTHeading(
            level=2,
            text=stripped_class_name,
            ))

        document.append(documentationtools.ReSTLineageDirective(
            argument=module_name,
            ))

        document.append(documentationtools.ReSTAutodocDirective(
            argument=module_name,
            directive='autoclass',
            options={
                #'noindex': True, 
                },
            ))

        document.extend(self._format_inheritance_note())

        if self.readonly_properties:
            document.append(documentationtools.ReSTHeading(
                level=3,
                text='Read-only properties',
                ))
            for attr in self.readonly_properties:
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(module_name, attr.name),
                    directive='autoattribute',
                    options={'noindex': True},
                    )
                document.append(autodoc)

        if self.readwrite_properties:
            document.append(documentationtools.ReSTHeading(
                level=3,
                text='Read/write properties',
                ))
            for attr in self.readwrite_properties:
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(module_name, attr.name),
                    directive='autoattribute',
                    options={'noindex': True},
                    )
                document.append(autodoc)

        if self.methods:
            document.append(documentationtools.ReSTHeading(
                level=3,
                text='Methods',
                ))
            for attr in self.methods:
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(module_name, attr.name),
                    directive='automethod',
                    options={'noindex': True},
                    )
                document.append(autodoc)

        if self.special_methods:
            document.append(documentationtools.ReSTHeading(
                level=3,
                text='Special methods',
                ))
            for attr in self.special_methods:
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(module_name, attr.name),
                    directive='automethod',
                    options={'noindex': True},
                    )
                document.append(autodoc)

        return document.rest_format

    ### PRIVATE METHODS ###

    def _attribute_is_inherited(self, attr):
        if attr.defining_class is not self._object:
            return True
        return False

    def _format_inheritance_note(self):
        from abjad.tools import documentationtools
        pieces = []
        pieces.append(documentationtools.ReSTHeading(                     
            level=3,                                                        
            text='Bases',
            ))
        mro = inspect.getmro(self.object)[1:]
        for cls in mro:
            packagesystem_path = '.'.join((cls.__module__, cls.__name__))
            stripped_packagesystem_path = self._shrink_module_name(
                packagesystem_path)
            if packagesystem_path.startswith('__builtin__'):
                packagesystem_path = packagesystem_path.partition('__builtin__.')[-1]
            text = '- :class:`{} <{}>`'.format(
                stripped_packagesystem_path,
                packagesystem_path,
                )
            paragraph = documentationtools.ReSTParagraph(                                
                text=text,
                wrap=False,                                                         
                )
            pieces.append(paragraph) 
        return pieces

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
