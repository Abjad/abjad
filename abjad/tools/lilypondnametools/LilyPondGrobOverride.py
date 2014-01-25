# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class LilyPondGrobOverride(AbjadObject):
    r'''A LilyPond grob override.

    ::

        >>> override = lilypondnametools.LilyPondGrobOverride(
        ...    context_name='Staff',
        ...    grob_name='TextSpanner',
        ...    is_once=True,
        ...    property_path=(
        ...        'bound-details',
        ...        'left',
        ...        'text',
        ...        ),
        ...    value=Markup(r'\bold { over pressure }'),
        ...    )

    ::

        >>> print '\n'.join(override.override_format_pieces)
        \once \override Staff.TextSpanner.bound-details.left.text = \markup {
            \bold
                {
                    over
                    pressure
                }
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_name',
        '_grob_name',
        '_is_once',
        '_is_revert',
        '_property_path',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        context_name=None,
        grob_name='NoteHead',
        is_once=None,
        is_revert=None,
        property_path='color',
        value='red',
        ):
        if context_name is not None:
            context_name = str(context_name)
        self._context_name = context_name
        assert grob_name
        self._grob_name = str(grob_name)
        if is_once is not None:
            is_once = bool(is_once)
        self._is_once = is_once
        if is_revert is not None:
            is_revert = bool(is_revert)
        self._is_revert = is_revert
        if isinstance(property_path, str):
            property_path = [property_path]
        property_path = tuple(property_path)
        assert len(property_path)
        assert all(isinstance(x, str) for x in property_path)
        self._property_path = property_path
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        r'''Optional LilyPond grob override context name.

        Returns string or none.
        '''
        return self._context_name

    @property
    def grob_name(self):
        r'''LilyPond grob override grob name.

        Returns string.
        '''
        return self._grob_name

    @property
    def is_once(self):
        r'''Is true if grob override is to be applied only once.  Otherwise
        false.

        Returns boolean or none.
        '''
        return self._is_once

    @property
    def is_revert(self):
        r'''Is true if grob override is a grob revert. Otherwise false.

        Returns boolean or none.
        '''
        return self._is_revert

    @property
    def override_format_pieces(self):
        r'''Gets LilyPond grob override \override format pieces.

        Returns tuple of strings.
        '''
        from abjad.tools import schemetools
        result = []
        if self.is_once:
            result.append(r'\once')
        result.append(r'\override')
        property_path = []
        if self.context_name is not None:
            property_path.append(self.context_name)
        property_path.append(self.grob_name)
        property_path.extend(self.property_path)
        property_path = '.'.join(property_path)
        result.append(property_path)
        result.append('=')
        value_pieces = schemetools.Scheme.format_scheme_value(self.value)
        value_pieces = value_pieces.split('\n')
        result.append(value_pieces[0])
        result[:] = [' '.join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)

    @property
    def property_path(self):
        r'''LilyPond grob override property path.

        Returns tuple of strings.
        '''
        return self._property_path

    @property
    def revert_format_pieces(self):
        r'''Gets LilyPond grob override \revert format pieces.

        Returns tuple of strings.
        '''
        raise NotImplementedError

    @property
    def value(self):
        r'''Value of LilyPond grob override.

        Returns arbitrary object.
        '''
        return self._value
