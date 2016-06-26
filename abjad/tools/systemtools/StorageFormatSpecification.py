# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class StorageFormatSpecification(AbjadObject):
    r'''Specifies the storage format of a given object.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Storage formatting'

    __slots__ = (
        '_body_text',
        '_include_abjad_namespace',
        '_instance',
        '_is_bracketed',
        '_is_indented',
        '_keyword_argument_callables',
        '_keyword_argument_names',
        '_keywords_ignored_when_false',
        '_positional_argument_values',
        '_storage_format_pieces',
        '_tools_package_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        instance=None,
        body_text=None,
        include_abjad_namespace=None,
        is_bracketed=False,
        is_indented=True,
        keyword_argument_callables=None,
        keyword_argument_names=None,
        keywords_ignored_when_false=None,
        positional_argument_values=None,
        storage_format_pieces=None,
        tools_package_name=None,
        ):
        self._instance = instance

        if body_text is not None:
            body_text = str(body_text)
        self._body_text = body_text

        self._include_abjad_namespace = bool(include_abjad_namespace)
        self._is_bracketed = bool(is_bracketed)
        self._is_indented = bool(is_indented)

        if keyword_argument_callables is not None:
            keyword_argument_callables = \
                tuple(sorted(dict(keyword_argument_callables).items()))
        self._keyword_argument_callables = keyword_argument_callables

        if keyword_argument_names is not None:
            keyword_argument_names = tuple(keyword_argument_names)
        self._keyword_argument_names = keyword_argument_names

        if keywords_ignored_when_false is not None:
            keywords_ignored_when_false = tuple(keywords_ignored_when_false)
        self._keywords_ignored_when_false = keywords_ignored_when_false

        if positional_argument_values is not None:
            positional_argument_values = tuple(positional_argument_values)
        self._positional_argument_values = positional_argument_values

        if storage_format_pieces is not None:
            storage_format_pieces = tuple(storage_format_pieces)
        self._storage_format_pieces = storage_format_pieces

        if tools_package_name is not None:
            tools_package_name = str(tools_package_name)
        self._tools_package_name = tools_package_name

    ### PUBLIC PROPERTIES ###

    @property
    def body_text(self):
        r'''Body text of storage specification.

        Returns string.
        '''
        return self._body_text

    @property
    def instance(self):
        r'''Instance of storage specification.

        Returns string.
        '''
        return self._instance

    @property
    def include_abjad_namespace(self):
        r'''Is true when storage specification includes Abjad namespace.

        Returns true or false.
        '''
        return self._include_abjad_namespace

    @property
    def is_bracketed(self):
        r'''Is true when storage specification is bracketed.
        Otherwise false.

        Returns true or false.
        '''
        return self._is_bracketed

    @property
    def is_indented(self):
        r'''Is true when storage format is indented. Otherwise false.

        Returns true or false.
        '''
        return self._is_indented

    @property
    def keyword_argument_callables(self):
        r'''Keyword argument callables.

        Returns tuple.
        '''
        return self._keyword_argument_callables

    @property
    def keyword_argument_names(self):
        r'''Keyword argument names of storage format.

        Returns tuple.
        '''
        from abjad.tools import systemtools
        if self._keyword_argument_names is not None:
            names = self._keyword_argument_names
        else:
            names = \
                systemtools.StorageFormatManager.get_keyword_argument_names(
                    self.instance)
        if self._keywords_ignored_when_false is not None:
            names = list(names)
            for name in self._keywords_ignored_when_false:
                result = getattr(self.instance, name, True)
                if not result and name in names:
                    names.remove(name)
            return tuple(names)
        return names

    @property
    def keywords_ignored_when_false(self):
        r'''Keywords ignored when false.

        Returns tuple.
        '''
        return self._keywords_ignored_when_false

    @property
    def positional_argument_values(self):
        r'''Positional argument values.

        Returns tuple.
        '''
        from abjad.tools import systemtools
        if self._positional_argument_values is not None:
            return self._positional_argument_values
        return systemtools.StorageFormatManager.get_positional_argument_values(
            self.instance)

    @property
    def storage_format_pieces(self):
        r'''Storage format pieces.

        Returns tuple.
        '''
        return self._storage_format_pieces

    @property
    def tools_package_name(self):
        r'''Tools package name of storage format.

        Returns string.
        '''
        from abjad.tools import systemtools
        tools_package_name = None
        if self._tools_package_name is not None:
            tools_package_name = self._tools_package_name
        if self.instance is not None:
            tools_package_name = \
                systemtools.StorageFormatManager.get_tools_package_name(
                self.instance)
        if tools_package_name and self.include_abjad_namespace:
            tools_package_name = 'abjad.' + tools_package_name
        return tools_package_name