from abjad.components._Component import _Component
from abjad.tools import threadtools
import types


def all_are_thread_contiguous_components(expr, klasses = (_Component), allow_orphans = True):
   r'''True when `expr` is a Python list of Abjad components, and
      when there exists no foreign component C_f not in list such that
      C_f occurs temporally between any of the components in list.

      Thread-contiguous components are definitionally spannable::

         t = Voice(notetools.make_repeated_notes(4))
         t.insert(2, Voice(notetools.make_repeated_notes(2)))
         Container(t[:2])
         Container(t[-2:])
         macros.diatonicize(t)

         \new Voice {
            {
               c'8
               d'8
            }
            \new Voice {
               e'8
               f'8
            }
            {
               g'8
               a'8
            }
         }

         assert _are_thread_contiguous_components(t[0:1] + t[-1:])
         assert _are_thread_contiguous_components(t[0][:] + t[-1:])
         assert _are_thread_contiguous_components(t[0:1] + t[-1][:])
         assert _are_thread_contiguous_components(t[0][:] + t[-1][:])
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True 

   first = expr[0]
   if not isinstance(first, klasses):
      return False

   orphan_components = True
   if not first.parentage.orphan:
      orphan_components = False

   same_thread = True
   thread_proper = True

   #first_thread = first.thread.signature
   first_thread = threadtools.component_to_thread_signature(first)
   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, klasses):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      #if not cur.thread.signature == first_thread:
      if not threadtools.component_to_thread_signature(cur) == first_thread:
         same_thread = False
      if not prev._navigator._is_immediate_temporal_successor_of(cur):
         if not _are_thread_proper(prev, cur):
            thread_proper = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_thread or not thread_proper):
         return False
      prev = cur

   return True


def _are_thread_proper(component_1, component_2, klasses = (_Component)):
   '''True when

         1. component_1 and component_2 are both Abjad components,
         2. component_1 and component_2 share the same thread,
         3. component_1 precedes component_2 in temporal order, and
         4. there exists no intervening component x that both shares
            the same thread as component_1 and component_2 and
            that intervenes temporally between component_1 and _2.

      Otherwise False.
   '''

   ## if either input parameter are not Abjad tokens
   if not isinstance(component_1, klasses) or \
      not isinstance(component_2, klasses):
      return False

   ## if component_1 and component_2 do not share a thread
   #first_thread = component_1.thread.signature
   first_thread = threadtools.component_to_thread_signature(component_1)
   #if not first_thread == component_2.thread.signature:
   if not first_thread == threadtools.component_to_thread_signature(component_2):
      #print 'not same thread!'
      return False

   ## find component_1 offset end time and component_2 offset begin
   first_end = component_1.offset.prolated.stop
   second_begin = component_2.offset.prolated.start

   ## if component_1 does not preced component_2
   if not first_end <= second_begin:
      #print 'not temporally ordered!'
      return False

   ## if there exists an intervening component of the same thread
   dfs = component_1._navigator._DFS(capped = False)
   for node in dfs:
      if node is component_2:
         break
      #node_thread = node.thread.signature
      node_thread = threadtools.component_to_thread_signature(node)
      if node_thread == first_thread:
         node_begin = node.offset.prolated.start
         if first_end <= node_begin < second_begin:
            print 'Component %s intervenes between %s and %s.' % \
               (node, component_1, component_2)
            return False

   ## otherwise, return True
   return True
