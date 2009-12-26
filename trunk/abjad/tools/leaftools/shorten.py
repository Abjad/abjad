from abjad.rest import Rest


def shorten(leaf, prolated_duration):
   r'''.. versionadded:: 1.1.2

   Split `leaf` at `prolated_duration`.
   Cast leaves after `prolated_duration` to rests.
   Return list of leaves to left of `prolated_durration`,
   list of leaves to right of `prolated_duration`. ::

      abjad> t = Staff(construct.scale(4))
      abjad> Slur(t[:])
      Slur(c'8, d'8, e'8, f'8)
      abjad> f(t)
      \new Staff {
         c'8 (
         d'8
         e'8
         f'8 )
      }

   ::

      abjad> leaftools.shorten(t.leaves[1], (1, 32))
      ([Note(d', 32)], [Note(d', 16.)])
      abjad> f(t)
      \new Staff {
         c'8 (
         d'32
         r16.
         e'8
         f'8 )
      }

   .. todo:: implement ``leaftools.shorten_left( )``.
   '''

   from abjad.tools.split.unfractured_at_duration import unfractured_at_duration

   left, right = unfractured_at_duration(leaf, prolated_duration)
   for leaf in right:
      Rest(leaf)

   return left, right
