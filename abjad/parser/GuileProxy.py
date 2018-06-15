from typing import Callable, Dict  # noqa
from abjad import core
from abjad import indicators as abjad_indicators
from abjad import pitch as abjad_pitch
from abjad.system.AbjadObject import AbjadObject
from abjad.top import attach


# TODO: should not inherit from AbjadObject because no slots
class GuileProxy(AbjadObject):
    """
    Emulates LilyPond music functions.

    Used internally by LilyPondParser.

    Not composer-safe.
    """

    ### CLASS VARIABLES ###

    _function_name_mapping = {}  # type: Dict[str, Callable]

    ### INITIALIZER ###

    def __init__(self, client=None):
        self.client = client

    ### SPECIAL METHODS ###

    def __call__(self, function_name, arguments):
        """
        Calls Guile proxy on ``function_name`` with ``arguments``.

        Returns function output.
        """
        if hasattr(self, function_name[1:]):
            result = getattr(self, function_name[1:])(*arguments)
            return result
        elif function_name[1:] in self._function_name_mapping:
            function_name = function_name[1:]
            result = getattr(self, function_name)(*arguments)
            return result
        message = 'LilyPondParser can not emulate music function: {}.'
        message = message.format(function_name)
        raise Exception(message)

    ### FUNCTION EMULATORS ###

    def acciaccatura(self, music):
        r"""
        Handles LilyPond ``\acciaccatura`` command.
        """
        grace = core.AcciaccaturaContainer(music[:])
        return grace

    # afterGrace?

    def appoggiatura(self, music):
        r"""
        Handles LilyPond ``\appoggiatura`` command.
        """
        grace = core.AppoggiaturaContainer(music[:])
        return grace

    def bar(self, string):
        r"""
        Handles LilyPond ``\bar`` command.
        """
        return abjad_indicators.BarLine(string)

    def breathe(self):
        r"""
        Handles LilyPond ``\breathe`` command.
        """
        return abjad_indicators.LilyPondLiteral(r'\breathe', 'after')

    def clef(self, string):
        r"""
        Handles LilyPond ``\clef`` command.
        """
        return abjad_indicators.Clef(string)

    def grace(self, music):
        r"""
        Handles LilyPond ``\grace`` command.
        """
        assert isinstance(music, core.Container)
        leaves = music[:]
        music[:] = []
        return core.GraceContainer(leaves)

    def key(self, notename_pitch, number_list):
        r"""
        Handles LilyPond ``\key`` command.
        """
        if number_list is None:
            number_list = 'major'
        return abjad_indicators.KeySignature(notename_pitch, number_list)

    def language(self, string):
        r"""
        Handles LilyPond ``\language`` command.
        """
        if string in self.client._language_pitch_names:
            self.client._pitch_names = \
                self.client._language_pitch_names[string]
        # try reparsing the next note name, if a note name immediately follows
        lookahead = self.client._parser.lookahead
        if lookahead.type == 'STRING':
            if lookahead.value in self.client._pitch_names:
                lookahead.type = 'NOTENAME_PITCH'
                lookahead.value = self.client._pitch_names[lookahead.value]

    def makeClusters(self, music):
        r"""
        Handles LilyPond ``\makeClusters`` command.
        """
        return core.Cluster(music[:])

    def mark(self, label):
        r"""
        Handles LilyPond ``\mark`` command.
        """
        if label is None:
            label = '\default'
        return abjad_indicators.LilyPondLiteral(r'\mark %s' % label)

    def oneVoice(self):
        r"""
        Handles LilyPond ``\oneVoice`` command.
        """
        return abjad_indicators.LilyPondLiteral(r'\oneVoice')

    # pitchedTrill

    def relative(self, pitch, music):
        r"""
        Handles LilyPond ``\relative`` command.
        """
        # We should always keep track of the last chord entered.
        # When there are repeated chords (via q),
        # we add the last chord as a key in a _repeated_chords dictionary.
        # Then, we associate a list with the chord "key" in the dict,
        # and append a reference to the repeated chord.

        # Should the referenced chord appear in a relative block,
        # we relativize that chord, and update any repeated chords
        # we've added to its list of referencing chords.

        # The parser's "last_chord" variable will now reflect the
        # relativized pitches of the original referenced chord,
        # and so any new chord repetitions following the \relative block
        # should result in matching absolute pitches to both the "last_chord"
        # and any other repetitions.

        if self._is_unrelativable(music):
            return music

        def recurse(component, pitch):
            if self._is_unrelativable(component):
                return pitch
            elif isinstance(component, (core.Chord, core.Note)):
                pitch = self._make_relative_leaf(component, pitch)
                if component in self.client._repeated_chords:
                    for repeated_chord in \
                        self.client._repeated_chords[component]:
                        repeated_chord.written_pitches = \
                            component.written_pitches
            elif isinstance(component, core.Container):
                for child in component:
                    pitch = recurse(child, pitch)
            return pitch

        pitch = recurse(music, pitch)

        self._make_unrelativable(music)

        return music

    def skip(self, duration):
        r"""
        Handles LilyPond ``\skip`` command.
        """
        leaf = core.Skip(duration.duration)
        if duration.multiplier is not None:
            attach(duration.multiplier, leaf)
        return leaf

    def slashed_grace_container(self, music):
        r"""
        Handles LilyPond ``\slahsedGrace`` command.
        """
        grace = core.GraceContainer(music[:])
        return grace

    def time(self, number_list, fraction):
        r"""
        Handles LilyPond ``\time`` command.
        """
        n, d = fraction.numerator, fraction.denominator
        return abjad_indicators.TimeSignature((n, d))

    def times(self, fraction, music):
        r"""
        Handles LilyPond ``\times`` command.
        """
        n, d = fraction.numerator, fraction.denominator
        if (not isinstance(music, core.Context) and
            not isinstance(music, core.Leaf)
            ):
            assert isinstance(music, core.Container), repr(music)
            leaves = music[:]
            music[:] = []
            return core.Tuplet((n, d), leaves)
        return core.Tuplet((n, d), [music])

    def transpose(self, from_pitch, to_pitch, music):
        r"""
        Handles LilyPond ``\transpose`` command.
        """
        from abjad import parser as abjad_parser
        def recurse(music):
            key_signatures = music._get_indicators(abjad_indicators.KeySignature)
            if key_signatures:
                for x in key_signatures:
                    tonic = abjad_pitch.NamedPitch((x.tonic.name, 4))
                    # TODO: cheating to assign to a read-only property
                    x._tonic = abjad_parser.LilyPondParser._transpose_enharmonically(
                        from_pitch, to_pitch, tonic).pitch_class
            if isinstance(music, core.Note):
                music.written_pitch = \
                    abjad_parser.LilyPondParser._transpose_enharmonically(
                        from_pitch, to_pitch, music.written_pitch)
            elif isinstance(music, core.Chord):
                for note_head in music.note_heads:
                    note_head.written_pitch = \
                        abjad_parser.LilyPondParser._transpose_enharmonically(
                            from_pitch, to_pitch, note_head.written_pitch)
            elif isinstance(music, core.Container):
                for x in music:
                    recurse(x)
        self._make_unrelativable(music)
        recurse(music)
        return music

    # transposition

    # tweak

    def voiceFour(self):
        r"""
        Handles LilyPond ``\voiceFour`` command.
        """
        return abjad_indicators.LilyPondLiteral(r'\voiceFour')

    def voiceOne(self):
        r"""
        Handles LilyPond ``\voiceOnce`` command.
        """
        return abjad_indicators.LilyPondLiteral(r'\voiceOne')

    def voiceThree(self):
        r"""
        Handles LilyPond ``\voiceThree`` command.
        """
        return abjad_indicators.LilyPondLiteral(r'\voiceThree')

    def voiceTwo(self):
        r"""
        Handles LilyPond ``\voiceTwo`` command.
        """
        return abjad_indicators.LilyPondLiteral(r'\voiceTwo')

    ### HELPER FUNCTIONS ###

    def _is_unrelativable(self, music):
        annotations = music._get_indicators(dict)
        keys = [list(_.keys())[0] for _ in annotations]
        if 'UnrelativableMusic' in keys:
            return True
        return False

    def _make_relative_leaf(self, leaf, pitch):
        if self._is_unrelativable(leaf):
            return pitch
        elif isinstance(leaf, core.Note):
            pitch = self._to_relative_octave(leaf.written_pitch, pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, core.Chord):
            # TODO: This is not ideal w/r/t post events as LilyPond does
            # not sort chord contents
            chord_pitches = self.client._chord_pitch_orders[leaf]
            for i, chord_pitch in enumerate(chord_pitches):
                pitch = self._to_relative_octave(chord_pitch, pitch)
                chord_pitches[i] = pitch
            leaf.written_pitches = chord_pitches
            pitch = min(leaf.written_pitches)
        return pitch

    def _make_unrelativable(self, music):
        if not self._is_unrelativable(music):
            annotation = {'UnrelativableMusic': True}
            attach(annotation, music)

    def _to_relative_octave(self, pitch, reference):
        if pitch.pitch_class.number > reference.pitch_class.number:
            pair = (pitch.pitch_class.name, reference.octave.number)
            up_pitch = abjad_pitch.NamedPitch(pair)
            pair = (pitch.pitch_class.name, reference.octave.number - 1)
            down_pitch = abjad_pitch.NamedPitch(pair)
            up_octave = up_pitch.octave.number
            down_octave = down_pitch.octave.number
        else:
            pair = (pitch.pitch_class.name, reference.octave.number + 1)
            up_pitch = abjad_pitch.NamedPitch(pair)
            pair = (pitch.pitch_class.name, reference.octave.number)
            down_pitch = abjad_pitch.NamedPitch(pair)
            up_octave = up_pitch.octave.number
            down_octave = down_pitch.octave.number
        if abs(
                float(up_pitch._get_diatonic_pitch_number()) -
                float(reference._get_diatonic_pitch_number())) < \
            abs(
                float(down_pitch._get_diatonic_pitch_number()) -
                float(reference._get_diatonic_pitch_number())):
            pair = (
                up_pitch.pitch_class.name,
                up_octave + pitch.octave.number - 3,
                )
            pitch = abjad_pitch.NamedPitch(pair)
        else:
            pair = (
                down_pitch.pitch_class.name,
                down_octave + pitch.octave.number - 3,
                )
            pitch = abjad_pitch.NamedPitch(pair)
        return pitch
