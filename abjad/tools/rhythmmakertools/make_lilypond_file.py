# -*- coding: utf-8 -*-
import copy


def make_lilypond_file(
    selections,
    divisions=None,
    attach_lilypond_voice_commands=None,
    implicit_scaling=None,
    pitched_staff=None,
    simultaneous_selections=None,
    time_signatures=None,
    ):
    r'''Makes LilyPond file.

    ..  container:: example

        Makes rhythmic staff:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(exponent=1)
            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> selections = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file[Score]
            >>> f(score)
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    {
                        \time 4/8
                        s1 * 1/2
                    }
                    {
                        \time 1/4
                        s1 * 1/4
                    }
                }
                \new RhythmicStaff {
                    {
                        \time 3/4
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 1/4
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                }
            >>

    ..  container:: example

        Set time signatures explicitly:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(exponent=1)
            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> selections = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     [(6, 8), (4, 8), (2, 8)],
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file[Score]
            >>> f(score)
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 6/8
                        s1 * 3/4
                    }
                    {
                        \time 4/8
                        s1 * 1/2
                    }
                    {
                        \time 2/8
                        s1 * 1/4
                    }
                }
                \new RhythmicStaff {
                    {
                        \time 6/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 2/8
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                }
            >>

    ..  container:: example

        Makes pitched staff:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(exponent=1)
            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> selections = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     pitched_staff=True,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file[Score]
            >>> f(score)
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    {
                        \time 4/8
                        s1 * 1/2
                    }
                    {
                        \time 1/4
                        s1 * 1/4
                    }
                }
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 1/4
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                }
            >>

    ..  container:: example

        Makes simultaneous voices:

        ::

            >>> maker_1 = rhythmmakertools.EvenRunRhythmMaker(exponent=1)
            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> selection_1 = select(maker_1(divisions))
            >>> for note in iterate(selection_1).by_class(Note):
            ...     note.written_pitch = NamedPitch("e'")
            ...
            >>> maker_2 = rhythmmakertools.EvenRunRhythmMaker(exponent=2)
            >>> selection_2 = select(maker_2(divisions))
            >>> selections = {
            ...     'Voice 1': selection_1,
            ...     'Voice 2': selection_2,
            ... }
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> voice_1 = lilypond_file['Voice 1']
            >>> attach(LilyPondCommand('voiceOne'), voice_1)
            >>> voice_2 = lilypond_file['Voice 2']
            >>> attach(LilyPondCommand('voiceTwo'), voice_2)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    {
                        \time 4/8
                        s1 * 1/2
                    }
                    {
                        \time 1/4
                        s1 * 1/4
                    }
                }
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            e'8 [
                            e'8
                            e'8
                            e'8
                            e'8
                            e'8 ]
                        }
                        {
                            e'16 [
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16
                            e'16 ]
                        }
                        {
                            e'8 [
                            e'8 ]
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                        {
                            c'32 [
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32 ]
                        }
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                >>
            >>

    Used in rhythm-maker docs.

    Returns LilyPond file.
    '''
    import abjad
    if isinstance(selections, list):
        for selection in selections:
            if not isinstance(selection, abjad.Selection):
                message = 'must be selection: {!r}.'
                message = message.format(selection)
                raise TypeError(message)
    elif isinstance(selections, dict):
        for selection in selections.values():
            if not isinstance(selection, abjad.Selection):
                message = 'must be selection: {!r}.'
                message = message.format(selection)
                raise TypeError(message)
    else:
        message = 'must be list or dictionary: {!r}.'
        message = message.format(selections)
        raise TypeError(message)
    score = abjad.Score()
    package = abjad.lilypondfiletools
    lilypond_file = package.make_floating_time_signature_lilypond_file(score)
    if pitched_staff is None:
        for note in abjad.iterate(selections).by_class(
            abjad.Note,
            with_grace_notes=True,
            ):
            if note.written_pitch != abjad.NamedPitch("c'"):
                pitched_staff = True
                break
    if isinstance(selections, list):
        if divisions is None:
            duration = sum([_.get_duration() for _ in selections])
            divisions = [duration]
        time_signatures = time_signatures or divisions
        measures = abjad.scoretools.make_spacer_skip_measures(
            time_signatures,
            implicit_scaling=implicit_scaling,
            )
        if pitched_staff:
            staff = abjad.Staff(measures)
        else:
            staff = abjad.Staff(measures, context_name='RhythmicStaff')
        selections = abjad.Sequence(selections).flatten()
        selections_ = copy.deepcopy(selections)
        try:
            measures = abjad.mutate(staff).replace_measure_contents(selections)
        except StopIteration:
            if pitched_staff:
                staff = abjad.Staff(selections_)
            else:
                staff = abjad.Staff(selections_, context_name='RhythmicStaff')
    elif isinstance(selections, dict):
        voices = []
        for voice_name in sorted(selections):
            selections_ = selections[voice_name]
            selections_ = abjad.Sequence(selections_).flatten()
            selections_ = copy.deepcopy(selections_)
            voice = abjad.Voice(selections_, name=voice_name)
            if attach_lilypond_voice_commands:
                voice_name_to_command_string = {
                    'Voice 1': 'voiceOne',
                    'Voice 2': 'voiceTwo',
                    'Voice 3': 'voiceThree',
                    'Voice 4': 'voiceFour',
                    }
                command_string = voice_name_to_command_string.get(voice_name)
                if command_string:
                    command = abjad.LilyPondCommand(command_string)
                    abjad.attach(command, voice)
            voices.append(voice)
        staff = abjad.Staff(voices, is_simultaneous=True)
        if divisions is None:
            duration = abjad.inspect_(staff).get_duration()
            divisions = [duration]
    else:
        message = 'must be list or dictionary of selections: {!r}.'
        message = message.format(selections)
        raise TypeError(message)
    score.append(staff)
    assert isinstance(divisions, (tuple, list)), repr(divisions)
    time_signatures = time_signatures or divisions
    context = abjad.scoretools.Context(context_name='TimeSignatureContext')
    measures = abjad.scoretools.make_spacer_skip_measures(
        time_signatures,
        implicit_scaling=implicit_scaling,
        )
    context.extend(measures)
    score.insert(0, context)
    return lilypond_file
