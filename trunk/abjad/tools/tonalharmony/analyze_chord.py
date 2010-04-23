from abjad.exceptions import TonalHarmonyError
from abjad.tools import pitchtools
from abjad.tools.tonalharmony.ChordClass import ChordClass
from abjad.tools.tonalharmony.chord_class_cardinality_to_extent import \
   chord_class_cardinality_to_extent
from abjad.tools.tonalharmony.diatonic_interval_class_segment_to_chord_quality_string import \
   diatonic_interval_class_segment_to_chord_quality_string


def analyze_chord(expr):
   '''.. versionadded:: 1.1.2

   Analyze `expr` and return chord class. ::

      abjad> chord = Chord([7, 10, 12, 16], (1, 4))
      abjad> tonalharmony.analyze_chord(chord)
      CDominantSeventhInSecondInversion

   Return none when no tonal chord is understood. ::

      abjad> chord = Chord(['c', 'cs', 'd'], (1, 4))
      abjad> tonalharmony.analyze_chord(chord) is None
      True
   '''

   pitches = pitchtools.get_pitches(expr)
   npcset = pitchtools.NamedPitchClassSet(pitches)

   ordered_npcs = pitchtools.NamedPitchClassSegment([ ])
   letters = ('c', 'e', 'g', 'b', 'd', 'f', 'a')
   for letter in letters:
      for npc in npcset:
         if npc.letter == letter:
            ordered_npcs.append(npc)

   for x in range(len(ordered_npcs)):
      ordered_npcs = ordered_npcs.rotate(1)
      if ordered_npcs.diatonic_interval_class_segment.is_tertian:
         break
   else:
      #raise TonalHarmonyError('expr is not tertian harmony: %s' % str(expr))
      return None

   root = ordered_npcs[0]
   bass = min(pitches).named_pitch_class
   inversion = ordered_npcs.index(bass)
   dic_seg =  ordered_npcs.diatonic_interval_class_segment
   cardinality = len(ordered_npcs)
   extent = chord_class_cardinality_to_extent(cardinality)
   quality = diatonic_interval_class_segment_to_chord_quality_string(dic_seg)

   return ChordClass(root, quality, extent, inversion)
