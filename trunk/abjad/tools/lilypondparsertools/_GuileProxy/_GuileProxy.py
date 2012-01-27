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


    def transpose(self, to_pitch, from_pitch, music):
        return music


    # transposition


    # tweak

    
    ### HELPER FUNCTIONS ###


    def _is_unrelativable(self, music):
        annotations = marktools.get_annotations_attached_to_component(music)
        if 'UnrelativableMusic' in [x.name for x in annotations]:
            return True
        return False


    def _make_unrelativable(self, music):
        if not is_unrelativable(music):
            marktools.Annotation('UnrelativableMusic')(music)


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
        if abs(up_pitch.chromatic_pitch_class_number - reference.chromatic_pitch_class_number) < \
            abs(down_pitch.chromatic_pitch_class_number - reference.chromatic_pitch_class_number):
            return up_pitch + 12 * (pitch.octave_number - 4)
        else:
            return down_pitch + 12 * (pitch.octave_number - 4)
