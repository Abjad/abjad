# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class KeySignature(AbjadObject):
    r'''A key signature.

    ::

        >>> staff = Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = KeySignature('e', 'major')
        >>> attach(key_signature, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \key e \major
            e'8
            fs'8
            gs'8
            a'8
        }

    '''

    ### CLASS VARIABLES ###

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, tonic='c', mode='major'):
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools import tonalanalysistools
        tonic = pitchtools.NamedPitchClass(tonic)
        mode = tonalanalysistools.Mode(mode)
        self._tonic = tonic
        self._mode = mode
        self._default_scope = scoretools.Staff

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies key signature.

        Returns new key signature.
        '''
        return type(self)(
            self.tonic,
            self.mode,
            )

    def __eq__(self, expr):
        r'''Is true when `expr` is a key signature with tonic and mode equal
        to that of this key signature. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.tonic == expr.tonic:
                if self.mode == expr.mode:
                    return True
        return False

    def __hash__(self):
        r'''Hashes key signature.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(KeySignature, self).__hash__()

    def __str__(self):
        r'''String representation of key signature.

        Returns string.
        '''
        return '{!s}-{!s}'.format(self.tonic, self.mode)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '{!r}, {!r}'.format(self.tonic, self.mode)

    @property
    def _lilypond_format(self):
        return r'\key {!s} \{!s}'.format(self.tonic, self.mode)

    ### PUBLIC PROPERTIES ###

    @property
    def mode(self):
        r'''Mode of signature.

        ::

            >>> key_signature.mode
            Mode(mode_name='major')

        Returns mode.
        '''
        return self._mode

    @property
    def name(self):
        r'''Name of key signature.

        ::

            >>> key_signature = KeySignature('e', 'major')
            >>> key_signature.name
            'E major'

        Returns string.
        '''
        if self.mode.mode_name == 'major':
            tonic = str(self.tonic).upper()
        else:
            tonic = str(self.tonic)
        return '{!s} {!s}'.format(tonic, self.mode.mode_name)

    @property
    def tonic(self):
        r'''Tonic of key signature.

        ::

            >>> key_signature.tonic
            NamedPitchClass('e')

        Returns named pitch-class.
        '''
        return self._tonic
