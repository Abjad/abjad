import copy
from abjad.tools import leaftools
from abjad.tools.abctools.SortableAttributeEqualityAbjadObject import SortableAttributeEqualityAbjadObject
from abjad.tools.lilypondproxytools import LilyPondTweakReservoir


class NoteHead(SortableAttributeEqualityAbjadObject):
    r'''Abjad model of a note head:

    ::

        >>> notetools.NoteHead(13)
        NoteHead("cs''")

    Note heads are immutable.
    '''

    __slots__ = ('_client', '_is_cautionary', '_is_forced', '_tweak', '_written_pitch')

    def __init__(self, written_pitch=None, client=None,
        is_cautionary=False, is_forced=False, tweak_pairs=()):
        assert isinstance(client, (type(None), leaftools.Leaf))
        self._client = client
        self.written_pitch = written_pitch
        self.is_cautionary = is_cautionary
        self.is_forced = is_forced
        # must assign comparison attribute after written pitch initialization #
        self._comparison_attribute = self.written_pitch
        for tweak_pair in tweak_pairs:
            key, value = tweak_pair
            setattr(self.tweak, key, copy.copy(value))

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(**self.__getnewargs__())

    __deepcopy__ = __copy__

    def __getnewargs__(self):
        args = {
            'written_pitch': self.written_pitch,
            'is_cautionary': self.is_cautionary,
            'is_forced': self.is_forced,
            'tweak_pairs': self.tweak._get_attribute_pairs(),
        }
        return args

    def __repr__(self):
        args = [repr(self._format_string)]
        args.extend(self.tweak._get_attribute_pairs())
        args = ', '.join([str(x) for x in args])
        return '%s(%s)' % (type(self).__name__, args)

    def __str__(self):
        return self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        result = ''
        if self.written_pitch:
            result = str(self.written_pitch)
            if self.is_forced:
                result += '!'
            if self.is_cautionary:
                result += '?'
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def is_cautionary():
        def fget(self):
            '''Get cautionary accidental flag::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.is_cautionary
                False

            Set cautionary accidental flag::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.is_cautionary = True

            Return boolean.
            '''
            return self._is_cautionary
        def fset(self, arg):
            self._is_cautionary = bool(arg)
        return property(**locals())

    @apply
    def is_forced():
        '''Get forced accidental flag::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.is_forced
            False

        Set forced accidental flag::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.is_forced = True

        Return boolean.
        '''
        def fget(self):
            return self._is_forced
        def fset(self, arg):
            self._is_forced = bool(arg)
        return property(**locals())

    @property
    def lilypond_format(self):
        '''Read-only LilyPond input format of note head::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.lilypond_format
            "cs''"

        Return string.
        '''
        from abjad.tools.notetools._format_note_head import _format_note_head
        return _format_note_head(self)

    @property
    def named_chromatic_pitch(self):
        '''Read-only named chromatic pitch equal to note head::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.named_chromatic_pitch
            NamedChromaticPitch("cs''")

        Return named chromatic pitch.
        '''
        return self.written_pitch

    @property
    def tweak(self):
        '''Read-only LilyPond tweak reservoir::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.tweak
            LilyPondTweakReservoir()

        Return LilyPond tweak reservoir.
        '''
        if not hasattr(self, '_tweak'):
            self._tweak = LilyPondTweakReservoir()
        return self._tweak

    @apply
    def written_pitch():
        def fget(self):
            '''Get named pitch of note head::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.written_pitch
                NamedChromaticPitch("cs''")

            Set named pitch of note head::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.written_pitch = "d''"
                >>> note_head.written_pitch
                NamedChromaticPitch("d''")

            Set pitch token.
            '''
            return self._written_pitch
        def fset(self, arg):
            from abjad.tools import pitchtools
            written_pitch = pitchtools.NamedChromaticPitch(arg)
            self._written_pitch = written_pitch
        return property(**locals())
