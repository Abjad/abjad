# -*- coding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools.scoretools.Leaf import Leaf
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_


class Chord(Leaf):
    r'''A chord.

    ..  container:: example

        ::

            >>> chord = Chord("<e' cs'' f''>4")
            >>> show(chord) # doctest: +SKIP

        ..  doctest::

            >>> print(format(chord))
            <e' cs'' f''>4

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = (
        '_note_heads',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.ly import drums
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import parse
        assert len(args) in (0, 1, 2)
        self._note_heads = scoretools.NoteHeadInventory(
            client=self,
            )
        if len(args) == 1 and isinstance(args[0], str):
            string = '{{ {} }}'.format(args[0])
            parsed = parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            args = [parsed[0]]
        are_cautionary = []
        are_forced = []
        are_parenthesized = []
        if len(args) == 1 and isinstance(args[0], Leaf):
            leaf = args[0]
            written_pitches = []
            written_duration = leaf.written_duration
            if 'written_pitch' in dir(leaf):
                written_pitches.append(leaf.note_head.written_pitch)
                are_cautionary = [leaf.note_head.is_cautionary]
                are_forced = [leaf.note_head.is_forced]
                are_parenthesized = [leaf.note_head.is_parenthesized]
            elif 'written_pitches' in dir(leaf):
                written_pitches.extend(x.written_pitch
                    for x in leaf.note_heads)
                are_cautionary = [x.is_cautionary for x in leaf.note_heads]
                are_forced = [x.is_forced for x in leaf.note_heads]
                are_parenthesized = [x.is_parenthesized for x in
                    leaf.note_heads]
        elif len(args) == 2:
            written_pitches, written_duration = args
            if isinstance(written_pitches, str):
                written_pitches = [x for x in written_pitches.split() if x]
            elif isinstance(written_pitches, type(self)):
                written_pitches = written_pitches.written_pitches
        elif len(args) == 0:
            written_pitches = [0, 4, 7]
            written_duration = durationtools.Duration(1, 4)
        else:
            message = 'can not initialize chord from {!r}.'
            message = message.format(args)
            raise ValueError(message)
        Leaf.__init__(self, written_duration)
        if not are_cautionary:
            are_cautionary = [None] * len(written_pitches)
        if not are_forced:
            are_forced = [None] * len(written_pitches)
        if not are_parenthesized:
            are_parenthesized = [None] * len(written_pitches)
        for written_pitch, is_cautionary, is_forced, is_parenthesized in zip(
            written_pitches, are_cautionary, are_forced, are_parenthesized):
            if not is_cautionary:
                is_cautionary = None
            if not is_forced:
                is_forced = None
            if not is_parenthesized:
                is_parenthesized = None
            if written_pitch not in drums:
                note_head = scoretools.NoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                    )
            else:
                note_head = scoretools.DrumNoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                    )
            self._note_heads.append(note_head)
        if len(args) == 1 and isinstance(args[0], Leaf):
            self._copy_override_and_set_from_leaf(args[0])

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self.written_pitches, self.written_duration)

    ### PRIVATE METHODS ###

    @staticmethod
    def _cast_defective_chord(chord):
        from abjad.tools import scoretools
        if isinstance(chord, Chord):
            note_head_count = len(chord.note_heads)
            if not note_head_count:
                return scoretools.Rest(chord)
            elif note_head_count == 1:
                return scoretools.Note(chord)
        return chord

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Leaf._copy_with_indicators_but_without_children_or_spanners(self)
        new.note_heads[:] = []
        for note_head in self.note_heads:
            new_note_head = copy.copy(note_head)
            new.note_heads.append(new_note_head)
        return new

    def _divide(self, pitch=None):
        from abjad.tools import scoretools
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        pitch = pitch or pitchtools.NamedPitch('b', 3)
        pitch = pitchtools.NamedPitch(pitch)
        treble = copy.copy(self)
        bass = copy.copy(self)
        detach(markuptools.Markup, treble)
        detach(markuptools.Markup, bass)
        if isinstance(treble, scoretools.Note):
            if treble.written_pitch < pitch:
                treble = scoretools.Rest(treble)
        elif isinstance(treble, scoretools.Rest):
            pass
        elif isinstance(treble, scoretools.Chord):
            for note_head in reversed(treble.note_heads):
                if note_head.written_pitch < pitch:
                    treble.note_heads.remove(note_head)
        else:
            raise TypeError
        if isinstance(bass, scoretools.Note):
            if pitch <= bass.written_pitch:
                bass = scoretools.Rest(bass)
        elif isinstance(bass, scoretools.Rest):
            pass
        elif isinstance(bass, scoretools.Chord):
            for note_head in reversed(bass.note_heads):
                if pitch <= note_head.written_pitch:
                    bass.note_heads.remove(note_head)
        else:
            raise TypeError
        treble = self._cast_defective_chord(treble)
        bass = self._cast_defective_chord(bass)
        up_markup = self._get_markup(direction=Up)
        up_markup = [copy.copy(markup) for markup in up_markup]
        down_markup = self._get_markup(direction=Down)
        down_markup = [copy.copy(markup) for markup in down_markup]
        for markup in up_markup:
            markup(treble)
        for markup in down_markup:
            markup(bass)
        return treble, bass

    def _format_before_slot(self, bundle):
        result = []
        result.append(self._format_grace_body())
        result.append(('comments', bundle.before.comments))
        commands = bundle.before.commands
        if inspect_(self).has_indicator(indicatortools.Tremolo):
            tremolo_command = self._format_repeat_tremolo_command()
            commands = list(commands)
            commands.append(tremolo_command)
            commands = tuple(commands)
        result.append(('commands', commands))
        result.append(('indicators', bundle.before.indicators))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        result.append(('spanners', bundle.before.spanners))
        return result

    def _format_close_brackets_slot(self, bundle):
        result = []
        if inspect_(self).has_indicator(indicatortools.Tremolo):
            brackets_close = ['}']
            result.append([('close brackets', ''), brackets_close])
        return result

    def _format_leaf_nucleus(self):
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
        result = []
        note_heads = self.note_heads
        if any('\n' in format(x) for x in note_heads):
            for note_head in note_heads:
                current_format = format(note_head)
                format_list = current_format.split('\n')
                format_list = [indent + x for x in format_list]
                result.extend(format_list)
            result.insert(0, '<')
            result.append('>')
            result = '\n'.join(result)
            result += str(self._formatted_duration)
        elif inspect_(self).has_indicator(indicatortools.Tremolo):
            reattack_duration = self._get_tremolo_reattack_duration()
            duration_string = reattack_duration.lilypond_duration_string
            durated_pitches = []
            for note_head in note_heads:
                durated_pitch = format(note_head) + duration_string
                durated_pitches.append(durated_pitch)
            tremolo = inspect_(self).get_indicator(indicatortools.Tremolo)
            if tremolo.is_slurred:
                durated_pitches[0] = durated_pitches[0] + r' \('
                durated_pitches[-1] = durated_pitches[-1] + r' \)'
            result = ' '.join(durated_pitches)
        else:
            result.extend([format(_) for _ in note_heads])
            result = '<%s>%s' % (' '.join(result), self._formatted_duration)
        # single string, but wrapped in list bc contribution
        return ['nucleus', [result]]

    def _format_open_brackets_slot(self, bundle):
        result = []
        if inspect_(self).has_indicator(indicatortools.Tremolo):
            brackets_open = ['{']
            result.append([('open brackets', ''), brackets_open])
        return result

    def _format_repeat_tremolo_command(self):
        tremolo = inspect_(self).get_indicator(indicatortools.Tremolo)
        reattack_duration = self._get_tremolo_reattack_duration()
        repeat_count = self.written_duration / reattack_duration / 2
        if not mathtools.is_integer_equivalent_expr(repeat_count):
            message = 'can not tremolo duration {} with {} beams.'
            message = message.format(self.written_duration, tremolo.beam_count)
            raise Exception(message)
        repeat_count = int(repeat_count)
        command = r'\repeat tremolo {}'.format(repeat_count)
        return command

    def _get_sounding_pitches(self):
        from abjad.tools import instrumenttools
        from abjad.tools import pitchtools
        if self._has_effective_indicator(indicatortools.IsAtSoundingPitch):
            return self.written_pitches
        else:
            instrument = self._get_effective(
                instrumenttools.Instrument)
            if instrument:
                sounding_pitch = instrument.sounding_pitch_of_written_middle_c
            else:
                sounding_pitch = pitchtools.NamedPitch('C4')
            interval = pitchtools.NamedPitch('C4') - sounding_pitch
            sounding_pitches = [
                pitchtools.transpose_pitch_carrier_by_interval(pitch, interval)
                for pitch in self.written_pitches
                ]
            return tuple(sounding_pitches)

    def _get_tremolo_reattack_duration(self):
        tremolos = inspect_(self).get_indicators(indicatortools.Tremolo)
        if not tremolos:
            return
        tremolo = tremolos[0]
        exponent = 2 + tremolo.beam_count
        denominator = 2 ** exponent
        reattack_duration = durationtools.Duration(1, denominator)
        return reattack_duration

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '<{}>{}'.format(self._summary, self._formatted_duration)

    @property
    def _compact_representation_with_tie(self):
        logical_tie = self._get_logical_tie()
        if 1 < len(logical_tie) and self is not logical_tie[-1]:
            return '{} ~'.format(self._body[0])
        else:
            return self._body[0]

    @property
    def _lilypond_format(self):
        return super(Chord, self)._lilypond_format

    @property
    def _summary(self):
        return ' '.join([str(x) for x in self.note_heads])

    ### PUBLIC PROPERTIES ###

    @property
    def note_heads(self):
        r'''Note heads in chord.

        ..  container:: example

            **Example 1.** Get note heads in chord:

            ::

                >>> chord = Chord("<g' c'' e''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> print(format(chord.note_heads))
                scoretools.NoteHeadInventory(
                    [
                        scoretools.NoteHead(
                            written_pitch=pitchtools.NamedPitch("g'"),
                            ),
                        scoretools.NoteHead(
                            written_pitch=pitchtools.NamedPitch("c''"),
                            ),
                        scoretools.NoteHead(
                            written_pitch=pitchtools.NamedPitch("e''"),
                            ),
                        ]
                    )

        ..  container:: example

            **Example 2.** Set note heads with pitch names:

            ::

                >>> chord = Chord("<g' c'' e''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> chord.note_heads = "c' d' fs'"
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                <c' d' fs'>4

        ..  container:: example

            **Example 3.** Set note heads with pitch numbers:

                >>> chord = Chord("<g' c'' e''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> chord.note_heads = [16, 17, 19]
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                <e'' f'' g''>4

        Set note heads with any iterable.

        Returns tuple.
        '''
        return self._note_heads

    @note_heads.setter
    def note_heads(self, note_heads):
        self._note_heads[:] = []
        if isinstance(note_heads, str):
            note_heads = note_heads.split()
        self.note_heads.extend(note_heads)

    @property
    def written_duration(self):
        r'''Written duration of chord.

        ..  container:: example

            **Example 1.** Get written duration:

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> chord.written_duration
                Duration(1, 4)

        ..  container:: example

            **Example 2.** Set written duration:

            ::

                >>> chord = Chord("<e' cs'' f''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> chord.written_duration = Duration(1, 16)
                >>> show(chord) # doctest: +SKIP

        Set duration.

        Returns duration.
        '''
        return Leaf.written_duration.fget(self)

    @written_duration.setter
    def written_duration(self, expr):
        Leaf.written_duration.fset(self, expr)

    @property
    def written_pitches(self):
        r'''Written pitches in chord.

        ..  container:: example

            **Example 1.** Get written pitches:

                >>> chord = Chord("<g' c'' e''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> chord.written_pitches
                PitchSegment(["g'", "c''", "e''"])

        ..  container:: example

            **Example 2.** Set written pitches with pitch names:

            ::

                >>> chord = Chord("<e' g' c''>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> chord.written_pitches = "f' b' d''"
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                <f' b' d''>4

            ::

                >>> chord.written_pitches
                PitchSegment(["f'", "b'", "d''"])

        Set written pitches with any iterable.

        Returns tuple.
        '''
        return pitchtools.PitchSegment(
            items=(note_head.written_pitch for note_head in self.note_heads),
            item_class=pitchtools.NamedPitch,
            )

    @written_pitches.setter
    def written_pitches(self, pitches):
        self.note_heads = pitches
