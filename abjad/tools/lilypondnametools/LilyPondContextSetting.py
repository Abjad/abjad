# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class LilyPondContextSetting(AbjadObject):
    r'''A LilyPond context setting.

    ::

        >>> context_setting = lilypondnametools.LilyPondContextSetting(
        ...    context_name='Score',
        ...    context_property='autoBeaming',
        ...    value=False,
        ...    )

    ::

        >>> print('\n'.join(context_setting.format_pieces))
        \set Score.autoBeaming = ##f

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_name',
        '_context_property',
        '_is_unset',
        '_value',
        )

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        context_name=None,
        context_property='autoBeaming',
        is_unset=False,
        value=False,
        ):
        if context_name is not None:
            context_name = str(context_name)
        self._context_name = context_name
        assert isinstance(context_property, str) and context_property
        self._context_property = context_property
        if is_unset is not None:
            is_unset = bool(is_unset)
        self._is_unset = is_unset
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a LilyPond context setting with equivalent
        keyword values.
        '''
        from abjad.tools import systemtools
        return systemtools.TestManager.compare_objects(self, expr)

    def __hash__(self):
        r'''Hashes LilyPond context setting.

        Returns integer.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatAgent(self).get_hash_values()
        return hash(hash_values)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        string = '\n'.join(self.format_pieces)
        lilypond_format_bundle.context_settings.append(string)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        r'''Optional LilyPond context name.

        Returns string or none.
        '''
        return self._context_name

    @property
    def context_property(self):
        r'''LilyPond context property name.

        Returns string.
        '''
        return self._context_property

    @property
    def format_pieces(self):
        r'''Gets LilyPond context setting \set or \unset format pieces.

        Returns tuple of strings.
        '''
        from abjad.tools import schemetools
        result = []
        if not self.is_unset:
            result.append(r'\set')
        else:
            result.append(r'\unset')
        if self.context_name is not None:
            string = '{}.{}'.format(
                self.context_name,
                self.context_property,
                )
            result.append(string)
        else:
            result.append(self.context_property)
        result.append('=')
        value_pieces = schemetools.Scheme.format_embedded_scheme_value(
            self.value)
        value_pieces = value_pieces.split('\n')
        result.append(value_pieces[0])
        result[:] = [' '.join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)

    @property
    def is_unset(self):
        r'''Is true if context setting unsets its value. Otherwise false.

        Returns boolean or none.
        '''
        return self._is_unset

    @property
    def value(self):
        r'''Value of LilyPond context setting.

        Returns arbitrary object.
        '''
        return self._value
