from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondContextSetting(AbjadValueObject):
    r'''LilyPond context setting.

    >>> context_setting = abjad.lilypondnametools.LilyPondContextSetting(
    ...    lilypond_type='Score',
    ...    context_property='autoBeaming',
    ...    value=False,
    ...    )

    >>> print('\n'.join(context_setting.format_pieces))
    \set Score.autoBeaming = ##f

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lilypond_type',
        '_context_property',
        '_is_unset',
        '_value',
        )

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_type=None,
        context_property='autoBeaming',
        is_unset=False,
        value=False,
        ):
        if lilypond_type is not None:
            lilypond_type = str(lilypond_type)
        self._lilypond_type = lilypond_type
        assert isinstance(context_property, str) and context_property
        self._context_property = context_property
        if is_unset is not None:
            is_unset = bool(is_unset)
        self._is_unset = is_unset
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a LilyPond context setting with
        equivalent keyword values.
        '''
        return super(LilyPondContextSetting, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes LilyPond context setting.

        Returns integer.
        '''
        return super(LilyPondContextSetting, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        string = '\n'.join(self.format_pieces)
        bundle.context_settings.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_type(self):
        r'''Optional LilyPond context name.

        Returns string or none.
        '''
        return self._lilypond_type

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
        if self.lilypond_type is not None:
            string = '{}.{}'.format(
                self.lilypond_type,
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
