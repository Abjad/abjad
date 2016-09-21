# -*- coding: utf-8 -*-
import copy
import functools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadObject import AbjadObject


@functools.total_ordering
class NoteHead(AbjadObject):
    r'''A note head.

    ::

        >>> note_head = scoretools.NoteHead(13)
        >>> note_head
        NoteHead("cs''")

    Note heads are immutable.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Note heads'

    __slots__ = (
        '_client',
        '_is_cautionary',
        '_is_forced',
        '_is_parenthesized',
        '_tweak',
        '_written_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        written_pitch=None,
        client=None,
        is_cautionary=None,
        is_forced=None,
        is_parenthesized=None,
        tweak_pairs=(),
        ):
        from abjad.tools import scoretools
        assert isinstance(client, (type(None), scoretools.Leaf))
        self._client = client
        self._tweak = None
        if isinstance(written_pitch, type(self)):
            note_head = written_pitch
            written_pitch = note_head.written_pitch
            is_cautionary = note_head.is_cautionary
            is_forced = note_head.is_forced
            tweak_pairs = note_head.tweak._get_attribute_pairs()
        elif written_pitch is None:
            written_pitch = 0
        self.written_pitch = written_pitch
        self.is_cautionary = is_cautionary
        self.is_forced = is_forced
        self.is_parenthesized = is_parenthesized
        for tweak_pair in tweak_pairs:
            key, value = tweak_pair
            setattr(self.tweak, key, copy.copy(value))

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies note-head.

        ::

            >>> import copy
            >>> copy.copy(note_head)
            NoteHead("cs''")

        Returns new note-head.
        '''
        return type(self)(*self.__getnewargs__())

    def __eq__(self, expr):
        r'''Is true when `expr` is a note-head with written pitch equal to
        that of this note-head. Otherwise false.

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self.written_pitch == expr.written_pitch
        return self.written_pitch == expr

    def __format__(self, format_specification=''):
        r'''Formats note-head.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        args = (
            self.written_pitch,
            None,
            self.is_cautionary,
            self.is_forced,
            self.is_parenthesized,
            self.tweak._get_attribute_pairs(),
            )
        return args

    def __hash__(self):
        r'''Hashes note-head.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NoteHead, self).__hash__()

    def __lt__(self, expr):
        r'''Is true when `expr` is a note-head with written pitch greater than
        that of this note-head. Otherwise false.

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self.written_pitch < expr.written_pitch
        try:
            expr = type(self)(expr)
        except (ValueError, TypeError):
            return False
        return self.written_pitch < expr.written_pitch

    def __repr__(self):
        r'''Gets interpreter representation of note-head.

        ::

            >>> note_head
            NoteHead("cs''")

        Returns string.
        '''
        return super(NoteHead, self).__repr__()

    def __str__(self):
        r'''String representation of note-head.

        ::

            >>> str(note_head)
            "cs''"

        Returns string.
        '''
        return self._format_string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        args = [repr(self._format_string)]
        args.extend(self.tweak._get_attribute_pairs())
        args = ', '.join([str(x) for x in args])
        repr_text = '{}({})'.format(type(self).__name__, args)
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        if 'client' in names:
            names.remove('client')
        if 'tweak_pairs' in names:
            names.remove('tweak_pairs')
        return systemtools.FormatSpecification(
            self,
            repr_text=repr_text,
            storage_format_kwargs_names=names,
            )

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

    @property
    def _keyword_argument_names(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatAgent(self)
        keyword_argument_names = list(agent.signature_keyword_names)
        if 'client' in keyword_argument_names:
            keyword_argument_names.remove('client')
        if 'tweak_pairs' in keyword_argument_names:
            keyword_argument_names.remove('tweak_pairs')
        keyword_argument_names = tuple(keyword_argument_names)
        return keyword_argument_names

    @property
    def _lilypond_format(self):
        from abjad.tools import systemtools
        from abjad.tools import scoretools
        # make sure note head has pitch
        assert self.written_pitch
        result = []
        # format chord note head with optional tweaks
        if self.is_parenthesized:
            result.append(r'\parenthesize')
        if isinstance(self._client, scoretools.Chord):
            for key, value in vars(self.tweak).items():
                if not key.startswith('_'):
                    result.append(
                        r'\tweak %s %s' % (
                        systemtools.LilyPondFormatManager.format_lilypond_attribute(key),
                        systemtools.LilyPondFormatManager.format_lilypond_value(value)),
                        )
        # format note head pitch
        kernel = format(self.written_pitch)
        if self.is_forced:
            kernel += '!'
        if self.is_cautionary:
            kernel += '?'
        result.append(kernel)
        result = '\n'.join(result)
        # return formatted note head
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Client of note-head.

        ::

            >>> note_head.client is None
            True

        Returns note, chord or none.
        '''
        return self._client

    @property
    def is_cautionary(self):
        r'''Gets and sets cautionary accidental flag.

        Gets cautionary accidental flag:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.is_cautionary is None
            True

        Sets cautionary accidental flag:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.is_cautionary = True

        Returns true or false.
        '''
        return self._is_cautionary

    @is_cautionary.setter
    def is_cautionary(self, arg):
        if arg is not None:
            arg = bool(arg)
        self._is_cautionary = arg

    @property
    def is_forced(self):
        r'''Gets and sets forced accidental flag.

        Gets forced accidental flag:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.is_forced is None
            True

        Sets forced accidental flag:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.is_forced = True

        Returns true or false.
        '''
        return self._is_forced

    @is_forced.setter
    def is_forced(self, arg):
        if arg is not None:
            arg = bool(arg)
        self._is_forced = arg

    @property
    def is_parenthesized(self):
        r'''Gets and sets forced accidental flag.

        Gets forced accidental flag:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.is_parenthesized is None
            True

        Sets forced accidental flag:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.is_parenthesized = True

        Returns true or false.
        '''
        return self._is_parenthesized

    @is_parenthesized.setter
    def is_parenthesized(self, arg):
        if arg is not None:
            arg = bool(arg)
        self._is_parenthesized = arg

    @property
    def named_pitch(self):
        r'''Named pitch of note-head.

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.named_pitch
            NamedPitch("cs''")

        Returns named pitch.
        '''
        return self.written_pitch

    @property
    def tweak(self):
        r'''LilyPond tweak reservoir of note-head.

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.tweak
            LilyPondNameManager()

        Returns LilyPond tweak reservoir.
        '''
        from abjad.tools import lilypondnametools
        if self._tweak is None:
            self._tweak = lilypondnametools.LilyPondNameManager()
        return self._tweak

    @property
    def written_pitch(self):
        r'''Gets and sets written pitch of note-head.

        Gets written pitch of note-head:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.written_pitch
            NamedPitch("cs''")

        Sets written pitch of note-head:

        ::

            >>> note_head = scoretools.NoteHead("cs''")
            >>> note_head.written_pitch = "d''"
            >>> note_head.written_pitch
            NamedPitch("d''")

        Returns named pitch.
        '''
        return self._written_pitch

    @written_pitch.setter
    def written_pitch(self, arg):
        from abjad.tools import pitchtools
        written_pitch = pitchtools.NamedPitch(arg)
        self._written_pitch = written_pitch
