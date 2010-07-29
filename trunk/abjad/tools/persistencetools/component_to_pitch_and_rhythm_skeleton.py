from abjad.chord import Chord
from abjad.component import _Component
from abjad.leaf import _Leaf
from abjad.measure.rigid.measure import RigidMeasure
from abjad.note import Note
from abjad.tuplet.fd.tuplet import FixedDurationTuplet
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


def component_to_pitch_and_rhythm_skeleton(component):
   r'''.. versionadded:: 1.1.2

   Make pitch and rhythm skeleton of any Abjad `component`.

   Thin, bare-bones alternative to built-in pickle and cPickle modules. ::

      abjad> tuplet = FixedDurationTuplet((3, 8), macros.scale(4))
      abjad> measure = RigidMeasure((6, 16), [tuplet])   
      abjad> staff = Staff([measure])   
      abjad> score = Score(staff * 2)   
      abjad> pitchtools.diatonicize(score)

   ::

      abjad> skeleton = persistencetools.component_to_pitch_and_rhythm_skeleton(score)
      abjad> print skeleton
      Score([
         Staff([
            RigidMeasure(Meter(6, 16), [
               FixedDurationTuplet(Rational(3, 8), [
                  Note(('c', 4), Rational(1, 8)),
                  Note(('d', 4), Rational(1, 8)),
                  Note(('e', 4), Rational(1, 8)),
                  Note(('f', 4), Rational(1, 8))
               ])
            ])
         ]),
         Staff([
            RigidMeasure(Meter(6, 16), [
               FixedDurationTuplet(Rational(3, 8), [
                  Note(('g', 4), Rational(1, 8)),
                  Note(('a', 4), Rational(1, 8)),
                  Note(('b', 4), Rational(1, 8)),
                  Note(('c', 5), Rational(1, 8))
               ])
            ])
         ])
      ])

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
                  c'8
                  d'8
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

   .. versionchanged:: 1.1.2
      renamed ``persistencetools.pitch_and_rhythm_skeleton( )`` to
      ``persistencetools.component_to_pitch_and_rhythm_skeleton( )``.
   '''
   
   if not isinstance(component, _Component):
      raise TypeError('must be Abjad component.')

   if isinstance(component, _Leaf):
      return _leaf_skeleton(component)
   else:
      return _container_skeleton(component)

   
def _leaf_skeleton(leaf):
   class_name = leaf.__class__.__name__
   duration = repr(leaf.duration.written)
   if isinstance(leaf, Note):
      return '%s(%s, %s)' % (class_name, leaf.pitch.pair, duration)
   elif isinstance(leaf, Chord):
      return '%s(%s, %s)' % (class_name, leaf.pairs, duration)
   else:
      return '%s(%s)' % (class_name, duration)


def _container_skeleton(container):
   class_name = container.__class__.__name__
   contents = [ ]
   for x in container:
      skeleton = component_to_pitch_and_rhythm_skeleton(x)
      skeleton = skeleton.split('\n')
      skeleton = ['\t' + line for line in skeleton]
      skeleton = '\n'.join(skeleton)
      contents.append(skeleton)
   contents = ',\n'.join(contents)
   if isinstance(container, RigidMeasure):
      meter= repr(container.meter.effective)
      return '%s(%s, [\n%s\n])' % (class_name, meter, contents)
   elif isinstance(container, FixedDurationTuplet):
      duration = repr(container.duration.target)
      return '%s(%s, [\n%s\n])' % (class_name, duration, contents)
   elif isinstance(container, FixedMultiplierTuplet):
      multiplier = repr(container.duration.multiplier)
      return '%s(%s, [\n%s\n])' % (class_name, multiplier, contents)
   else:
      return '%s([\n%s\n])' % (class_name, contents)
