from abjad.component.component import _Component
#from abjad.navigator.dfs import depth_first_search
from depth_first import depth_first


def thread_from(component, klass = None):
   r'''.. versionadded:: 1.1.1

   Yield left-to-right components in the thread of `component`
   starting from `component`.

   When ``klass = None`` return all components in the thread of `component`.

   When `klass` is set to some other Abjad class,
   yield only `klass` instances in the thread of `component`. ::

      abjad> container = Container(Voice(construct.run(2)) * 2)
      abjad> container.parallel = True
      abjad> container[0].name = 'voice 1'
      abjad> container[1].name = 'voice 2'
      abjad> staff = Staff(container * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> print staff.format
      \new Staff {
              <<
                      \context Voice = "voice 1" {
                              c'8
                              d'8
                      }
                      \context Voice = "voice 2" {
                              e'8
                              f'8
                      }
              >>
              <<
                      \context Voice = "voice 1" {
                              g'8
                              a'8
                      }
                      \context Voice = "voice 2" {
                              b'8
                              c''8
                      }
              >>
      }

   Starting from the first leaf in score. ::

      abjad> for x in iterate.thread_from(staff.leaves[0], Note):
      ...     x
      ... 
      Note(c', 8)
      Note(d', 8)
      Note(g', 8)
      Note(a', 8)

   Starting from the second leaf in score. ::

      abjad> for x in iterate.thread_from(staff.leaves[1], Note):
      ...     x
      ... 
      Note(d', 8)
      Note(g', 8)
      Note(a', 8)

   Yield all components in thread. ::

      abjad> for x in iterate.thread_from(staff.leaves[0]):
      ...     x
      ... 
      Note(c', 8)
      Voice{2}
      Note(d', 8)
      Voice{2}
      Note(g', 8)
      Note(a', 8)
   
   Note that this function is a special type of depth-first search.

   Compare with :func:`iterate.thread() <abjad.tools.iterate.thread>`.
   '''

   ## set default class
   if klass is None:
      klass = _Component

   ## save thread signature of input component
   component_thread_signature = component.thread.signature

   ## iterate component depth-first allowing to crawl UP into score
   #for x in depth_first_search(component, capped = False):
   for x in depth_first(component, capped = False):
      if isinstance(x, klass):
         if x.thread.signature == component_thread_signature:
            yield x
