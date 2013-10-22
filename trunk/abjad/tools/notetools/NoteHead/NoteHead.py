# -*- encoding: utf-8 -*-
import copy
import functools
from abjad.tools import leaftools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.lilypondproxytools import LilyPondTweakReservoir


@functools.total_ordering
class NoteHead(AbjadObject):
    r'''Abjad model of a note head:

    ::

        >>> notetools.NoteHead(13)
        NoteHead("cs''")

    Note heads are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client', 
        '_is_cautionary', 
        '_is_forced', 
        '_tweak', 
        '_written_pitch',
        )

    ### INITIALIZER ###

    def __init__(self, written_pitch=None, client=None,
        is_cautionary=False, is_forced=False, tweak_pairs=()):
        assert isinstance(client, (type(None), leaftools.Leaf))
        self._client = client
        self.written_pitch = written_pitch
        self.is_cautionary = is_cautionary
        self.is_forced = is_forced
        for tweak_pair in tweak_pairs:
            key, value = tweak_pair
            setattr(self.tweak, key, copy.copy(value))

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(*self.__getnewargs__())

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self.written_pitch == expr.written_pitch
        return self.written_pitch == expr

    def __getnewargs__(self):
        args = (
            self.written_pitch,
            None,
            self.is_cautionary,
            self.is_forced,
            self.tweak._get_attribute_pairs(),
        )
        return args

    def __lt__(self, expr):
        if isinstance(expr, type(self)):
            return self.written_pitch < expr.written_pitch
        try:
            expr = type(self)(expr)
        except (ValueError, TypeError):
            return False
        return self.written_pitch < expr.written_pitch

    def __repr__(self):
        args = [repr(self._format_string)]
        args.extend(self.tweak._get_attribute_pairs())
        args = ', '.join([str(x) for x in args])
        return '%s(%s)' % (self._class_name, args)

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
            r'''Get cautionary accidental flag:

            ::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.is_cautionary
                False

            Set cautionary accidental flag:

            ::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.is_cautionary = True

            Returns boolean.
            '''
            return self._is_cautionary
        def fset(self, arg):
            self._is_cautionary = bool(arg)
        return property(**locals())

    @apply
    def is_forced():
        r'''Get forced accidental flag:

        ::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.is_forced
            False

        Set forced accidental flag:

        ::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.is_forced = True

        Returns boolean.
        '''
        def fget(self):
            return self._is_forced
        def fset(self, arg):
            self._is_forced = bool(arg)
        return property(**locals())

    @property
    def lilypond_format(self):
        r'''LilyPond input format of note head:

        ::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.lilypond_format
            "cs''"

        Returns string.
        '''
        from abjad.tools import formattools
        from abjad.tools import chordtools
        # make sure note head has pitch
        assert self.written_pitch
        result = []
        # format chord note head with optional tweaks
        if isinstance(self._client, chordtools.Chord):
            for key, value in vars(self.tweak).iteritems():
                if not key.startswith('_'):
                    result.append(
                        r'\tweak %s %s' % (
                        formattools.format_lilypond_attribute(key),
                        formattools.format_lilypond_value(value)),
                        )
        # format note head pitch
        kernel = self.written_pitch.lilypond_format
        if self.is_forced:
            kernel += '!'
        if self.is_cautionary:
            kernel += '?'
        result.append(kernel)
        result = '\n'.join(result)
        # return formatted note head
        return result

    @property
    def named_pitch(self):
        r'''Named pitch equal to note head:

        ::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.named_pitch
            NamedPitch("cs''")

        Returns named pitch.
        '''
        return self.written_pitch

    @property
    def tweak(self):
        r'''LilyPond tweak reservoir:

        ::

            >>> note_head = notetools.NoteHead("cs''")
            >>> note_head.tweak
            LilyPondTweakReservoir()

        Returns LilyPond tweak reservoir.
        '''
        if not hasattr(self, '_tweak'):
            self._tweak = LilyPondTweakReservoir()
        return self._tweak

    @apply
    def written_pitch():
        def fget(self):
            r'''Get named pitch of note head:

            ::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.written_pitch
                NamedPitch("cs''")

            Set named pitch of note head:

            ::

                >>> note_head = notetools.NoteHead("cs''")
                >>> note_head.written_pitch = "d''"
                >>> note_head.written_pitch
                NamedPitch("d''")

            Set pitch token.
            '''
            return self._written_pitch
        def fset(self, arg):
            from abjad.tools import pitchtools
            written_pitch = pitchtools.NamedPitch(arg)
            self._written_pitch = written_pitch
        return property(**locals())
