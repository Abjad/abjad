from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondGrobOverride(AbjadValueObject):
    r'''LilyPond grob override.

    >>> override = abjad.LilyPondGrobOverride(
    ...    context_name='Staff',
    ...    grob_name='TextSpanner',
    ...    once=True,
    ...    property_path=(
    ...        'bound-details',
    ...        'left',
    ...        'text',
    ...        ),
    ...    value=abjad.Markup(r'\bold { over pressure }'),
    ...    )

    >>> print(override.override_string)
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
        '_once',
        '_is_revert',
        '_property_path',
        '_value',
        )

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        context_name=None,
        grob_name='NoteHead',
        once=None,
        is_revert=None,
        property_path='color',
        value='red',
        ):
        if context_name is not None:
            context_name = str(context_name)
        self._context_name = context_name
        assert grob_name
        self._grob_name = str(grob_name)
        if once is not None:
            once = bool(once)
        self._once = once
        if is_revert is not None:
            is_revert = bool(is_revert)
        self._is_revert = is_revert
        if isinstance(property_path, str):
            property_path = [property_path]
        property_path = tuple(property_path)
        assert all(isinstance(x, str) and x for x in property_path)
        self._property_path = property_path
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a LilyPond grob override with equivalent
        keyword values.
        '''
        return super(LilyPondGrobOverride, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes LilyPond grob override.

        Returns integer.
        '''
        return super(LilyPondGrobOverride, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        if not self.once:
            revert_format = '\n'.join(self.revert_format_pieces)
            bundle.grob_reverts.append(revert_format)
        if not self.is_revert:
            override_format = '\n'.join(self.override_format_pieces)
            bundle.grob_overrides.append(override_format)
        return bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _override_property_path_string(self):
        parts = []
        if self.context_name is not None:
            parts.append(self.context_name)
        parts.append(self.grob_name)
        parts.extend(self.property_path)
        path = '.'.join(parts)
        return path

    @property
    def _revert_property_path_string(self):
        parts = []
        if self.context_name is not None:
            parts.append(self.context_name)
        parts.append(self.grob_name)
        parts.append(self.property_path[0])
        path = '.'.join(parts)
        return path

    ### PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        r'''Optional LilyPond grob override context name.

        >>> override = abjad.LilyPondGrobOverride(
        ...    context_name='Staff',
        ...    grob_name='TextSpanner',
        ...    once=True,
        ...    property_path=(
        ...        'bound-details',
        ...        'left',
        ...        'text',
        ...        ),
        ...    value=abjad.Markup(r'\bold { over pressure }'),
        ...    )
        >>> override.context_name
        'Staff'

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     property_path='style',
        ...     value=abjad.SchemeSymbol('zigzag'),
        ...     )
        >>> override.context_name is None
        True

        Returns string or none.
        '''
        return self._context_name

    @property
    def grob_name(self):
        r'''LilyPond grob override grob name.

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     property_path='style',
        ...     value=abjad.SchemeSymbol('zigzag'),
        ...     )
        >>> override.grob_name
        'Glissando'

        Returns string.
        '''
        return self._grob_name

    @property
    def once(self):
        r'''Is true if grob override is to be applied only once.  Otherwise
        false.

        >>> override = abjad.LilyPondGrobOverride(
        ...    context_name='Staff',
        ...    grob_name='TextSpanner',
        ...    once=True,
        ...    property_path=(
        ...        'bound-details',
        ...        'left',
        ...        'text',
        ...        ),
        ...    value=abjad.Markup(r'\bold { over pressure }'),
        ...    )
        >>> bool(override.once)
        True

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     property_path='style',
        ...     value=abjad.SchemeSymbol('zigzag'),
        ...     )
        >>> bool(override.once)
        False

        Returns boolean or none.
        '''
        return self._once

    @property
    def is_revert(self):
        r'''Is true if grob override is a grob revert. Otherwise false.

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     property_path='style',
        ...     value=abjad.SchemeSymbol('zigzag'),
        ...     )
        >>> bool(override.is_revert)
        False

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     is_revert=True,
        ...     property_path='style',
        ...     )
        >>> bool(override.is_revert)
        True

        Returns boolean or none.
        '''
        return self._is_revert

    @property
    def override_format_pieces(self):
        r'''Gets LilyPond grob override \override format pieces.

        >>> override = abjad.LilyPondGrobOverride(
        ...    context_name='Staff',
        ...    grob_name='TextSpanner',
        ...    once=True,
        ...    property_path=(
        ...        'bound-details',
        ...        'left',
        ...        'text',
        ...        ),
        ...    value=abjad.Markup(r'\bold { over pressure }'),
        ...    )
        >>> for line in override.override_format_pieces:
        ...     line
        ...
        '\\once \\override Staff.TextSpanner.bound-details.left.text = \\markup {'
        '    \\bold'
        '        {'
        '            over'
        '            pressure'
        '        }'
        '    }'

        Returns tuple of strings.
        '''
        from abjad.tools import schemetools
        result = []
        if self.once:
            result.append(r'\once')
        result.append(r'\override')
        result.append(self._override_property_path_string)
        result.append('=')
        value_pieces = schemetools.Scheme.format_embedded_scheme_value(
            self.value)
        value_pieces = value_pieces.split('\n')
        result.append(value_pieces[0])
        result[:] = [' '.join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)

    @property
    def override_string(self):
        r'''Gets LilyPond grob override \override string.

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     property_path='style',
        ...     value=abjad.SchemeSymbol('zigzag'),
        ...     )
        >>> override.override_string
        "\\override Glissando.style = #'zigzag"

        Returns string.
        '''
        return '\n'.join(self.override_format_pieces)

    @property
    def property_path(self):
        r'''LilyPond grob override property path.

        >>> override = abjad.LilyPondGrobOverride(
        ...    context_name='Staff',
        ...    grob_name='TextSpanner',
        ...    once=True,
        ...    property_path=(
        ...        'bound-details',
        ...        'left',
        ...        'text',
        ...        ),
        ...    value=abjad.Markup(r'\bold { over pressure }'),
        ...    )
        >>> override.property_path
        ('bound-details', 'left', 'text')

        Returns tuple of strings.
        '''
        return self._property_path

    @property
    def revert_format_pieces(self):
        r'''Gets LilyPond grob override \revert format pieces.

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     property_path='style',
        ...     value=abjad.SchemeSymbol('zigzag'),
        ...     )
        >>> override.revert_format_pieces
        ('\\revert Glissando.style',)

        Returns tuple of strings.
        '''
        result = r'\revert {}'.format(self._revert_property_path_string)
        return (result,)

    @property
    def revert_string(self):
        r'''Gets LilyPond grob override \revert string.

        >>> override = abjad.LilyPondGrobOverride(
        ...     grob_name='Glissando',
        ...     property_path='style',
        ...     value=abjad.SchemeSymbol('zigzag'),
        ...     )
        >>> override.revert_string
        '\\revert Glissando.style'

        Returns string.
        '''
        return '\n'.join(self.revert_format_pieces)

    @property
    def value(self):
        r'''Value of LilyPond grob override.

        >>> override = abjad.LilyPondGrobOverride(
        ...    context_name='Staff',
        ...    grob_name='TextSpanner',
        ...    once=True,
        ...    property_path=(
        ...        'bound-details',
        ...        'left',
        ...        'text',
        ...        ),
        ...    value=abjad.Markup(r'\bold { over pressure }'),
        ...    )
        >>> override.value
        Markup(contents=[MarkupCommand('bold', ['over', 'pressure'])])

        Returns arbitrary object.
        '''
        return self._value
