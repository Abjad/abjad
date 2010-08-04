from abjad.Pitch import Pitch
from abjad.marks import KeySignature
from abjad.tools.pitchtools.HarmonicDiatonicIntervalSegment import HarmonicDiatonicIntervalSegment
from abjad.tools.pitchtools.MelodicDiatonicIntervalSegment import MelodicDiatonicIntervalSegment
from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
from abjad.tools.pitchtools.NamedPitchClassSegment import NamedPitchClassSegment
from abjad.tools.tonalitytools.ScaleDegree import ScaleDegree
import copy


class Scale(NamedPitchClassSegment):
   '''.. versionadded:: 1.1.2

   Abjad model of diatonic scale.
   '''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], KeySignature):
         self._init_by_key_signature(args[0])
      elif len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_key_signature(args[0].key_signature)
      elif len(args) == 2:
         key_signature = KeySignature(*args)
         self._init_by_key_signature(key_signature)
      else:
         raise TypeError

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self._capital_name, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _capital_name(self):
      letter = self.key_signature.tonic.name.title( )
      mode = self.key_signature.mode.mode_name_string.title( )
      return '%s%s' % (letter, mode)

   ## PRIVATE METHODS ##

   def _init_by_key_signature(self, key_signature):
      self._key_signature = key_signature
      npcs = [key_signature.tonic]
      for mdi in key_signature.mode.melodic_diatonic_interval_segment[:-1]:
         named_pitch_class = npcs[-1] + mdi
         npcs.append(named_pitch_class)
      self.extend(npcs)

   ## PUBLIC ATTRIBUTES ##

   @property
   def diatonic_interval_class_segment(self):
      from abjad.tools import listtools
      from abjad.tools import pitchtools
      dics = [ ]
      for left, right in listtools.pairwise(self, mode = 'wrap'):
         dic = left - right
         dics.append(dic)
      dicg = pitchtools.DiatonicIntervalClassSegment(dics)
      return dicg

   @property
   def dominant(self):
      return self[4]

   @property
   def key_signature(self):
      return self._key_signature

   @property
   def leading_tone(self):
      return self[-1]

   @property
   def mediant(self):
      return self[2]

   @property
   def subdominant(self):
      return self[3]
   
   @property
   def submediant(self):
      return self[5]

   @property
   def superdominant(self):
      return self[1]

   @property
   def tonic(self):
      return self[0]

   ## PUBLIC METHODS ##

   def named_pitch_class_to_scale_degree(self, *args):
      foreign_pitch_class = NamedPitchClass(*args)
      letter = foreign_pitch_class.letter
      for i, pc in enumerate(self):
         if pc.letter == letter:
            native_pitch_class = pc
            scale_degree_index = i
            scale_degree_number = scale_degree_index + 1
            break
      native_pitch = Pitch(native_pitch_class, 4)
      foreign_pitch = Pitch(foreign_pitch_class, 4)
      accidental = foreign_pitch.accidental - native_pitch.accidental
      return ScaleDegree(accidental, scale_degree_number)

   def scale_degree_to_named_pitch_class(self, *args):
      scale_degree = ScaleDegree(*args)
      scale_index = scale_degree.number - 1
      pitch_class = self[scale_index]
      pitch_class = pitch_class.apply_accidental(scale_degree.accidental)
      return pitch_class
