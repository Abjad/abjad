# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class StorageFormatSpecification(AbjadObject):
    r'''Specifies the storage format of a given object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_instance',
        '_is_indented',
        '_keyword_argument_names',
        '_positional_argument_values',
        '_storage_format_pieces',
        '_tools_package_name',
        )

    ### INITIALIZER ###

    def __init__(self,
        instance,
        is_indented=True,
        keyword_argument_names=None,
        positional_argument_values=None,
        storage_format_pieces=None,
        tools_package_name=None,
        ):
        self._instance = instance
        self._is_indented = bool(is_indented)
        if keyword_argument_names is not None:
            self._keyword_argument_names = tuple(keyword_argument_names)
        else:
            self._keyword_argument_names = None
        if positional_argument_values is not None:
            self._positional_argument_values = \
                tuple(positional_argument_values)
        else:
            self._positional_argument_values = None
        if storage_format_pieces is not None:
            self._storage_format_pieces = tuple(storage_format_pieces)
        else:
            self._storage_format_pieces = None
        if tools_package_name is not None:
            self._tools_package_name = str(tools_package_name)
        else:
            self._tools_package_name = None

    ### PUBLIC PROPERTIES ###

    @property
    def instance(self):
        return self._instance

    @property
    def is_indented(self):
        return self._is_indented

    @property
    def keyword_argument_names(self):
        from abjad.tools import systemtools
        if self._keyword_argument_names is not None:
            return self._keyword_argument_names
        return systemtools.StorageFormatManager.get_keyword_argument_names(
            self.instance)

    @property
    def positional_argument_values(self):
        from abjad.tools import systemtools
        if self._positional_argument_values is not None:
            return self._positional_argument_values
        return systemtools.StorageFormatManager.get_positional_argument_values(
            self.instance)

    @property
    def storage_format_pieces(self):
        return self._storage_format_pieces

    @property
    def tools_package_name(self):
        from abjad.tools import systemtools
        if self._tools_package_name is not None:
            return self._tools_package_name
        return systemtools.StorageFormatManager.get_tools_package_name(
            self.instance)
