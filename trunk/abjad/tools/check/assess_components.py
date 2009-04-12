from abjad.component.component import _Component
from abjad.tools import iterate
import types


## TODO: Make check.assess_components( ) work with generators 
##       This will prevent needing to manifest large lists
##       of leaves for checking wiht check.assess_components( ).

def assess_components(expr, 
   contiguity = None, share = None, allow_orphans = True):
   '''Assert expr is a Python list of Abjad components.
      Set _contiguity_ to None, 'strict' or 'thread'.
      Set _share_ to None, 'parent', 'score' or 'thread'.

      The allow_orphans keyword works as a type of bypass.
      If allow_orphans is set to True (which it is by default),
      and if expr is a Python list of orphan components,
      then the helper will always evaluate to True, regardless
      of the checks specified by the other keywords.

      On the other hand, if the allow_orphans keyword is set
      to False, then expr must meet the checks specified by the
      other keywords in other for the helper to evaluate to True.

      Calls to this function appear at the beginning of many helpers.
      Calls to this function also iterate all elements in expr.
      For this reason, you can turn off all calls to this function.
      Set something in cfg.'''

   if contiguity is None:
      
      if share is None:
         return __are_components(expr)

      elif share == 'parent':
         return __are_components_in_same_parent(expr, allow_orphans)

      elif share == 'score':
         return __are_components_in_same_score(expr, allow_orphans)

      elif share == 'thread':
         return __are_components_in_same_thread(expr, allow_orphans)

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'strict':
   
      if share is None:
         return __are_strictly_contiguous_components(expr, allow_orphans)

      elif share == 'parent':
         return __are_strictly_contiguous_components_in_same_parent(
            expr, allow_orphans)

      elif share == 'score':
         return __are_strictly_contiguous_components_in_same_score(
            expr, allow_orphans)

      elif share == 'thread':
         return __are_strictly_contiguous_components_in_same_thread(
            expr, allow_orphans)

      else:
         raise ValueError(
            "share must be 'parent', 'score', 'thread' or None.")

   elif contiguity == 'thread':

      if share is not None:
         raise ValueError('When checking for thread-contiguity,'
            " the 'share' keyword should not be set.")

      else:
         return __are_thread_contiguous_components(expr, allow_orphans)

   else:
      raise ValueError("'contiguity' must be 'strict', 'thread' or None.")


## MANGLED MODULE FUNCTIONS BELOW ##

def __are_components(expr):
   '''True when expr is a Python list of Abjad components.
      otherwise False.'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('expr must be a list of Abjad components.')

   for element in expr:
      if not isinstance(element, _Component):
         return False

   return True



def __are_components_in_same_parent(expr, allow_orphans = True):
   '''True when expr is a Python list of Abjad components,
      and when all components have a parent and have the same parent.
      Otherwise False.'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True 

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   first_parent = first.parentage.parent
   if first_parent is None and not allow_orphans:
      return False

   for element in expr[1:]:
      if not isinstance(element, _Component):
         return False
      if element.parentage.parent is not first_parent:
         return False

   return True



def __are_components_in_same_score(expr, allow_orphans = True):
   '''True when expr is a Python list of Abjad components,
      and when all components have the same score root.
      Otherwise False.'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')
      
   if len(expr) == 0:
      return True 

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   first_parent = first.parentage.parent
   first_score = first.parentage.root
   for element in expr[1:]:
      if not isinstance(element, _Component):
         return False
      if element.parentage.root is not first_score:
         if not (allow_orphans and element.parentage.orphan):
            return False

   return True



def __are_components_in_same_thread(expr, allow_orphans = True):
   '''True when expr is a Python list of Abjad components such
      that all components in list carry the same thread signature.

      Otherwise False.'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   orphan_components = True
   if not first.parentage.orphan:
      orphan_components = False

   same_thread = True

   first_signature = first.thread.signature
   for component in expr[1:]:
      if not component.parentage.orphan:
         orphan_components = False
      if component.thread.signature != first_signature:
         same_thread = False
      if not allow_orphans and not same_thread:
         return False
      if allow_orphans and not orphan_components and not same_thread:
         return False

   return True



def __are_strictly_contiguous_components(expr, allow_orphans = True):
   '''True expr is a Python list of strictly contiguous components.
      Otherwise False.'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   orphan_components = True
   if not first.parentage.orphan:
      orphan_components = False

   strictly_contiguous = True

   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, _Component):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         not strictly_contiguous:
         return False
      prev = cur

   return True



def __are_strictly_contiguous_components_in_same_parent(
   expr, allow_orphans = True):
   '''True when expr is a Python list of Abjad components such that

         1. all components in list are strictly contiguous, and
         2. every component in list has the same parent.

      Otherwise False.'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   first_parent = first.parentage.parent
   if first_parent is None:
      if allow_orphans:
         orphan_components = True
      else:
         return False
   
   same_parent = True
   strictly_contiguous = True

   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, _Component):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      if not cur.parentage.parent is first_parent:
         #return False
         same_parent = False
      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
         #return False
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_parent or not strictly_contiguous):
         return False
      prev = cur

   return True



def __are_strictly_contiguous_components_in_same_score(
   expr, allow_orphans = True):
   '''True when expr is a Python list of Abjad components such that

         1. all components in list are strictly contiguous, and
         2. every component in list is in the same score.

      Otherwise False.'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   orphan_components = True   
   if not first.parentage.orphan:
      orphan_components = False

   same_score = True
   strictly_contiguous = True

   first_score = first.parentage.root
   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, _Component):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      if not cur.parentage.root is first_score:
         #return False
         same_score = False
      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
         #return False
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_score or not strictly_contiguous):
         return False
      prev = cur

   return True


def __are_strictly_contiguous_components_in_same_thread(
   expr, allow_orphans = True):
   '''True when expr is a Python list of Abjad components such that
         
         1. all components in list are strictly contiguous, and
         2. all components in list are in the same thread.

      Otherwise False.'''
   
   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   orphan_components = True
   if not first.parentage.orphan:
      orphan_components = False

   same_thread = True
   strictly_contiguous = True

   first_signature = first.thread.signature
   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, _Component):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      cur_signature = cur.thread.signature
      if not cur_signature == first_signature:
         #return False
         same_thread = False
      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
         #print 'here return!'
         #return False
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_thread or not strictly_contiguous):
         return False
      prev = cur

   return True



def __are_thread_contiguous_components(expr, allow_orphans = True):
   r'''True when expr is a Python list of Abjad components, and
      when there exists no foreign component C_f not in list such that
      C_f occurs temporally between any of the components in list.

      Thread-contiguous components are definitionally spannable.

      Example:

      t = Voice(run(4))
      t.insert(2, Voice(run(2)))
      Container(t[:2])
      Container(t[-2:])
      pitchtools.diatonicize(t)

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
      assert _are_thread_contiguous_components(t[0][:] + t[-1][:])'''

   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True 

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   orphan_components = True
   if not first.parentage.orphan:
      orphan_components = False

   same_thread = True
   thread_proper = True

   first_thread = first.thread.signature
   prev = first
   for cur in expr[1:]:
      #print prev, cur
      if not isinstance(cur, _Component):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      if not cur.thread.signature == first_thread:
         #return False
         same_thread = False
      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
         if not _are_thread_proper(prev, cur):
            #return False
            thread_proper = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_thread or not thread_proper):
         return False
      prev = cur

   return True


def _are_thread_proper(component_1, component_2):
   '''True when

         1. component_1 and component_2 are both Abjad components,
         2. component_1 and component_2 share the same thread,
         3. component_1 precedes component_2 in temporal order, and
         4. there exists no intervening component x that both shares
            the same thread as component_1 and component_2 and
            that intervenes temporally between component_1 and _2.

      Otherwise False.'''

   ## if either input parameter are not Abjad tokens
   if not isinstance(component_1, _Component) or \
      not isinstance(component_2, _Component):
      #print 'not components!'
      return False

   ## if component_1 and component_2 do not share a thread
   first_thread = component_1.thread.signature
   if not first_thread == component_2.thread.signature:
      #print 'not same thread!'
      return False

   ## find component_1 offset end time and component_2 offset begin
   first_end = component_1.offset.score + component_1.duration.prolated
   second_begin = component_2.offset.score

   ## if component_1 does not preced component_2
   if not first_end <= second_begin:
      #print 'not temporally ordered!'
      return False

   ## if there exists an intervening component of the same thread
   dfs = component_1._navigator._DFS(capped = False)
   for node in dfs:
      if node is component_2:
         break
      node_thread = node.thread.signature
      if node_thread == first_thread:
         node_begin = node.offset.score
         if first_end <= node_begin < second_begin:
            print 'Component %s intervenes between %s and %s.' % \
               (node, component_1, component_2)
            return False

   ## otherwise, return True
   return True
