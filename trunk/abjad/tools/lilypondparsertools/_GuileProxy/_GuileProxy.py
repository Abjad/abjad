from abjad import *
from abjad.tools.contexttools._Context import _Context


class _GuileProxy(object):


    def __init__(self, client):
        self.client = client


    ### OVERRIDES ###


    def __call__(self, function_name, args):
        signature = self.client._current_module[function_name[1:]]['signature'][1:]
        print '_GuileProxy: %s, %s, %s' % (function_name, signature, args)
        if hasattr(self, function_name[1:]):
            result = getattr(self, function_name[1:])(*args)
            # print result
            return result
        raise Exception("LilyPondParser can't emulate music function %s." % function_name)


    ### FUNCTION EMULATORS ###


    def acciaccatura(self, music):
        grace = gracetools.Grace(music[:])
        grace.kind = 'acciaccatura'
        return grace


    # afterGrace


    def appoggiatura(self, music):
        grace = gracetools.Grace(music[:])
        grace.kind = 'appoggiatura'
        return grace


    def bar(self, string):
        return marktools.BarLine(string)


    def breathe(self):
        return marktools.LilyPondCommandMark('breathe', 'before')


    def clef(self, string):
        return contexttools.ClefMark(string)


    def grace(self, music):
        return gracetools.Grace(music[:])


    def key(self, notename_pitch, number_list):
        if number_list is None:
            number_list = 'major'
        return contexttools.KeySignatureMark(notename_pitch, number_list)


    def language(self, string):
        if string in self.client._language_pitch_names:
            self.client._parser_variables['language'] = string


    def makeClusters(self, music):
        return containertools.Cluster(music[:])


    def mark(self, label):
        if label is None:
            label = '\default'
        return marktools.LilyPondCommandMark('mark %s' % label)


    # pitchedTrill


    def relative(self, pitch, music):
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
            elif isinstance(component, (Chord, Note)):
                pitch = self._make_relative_leaf(component, pitch)
                if component in self.client._repeated_chords:
                    for repeated_chord in self.client._repeated_chords[component]:
                        repeated_chord.written_pitches = component.written_pitches
            elif isinstance(component, Container):
                for child in component:
                    pitch = recurse(child, pitch)
            return pitch
        
        pitch = recurse(music, pitch)

        annotation = self._make_unrelativable(music)
        self.client._annotations.append(annotation)

        return music


    def slashedGrace(self, music):
        grace = gracetools.Grace(music[:])
        grace.kind = 'slashedGrace'
        return grace


    def time(self, number_list, fraction):
        return contexttools.TimeSignatureMark(fraction)


    def times(self, fraction, music):
        if not isinstance(music, _Context):
            return tuplettools.Tuplet(fraction, music[:])
        return tuplettools.Tuplet(fraction, [music])


    def transpose(self, from_pitch, to_pitch, music):
        annotation = self._make_unrelativable(music)
        self.client._annotations.append(annotation)

        interval = from_pitch - to_pitch

        def recurse(music):
            key_signatures = contexttools.get_key_signature_marks_attached_to_component(music)
            if key_signatures:
                for x in key_signatures:
                    x.tonic += interval
            if isinstance(music, Note):
                music.written_pitch += interval
            elif isinstance(music, Chord):
                for note_head in music.note_heads:
                    note_head.written_pitch += interval
            elif isinstance(music, Container):
                for x in music:
                    recurse(x)

        recurse(music)

        return music


    # transposition


    # tweak

    
    ### HELPER FUNCTIONS ###


    def _is_unrelativable(self, music):
        annotations = marktools.get_annotations_attached_to_component(music)
        if 'UnrelativableMusic' in [x.name for x in annotations]:
            return True
        return False


    def _make_relative_leaf(self, leaf, pitch):
        if self._is_unrelativable(leaf):
            return pitch
        elif isinstance(leaf, Note):
            pitch = self._to_relative_octave(leaf.written_pitch, pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, Chord):
            # TODO: This is not ideal w/r/t post events as LilyPond does not sort chord contents
            chord_pitches = self.client._chord_pitch_orders[leaf]
            for i, chord_pitch in enumerate(chord_pitches):
                pitch = self._to_relative_octave(chord_pitch, pitch)
                chord_pitches[i] = pitch
            leaf.written_pitches = chord_pitches
        return pitch


    def _make_unrelativable(self, music):
        if not self._is_unrelativable(music):
            return marktools.Annotation('UnrelativableMusic')(music)
        

    def _to_relative_octave(self, pitch, reference):
        if pitch.chromatic_pitch_class_number > reference.chromatic_pitch_class_number:
            up_pitch = pitchtools.NamedChromaticPitch(
                pitch.chromatic_pitch_class_name, reference.octave_number)
            down_pitch = pitchtools.NamedChromaticPitch(
                pitch.chromatic_pitch_class_name, reference.octave_number - 1)
        else:
            up_pitch = pitchtools.NamedChromaticPitch(
                pitch.chromatic_pitch_class_name, reference.octave_number + 1)
            down_pitch = pitchtools.NamedChromaticPitch(
                pitch.chromatic_pitch_class_name, reference.octave_number)

        if abs(up_pitch - reference) < abs(down_pitch - reference):
            pitch = up_pitch + (12 * (pitch.octave_number - 3))
        else:
            pitch = down_pitch + (12 * (pitch.octave_number - 3))

        return pitch

