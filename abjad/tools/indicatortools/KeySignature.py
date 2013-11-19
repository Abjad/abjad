# -*- encoding: utf-8 -*-
#from abjad.tools.indicatortools.ContextMark import ContextMark
from abjad.tools.abctools.AbjadObject import AbjadObject


#class KeySignature(ContextMark):
class KeySignature(AbjadObject):
    r'''A key signature.

    ::

        >>> staff = Staff("e'8 fs'8 gs'8 a'8")
        >>> key_signature = KeySignature('e', 'major')
        >>> attach(key_signature, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \key e \major
            e'8
            fs'8
            gs'8
            a'8
        }

    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('c'),
        repr('major'),
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, tonic, mode):
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools import tonalanalysistools
        #ContextMark.__init__(self)
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
            self._tonic, 
            self._mode,
            )

    def __eq__(self, arg):
        r'''True when `arg` is a key signature with tonic and mode equal
        to key signature. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.tonic == arg.tonic:
                if self.mode == arg.mode:
                    return True
        return False

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

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                str(self.tonic),
                str(self.mode),
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def mode(self):
        r'''Mode of signature.

        ::

            >>> key_signature.mode
            Mode('major')

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
