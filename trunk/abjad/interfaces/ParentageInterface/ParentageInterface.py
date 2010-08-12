from abjad.interfaces._Interface import _Interface
from abjad.interfaces.ParentageInterface.containment import _ContainmentSignature
from abjad.core import Rational
import types


class ParentageInterface(_Interface):
   '''Bundle attributes relating to the containers within
   which any Abjad component nests.
   
   Handle no LilyPond grob.
   '''

   def __init__(self, _client):
      '''Bind to client and set parent to None.'''
      _Interface.__init__(self, _client)
      self.__parent = None

   ## PRIVATE METHODS ##

   def _cut(self):
      '''Client and parent cut completely.'''
      client, parent = self._client, self.parent
      if parent is not None:
         index = parent.index(client)
         parent._music.remove(client)
      self._ignore( )

   def _ignore(self):
      '''Client forgets parent (but parent remembers client).'''
      self._client._update._mark_for_update_to_root( )
      self.__parent = None

   def _switch(self, new_parent):
      '''Remove client from parent and give client to new_parent.'''
      self._cut( )
      self.__parent = new_parent
      self._client._update._mark_for_update_to_root( )

   ## PUBLIC ATTRIBUTES ##

   @property
   def depth(self):
      '''Nonnegative integer number of components in the proper
      parentage of `component`. ::

         abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> note.parentage.depth
         2

      Defined equal to ``len(component.parentage.proper)``.
      '''

      #return len(self.parentage) - 1
      return len(self.proper)

   @property
   def depth_tuplet(self):
      '''Nonnegative integer number of tuplets in the proper parentage 
      of `component`. ::

         abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> note.parentage.depth_tuplet
         1

      Tuplets do not count as containing themselves. ::

         abjad> tuplet.parentage.depth_tuplet
         0

      Zero when there is no tuplet in the proper parentage of component. ::

         abjad> staff.parentage.depth_tuplet
         0
      '''

      from abjad.components._Tuplet import _Tuplet
      result = 0
      for parent in self.parentage[1:]:
         if isinstance(parent, _Tuplet):
            result += 1
      return result

   @property
   def governor(self):
      r'''Reference to first sequential container `Q` 
      in the parentage of `component` such that 
      the parent of `Q` is either a parallel container or ``None``. ::

         abjad> t = Voice([Container(Voice(notetools.make_repeated_notes(2)) * 2)])
         abjad> t[0].parallel = True
         abjad> macros.diatonicize(t)
         abjad> t[0][0].name = 'voice 1'
         abjad> t[0][1].name = 'voice 2'

      ::

         abjad> print t.format
         \new Voice {
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
         }

      ::

         abjad> note = t.leaves[1]
         abjad> note.parentage.governor is t[0][0]
         True

      In the case that no such container exists
      in the parentage of `component`, return ``None``. ::

         abjad> note = Note(0, (1, 4))
         abjad> note.parentage.governor is None
         True

      .. note:: Governor is an old and probably nonoptimal idea
         in the codebase. The concept is used only 
         to clone components with a certain part of parentage.
      '''

      from abjad.components.Container import Container
      for component in self.parentage:
         if isinstance(component, Container) and not component.parallel:
            parent = component.parentage.parent
            if parent is None:
               return component
            if isinstance(parent, Container) and parent.parallel:
               return component
            
   @property
   def orphan(self):
      '''``True`` when component has no parent, otherwise ``False``.
      
      ::

         abjad> note = Note(0, (1, 4))
         abjad> note.parentage.orphan
         True

      Defined equal to ``len(component.parentage.proper) == 0``.
      '''

      #return len(self.parentage) == 1
      return len(self.proper) == 0

   @property
   def parent(self):
      '''Read-only reference to immediate parent of `component`.
   
      ::

         abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> note.parentage.parent
         FixedDurationTuplet(1/4, [c'8, d'8, e'8])
   
      Equivalent to ``component.parentage.proper[0]`` for those components
      with proper parentage. Otherwise ``None``.
      '''

      return self.__parent
      
   @property
   def parentage(self):
      '''Read-only list of all of components in the parentage of 
      `component`, including `component`. ::

         abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> note.parentage.parentage
         [Note(c', 8), FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1}]

      .. versionchanged:: 1.1.1
         Returns (immutable) tuple instead of (mutable) list.
      '''

      result = [ ]
      cur = self._client
      while cur is not None:
         result.append(cur)
         cur = cur.parentage.parent
      result = tuple(result)
      return result

   @property
   def proper(self):
      '''.. versionadded:: 1.1.1

      Read-only tuple of all of components in the parentage of 
      `component`, excluding `component`. ::

         abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> note.parentage.proper
         (FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1})

      Defined equal to ``component.parentage.parentage[1:]``.
      '''

      return tuple(self.parentage[1:])

   @property
   def root(self):
      '''Reference to root-level component in parentage 
      of `component`. ::

         abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> note.parentage.root
         Staff{1}

      Defined equal to ``component.parentage.parentage[-1]``.
      '''

      return self.parentage[-1]

   @property
   def signature(self):
      '''Containment signature of `component`.

      Containment signature defined equal to first voice, first staff,
      first staffgroup, first score and root in parentage. ::

         abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> print note.parentage.signature
               root: Staff-18830800 (18830800)
              score: 
         staffgroup: 
              staff: Staff-18830800
              voice: 
               self: Note-18619728
      '''

      from abjad.components.Score import Score
      from abjad.components.StaffGroup import StaffGroup
      from abjad.components.Staff import Staff
      from abjad.components.Voice import Voice
      signature = _ContainmentSignature( )
      signature._self = self._client._ID
      for component in self._client.parentage.parentage:
         if isinstance(component, Voice) and not signature._voice:
            signature._voice = component._ID
         elif isinstance(component, Staff) and not signature._staff:
            signature._staff = component._ID
         elif isinstance(component, StaffGroup) and not signature._staffgroup:
            signature._staffgroup = component._ID
         elif isinstance(component, Score) and not signature._score:
            signature._score = component._ID
      else:
         '''Root components must be manifestly equal to compare True.'''
         signature._root = id(component)
         signature._root_str = component._ID
      return signature
