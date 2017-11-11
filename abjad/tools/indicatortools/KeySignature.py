from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class KeySignature(AbjadValueObject):
    r'''Key signature.

    ..  container:: example

        E major:

        >>> staff = abjad.Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = abjad.KeySignature('e', 'major')
        >>> abjad.attach(key_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \key e \major
                e'8
                fs'8
                gs'8
                a'8
            }

    ..  container:: example

        e minor:

        >>> staff = abjad.Staff("e'8 fs'8 g'8 a'8")
        >>> key_signature = abjad.KeySignature('e', 'minor')
        >>> abjad.attach(key_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \key e \minor
                e'8
                fs'8
                g'8
                a'8
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_mode',
        '_tonic',
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, tonic='c', mode='major'):
        import abjad
        self._tonic = abjad.NamedPitchClass(tonic)
        self._mode = abjad.tonalanalysistools.Mode(mode)
        self._context = 'Staff'

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of key signature.

        ..  container:: example

            E major:

            >>> str(abjad.KeySignature('e', 'major'))
            'e-major'

        ..  container:: example

            e minor:

            >>> str(abjad.KeySignature('e', 'minor'))
            'e-minor'

        Returns string.
        '''
        return '{!s}-{!s}'.format(self.tonic, self.mode)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '{!r}, {!r}'.format(self.tonic, self.mode)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        values = [self.tonic, self.mode]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _get_lilypond_format(self):
        return r'\key {!s} \{!s}'.format(self.tonic, self.mode)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.context
            'Staff'

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.context
            'Staff'

        Returns context or string.
        '''
        return self._context

    @property
    def mode(self):
        r'''Gets mode of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.mode
            Mode('major')

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.mode
            Mode('minor')

        Returns mode.
        '''
        return self._mode

    @property
    def name(self):
        r'''Gets name of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.name
            'E major'

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.name
            'e minor'

        Returns string.
        '''
        if self.mode.mode_name == 'major':
            tonic = str(self.tonic).upper()
        else:
            tonic = str(self.tonic)
        return '{!s} {!s}'.format(tonic, self.mode.mode_name)

    @property
    def tonic(self):
        r'''Gets tonic of key signature.

        ..  container:: example

            E major:

            >>> key_signature = abjad.KeySignature('e', 'major')
            >>> key_signature.tonic
            NamedPitchClass('e')

        ..  container:: example

            e minor:

            >>> key_signature = abjad.KeySignature('e', 'minor')
            >>> key_signature.tonic
            NamedPitchClass('e')

        Returns named pitch-class.
        '''
        return self._tonic
