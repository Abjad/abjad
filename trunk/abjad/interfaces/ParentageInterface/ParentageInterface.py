from abjad.interfaces._Interface import _Interface


class ParentageInterface(_Interface):
   '''Bundle attributes relating to the containers within which any Abjad component nests.
   '''

   __slots__ = ('__parent', )

   def __init__(self, _client):
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
      #self._client._update._mark_all_improper_parents_for_update( )
      self._client._mark_entire_score_tree_for_later_update('prolated')
      self.__parent = None

   def _switch(self, new_parent):
      '''Remove client from parent and give client to new_parent.'''
      self._cut( )
      self.__parent = new_parent
      #self._client._update._mark_all_improper_parents_for_update( )
      self._client._mark_entire_score_tree_for_later_update('prolated')

   ## PUBLIC ATTRIBUTES ##

#   @property
#   def depth(self):
#      '''Nonnegative integer number of components in the proper
#      parentage of `component`. ::
#
#         abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
#         abjad> staff = Staff([tuplet])
#         abjad> note = staff.leaves[0]
#         abjad> note.parentage.depth
#         2
#
#      Defined equal to ``len(component.parentage.proper_parentage)``.
#      '''
#
#      return len(self.proper_parentage)

#   @property
#   def depth_tuplet(self):
#      '''Nonnegative integer number of tuplets in the proper parentage 
#      of `component`. ::
#
#         abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
#         abjad> staff = Staff([tuplet])
#         abjad> note = staff.leaves[0]
#         abjad> note.parentage.depth_tuplet
#         1
#
#      Tuplets do not count as containing themselves. ::
#
#         abjad> tuplet.parentage.depth_tuplet
#         0
#
#      Zero when there is no tuplet in the proper parentage of component. ::
#
#         abjad> staff.parentage.depth_tuplet
#         0
#      '''
#
#      from abjad.components.Tuplet import Tuplet
#      result = 0
#      for parent in self.proper_parentage:
#         if isinstance(parent, Tuplet):
#            result += 1
#      return result

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
      from abjad.tools import componenttools

      #for component in self.improper_parentage:
      for component in componenttools.get_improper_parentage_of_component(self._client):
         if isinstance(component, Container) and not component.parallel:
            parent = component.parentage.parent
            if parent is None:
               return component
            if isinstance(parent, Container) and parent.parallel:
               return component

#   @property
#   def improper_parentage(self):
#      '''Read-only list of all of components in the parentage of 
#      `component`, including `component`. ::
#
#         abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
#         abjad> staff = Staff([tuplet])
#         abjad> note = staff.leaves[0]
#         abjad> note.parentage.improper_parentage
#         [Note(c', 8), tuplettools.FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1}]
#
#      .. versionchanged:: 1.1.1
#         Returns (immutable) tuple instead of (mutable) list.
#      '''
#
#      result = [ ]
#      cur = self._client
#      while cur is not None:
#         result.append(cur)
#         cur = cur.parentage.parent
#      result = tuple(result)
#      return result
            
#   @property
#   def is_orphan(self):
#      '''``True`` when component has no parent, otherwise ``False``.
#      
#      ::
#
#         abjad> note = Note(0, (1, 4))
#         abjad> note.parentage.is_orphan
#         True
#
#      Defined equal to ``len(component.parentage.proper_parentage) == 0``.
#      '''
#
#      return len(self.proper_parentage) == 0

   @property
   def parent(self):
      '''Read-only reference to immediate parent of `component`.
   
      ::

         abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> staff = Staff([tuplet])
         abjad> note = staff.leaves[0]
         abjad> note.parentage.parent
         tuplettools.FixedDurationTuplet(1/4, [c'8, d'8, e'8])
   
      Equivalent to ``component.parentage.proper_parentage[0]`` for those components
      with proper parentage. Otherwise ``None``.
      '''

      return self.__parent
      
#   @property
#   def proper_parentage(self):
#      '''.. versionadded:: 1.1.1
#
#      Read-only tuple of all of components in the parentage of 
#      `component`, excluding `component`. ::
#
#         abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
#         abjad> staff = Staff([tuplet])
#         abjad> note = staff.leaves[0]
#         abjad> note.parentage.proper_parentage
#         (tuplettools.FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1})
#
#      Defined equal to ``component.parentage.improper_parentage[1:]``.
#      '''
#
#      return tuple(self.improper_parentage[1:])

#   @property
#   def root(self):
#      '''Reference to root-level component in parentage 
#      of `component`. ::
#
#         abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
#         abjad> staff = Staff([tuplet])
#         abjad> note = staff.leaves[0]
#         abjad> note.parentage.root
#         Staff{1}
#
#      Defined equal to ``component.parentage.improper_parentage[-1]``.
#      '''
#
#      return self.improper_parentage[-1]
