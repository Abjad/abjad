from abjad.components._Component import _Component
from abjad.components._Leaf import _Leaf
from abjad.tools.componenttools._container_to_pitch_and_rhythm_skeleton import _container_to_pitch_and_rhythm_skeleton
from abjad.tools.componenttools._leaf_to_pitch_and_rhythm_skeleton import _leaf_to_pitch_and_rhythm_skeleton


def component_to_pitch_and_rhythm_skeleton_with_interface_attributes(component):
   r'''.. versionadded:: 1.1.2

   Make pitch and rhythm skeleton of any Abjad `component`.

   Include user settings as keyword arguments::

      abjad> tuplet = tuplettools.FixedDurationTuplet((3, 8), macros.scale(4))
      abjad> measure = RigidMeasure((6, 16), [tuplet])   
      abjad> staff = Staff([measure])   
      abjad> score = Score(staff * 2)   
      abjad> macros.diatonicize(score)
      abjad> note = score.leaves[0]
      abjad> note.override.beam.thickness = 3
      abjad> note.duration.multiplier = Rational(1, 2)
      abjad> note.harmonic.natural = True
      abjad> note.name = 'custom name'
      abjad> note.override.note_head.color = 'red'
      abjad> note.offset.prolated.foo = 'bar'
      abjad> next_note = score.leaves[1]
      abjad> next_note.duration.multiplier = Rational(3, 2)
      
   ::
      
      abjad> skeleton = componenttools.component_to_pitch_and_rhythm_skeleton_with_interface_attributes(score)
      abjad> print skeleton
      Score([
         Staff([
            RigidMeasure(Meter(6, 16), [
               tuplettools.FixedDurationTuplet(Rational(3, 8), [
                  Note(('c', 4), Rational(1, 8), 
                     beam__thickness = 3,
                     duration__multiplier = Rational(1, 2),
                     harmonic__natural = True,
                     name = 'custom name',
                     note_head__color = 'red',
                     offset__prolated__foo = 'bar'),
                  Note(('d', 4), Rational(1, 8), 
                     duration__multiplier = Rational(3, 2)),
                  Note(('e', 4), Rational(1, 8)),
                  Note(('f', 4), Rational(1, 8))
               ])
            ])
         ], 
         context = 'Staff'),
         Staff([
            RigidMeasure(Meter(6, 16), [
               tuplettools.FixedDurationTuplet(Rational(3, 8), [
                  Note(('g', 4), Rational(1, 8)),
                  Note(('a', 4), Rational(1, 8)),
                  Note(('b', 4), Rational(1, 8)),
                  Note(('c', 5), Rational(1, 8))
               ])
            ])
         ], 
         context = 'Staff')
      ], 
      context = 'Score',
      parallel = True)

   ::
      
      abjad> new = eval(skeleton)
      abjad> new 
      Score<<2>>
      
   ::
      
      abjad> f(new)
      \new Score <<
         \new Staff {
            {
               \time 6/16
               \fraction \times 3/4 {
                  \once \override Beam #'thickness = #3
                  \once \override NoteHead #'color = #red
                  c'8 * 1/2 \flageolet
                  d'8 * 3/2
                  e'8
                  f'8
               }
            }
         }
         \new Staff {
            {
               \time 6/16
               \fraction \times 3/4 {
                  g'8
                  a'8
                  b'8
                  c''8
               }
            }
         }
      >>
   '''
   
   if not isinstance(component, _Component):
      raise TypeError('must be Abjad component.')

   if isinstance(component, _Leaf):
      return _leaf_to_pitch_and_rhythm_skeleton(component, include_keyword_attributes = True)
   else:
      return _container_to_pitch_and_rhythm_skeleton(component, include_keyword_attributes = True)
