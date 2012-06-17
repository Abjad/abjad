from abjad.tools.contexttools.ContextMark import ContextMark


class KeySignatureMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of a key signature setting or key signature change::

        >>> staff = Staff("e'8 fs'8 gs'8 a'8")

    ::

        >>> contexttools.KeySignatureMark('e', 'major')(staff)
        KeySignatureMark(NamedChromaticPitchClass('e'), Mode('major'))(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \key e \major
            e'8
            fs'8
            gs'8
            a'8
        }

    Key signature marks target staff context by default.
    '''

    ### CLASS ATTRIBUTES ###

    #__slots__ = ('_tonic', '_mode')

    _default_mandatory_input_arguments = (
        repr('c'),
        repr('major'),
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, tonic, mode, target_context=None):
        from abjad.tools.stafftools.Staff import Staff
        from abjad.tools import pitchtools
        from abjad.tools import tonalitytools
        ContextMark.__init__(self, target_context=target_context)
        if self.target_context is None:
            self._target_context = Staff
        tonic = pitchtools.NamedChromaticPitchClass(tonic)
        mode = tonalitytools.Mode(mode)
        self._tonic = tonic
        self._mode = mode

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(self._tonic, self._mode,
            target_context = self._target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.tonic == arg.tonic:
                if self.mode == arg.mode:
                    return True
        return False

    def __str__(self):
        return '%s-%s' % (self.tonic, self.mode)

    ### PRIVATE PROPERTIES ###

    @property
    #def _contents_name(self):
    def _contents_repr_string(self):
        return "%r, %r" % (self.tonic, self.mode)

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''Read-only LilyPond format of key signature mark:

        ::

            >>> key_signature = contexttools.KeySignatureMark('e', 'major')
            >>> key_signature.lilypond_format
            '\\key e \\major'

        Return string.
        '''
        return r'\key %s \%s' % (self.tonic, self.mode)

    @apply
    def mode():
        def fget(self):
            r'''Get mode of key signature::

                >>> key_signature = contexttools.KeySignatureMark('e', 'major')
                >>> key_signature.mode
                Mode('major')

            Set mode of key signature::

                >>> key_signature.mode = 'minor'
                >>> key_signature.mode
                Mode('minor')

            Return mode.
            '''
            return self._mode
        def fset(self, mode):
            from abjad.tools import tonalitytools
            mode = tonalitytools.Mode(mode)
            self._mode = mode
        return property(**locals())

    @property
    def name(self):
        r'''Read-only name of key signature:

        ::

            >>> key_signature = contexttools.KeySignatureMark('e', 'major')
            >>> key_signature.name
            'E major'

        Return string.
        '''
        if self.mode.mode_name == 'major':
            tonic = str(self.tonic).upper()
        else:
            tonic = str(self.tonic)
        return '%s %s' % (tonic, self.mode.mode_name)

    @apply
    def tonic():
        def fget(self):
            r'''Get tonic of key signature::

                >>> key_signature = contexttools.KeySignatureMark('e', 'major')
                >>> key_signature.tonic
                NamedChromaticPitchClass('e')

            Set tonic of key signature::

                >>> key_signature.tonic = 'd'
                >>> key_signature.tonic
                NamedChromaticPitchClass('d')

            Return named chromatic pitch.
            '''
            return self._tonic
        def fset(self, tonic):
            from abjad.tools import pitchtools
            tonic = pitchtools.NamedChromaticPitchClass(tonic)
            self._tonic = tonic
        return property(**locals())
