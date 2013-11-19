# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class StorageFormatSpecification(AbjadObject):
    r'''Specifies the storage format of a given object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_body_text',
        '_instance',
        '_is_bracketted',
        '_is_indented',
        '_keyword_argument_names',
        '_keywords_ignored_when_false',
        '_positional_argument_values',
        '_storage_format_pieces',
        '_tools_package_name',
        )

    ### INITIALIZER ###

    def __init__(self,
        instance,
        body_text=None,
        is_bracketted=False,
        is_indented=True,
        keyword_argument_names=None,
        keywords_ignored_when_false=None,
        positional_argument_values=None,
        storage_format_pieces=None,
        tools_package_name=None,
        ):
        self._instance = instance
        if body_text is not None:
            self._body_text = str(body_text)
        else:
            self._body_text = None
        self._is_bracketted = bool(is_bracketted)
        self._is_indented = bool(is_indented)
        if keyword_argument_names is not None:
            self._keyword_argument_names = tuple(keyword_argument_names)
        else:
            self._keyword_argument_names = None
        if keywords_ignored_when_false is not None:
            self._keywords_ignored_when_false = \
                tuple(keywords_ignored_when_false)
        else:
            self._keywords_ignored_when_false = None
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

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        state = {}
        for slot in self.__slots__:
            name = slot[1:]
            state[name] = kwargs.get(name, getattr(self, name))
        return type(self)(**state)

    ### PUBLIC PROPERTIES ###

    @property
    def body_text(self):
        return self._body_text

    @property
    def instance(self):
        return self._instance

    @property
    def is_bracketted(self):
        return self._is_bracketted

    @property
    def is_indented(self):
        return self._is_indented

    @property
    def keyword_argument_names(self):
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
                result = getattr(self.instance, name)
                if not result:
                    names.remove(name)
            return tuple(names)
        return names

    @property
    def keywords_ignored_when_false(self):
        return self._keywords_ignored_when_false

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
