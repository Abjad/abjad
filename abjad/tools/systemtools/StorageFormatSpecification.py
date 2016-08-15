# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class StorageFormatSpecification(AbjadObject):
    r'''Specifies the storage format of a given object.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Storage formatting'

    __slots__ = (
        '_repr_text',
        '_include_abjad_namespace',
        '_instance',
        '_is_bracketed',
        '_is_indented',
        '_keyword_argument_names',
        '_positional_argument_values',
        '_storage_format_text',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        instance=None,
        repr_text=None,
        include_abjad_namespace=None,
        is_bracketed=False,
        is_indented=True,
        keyword_argument_names=None,
        positional_argument_values=None,
        storage_format_text=None,
        ):
        self._instance = instance

        if repr_text is not None:
            repr_text = str(repr_text)
        self._repr_text = repr_text

        self._include_abjad_namespace = bool(include_abjad_namespace)
        self._is_bracketed = bool(is_bracketed)
        self._is_indented = bool(is_indented)

        if keyword_argument_names is not None:
            keyword_argument_names = tuple(keyword_argument_names)
        self._keyword_argument_names = keyword_argument_names

        if positional_argument_values is not None:
            positional_argument_values = tuple(positional_argument_values)
        self._positional_argument_values = positional_argument_values

        if storage_format_text is not None:
            storage_format_text = str(storage_format_text)
        self._storage_format_text = storage_format_text

    ### PUBLIC PROPERTIES ###

    @property
    def repr_text(self):
        r'''Body text of storage specification.

        Returns string.
        '''
        return self._repr_text

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
    def keyword_argument_names(self):
        r'''Keyword argument names of storage format.

        Returns tuple.
        '''
        return self._keyword_argument_names

    @property
    def positional_argument_values(self):
        r'''Positional argument values.

        Returns tuple.
        '''
        return self._positional_argument_values

    @property
    def storage_format_text(self):
        r'''Storage format pieces.

        Returns tuple.
        '''
        return self._storage_format_text
