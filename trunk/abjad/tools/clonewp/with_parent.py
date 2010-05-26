from abjad.meter import Meter
from abjad.tools import check
from abjad.tools import durtools
from abjad.tools import clone


def with_parent(components):
   r'''Copy thread-contiguous `components`.
   
   Return in newly created container equal to type of 
   first element in `copmonents`.

   If the parent of the first element in `components` is a tuplet then
   insure that the tuplet multiplier of the function output
   equals the tuplet multiplier of the parent of the 
   first element in `components`. ::

      voice = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 3)
      pitchtools.diatonicize(voice)
      beam = Beam(voice.leaves[:4])
      f(voice)
      \new Voice {
              \times 2/3 {
                      c'8 [
                      d'8
                      e'8
              }
              \times 2/3 {
                      f'8 ]
                      g'8
                      a'8
              }
              \times 2/3 {
                      b'8
                      c''8
                      d''8
              }
      }
      abjad> new_tuplet = clonewp.with_parent(voice.leaves[:2])
      abjad> new_tuplet
      FixedDurationTuplet(1/6, [c'8, d'8])
      abjad> f(new_tuplet)
      \times 2/3 {
              c'8 [
              d'8 ]
      }   

   Parent-contiguity is not required.
   Thread-contiguous `components` suffice. ::
   
      abjad> new_tuplet = clonewp.with_parent(voice.leaves[:5])
      abjad> new_tuplet
      FixedDurationTuplet(5/12, [c'8, d'8, e'8, f'8, g'8])
      abjad> f(new_tuplet)
      \times 2/3 {
              c'8 [
              d'8
              e'8
              f'8 ]
              g'8
      }

   .. note:: this function copies only the *immediate parent* of
      the first element in `components`. This function ignores any further 
      parentage of `components` above the immediate parent of `components`.
   '''

   from abjad.measure import _Measure

   # assert strictly contiguous components in same thread
   check.assert_components(components, contiguity = 'strict', share = 'thread')

   # remember parent
   parent = components[0].parentage.parent

   # new: remember parent multiplier, if any
   parent_multiplier = getattr(parent.duration, 'multiplier', 1)

   # new: remember parent denominator, if any
   if isinstance(parent, _Measure):
      parent_denominator = parent.meter.effective.denominator
   else:
      parent_denominator = None

   # remember parent's music
   parents_music = components[0].parentage.parent._music

   # strip parent of music temporarily
   parent._music = [ ]

   # copy parent without music
   result = clone.fracture([parent])[0]

   # give music back to parent
   parent._music = parents_music

   # populate result with references to input list
   result._music.extend(components)

   # populate result with deepcopy of input list and fracture spanners
   result = clone.fracture([result])[0]

   # point elements in result to result as new parent
   for element in result:
      element.parentage._switch(result)

   # new: resize result to match parent_multiplier, if resizable
   if result.__class__.__name__ == 'FixedDurationTuplet':
      result.duration.target = parent_multiplier * result.duration.contents
   elif result.__class__.__name__ == 'RigidMeasure':
      new_duration = parent_multiplier * result.duration.contents
      result.meter.forced = Meter(new_duration._n, new_duration._d)

   # new: rewrite result denominator, if available
   if parent_denominator is not None:
      old_meter = result.meter.effective
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = durtools.in_terms_of(old_meter_pair, parent_denominator)
      result.meter.forced = Meter(new_meter)

   # return copy
   return result
