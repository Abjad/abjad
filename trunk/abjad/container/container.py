from abjad.component.component import _Component
from abjad.container.duration import _ContainerDurationInterface
from abjad.container.formatter import _ContainerFormatter
from abjad.container.spanner.aggregator import _ContainerSpannerAggregator
from abjad.interfaces import BracketsInterface
from abjad.interfaces import NoteHeadInterface


class Container(_Component):

   def __init__(self, music = None):
      '''Initialize container with music list of length zero or grater.'''
      _Component.__init__(self)
      self._spanners = _ContainerSpannerAggregator(self)
      self._initializeMusic(music)
      self._brackets = BracketsInterface(self)
      self._duration = _ContainerDurationInterface(self)
      self._formatter = _ContainerFormatter(self)
      self.parallel = False

   ## OVERLOADS ##

   def __add__(self, expr):
      '''Concatenate containers self and expr.
         The operation c = a + b returns a new Container c with
         the content of both a and b.
         The operation is non-commutative: the content of the first
         operand will be placed before the content of the second operand.'''
      from abjad.tools import componenttools
      from abjad.tools import containertools
      left = componenttools.clone_components_and_fracture_crossing_spanners([self])[0]
      right = componenttools.clone_components_and_fracture_crossing_spanners([expr])[0]
      return containertools.fuse_like_named_contiguous_containers_in_expr([left, right])

   def __contains__(self, expr):
      '''True if expr is in container, otherwise False.'''
      return expr in self._music

   def __delitem__(self, i):
      '''Find component(s) at index or slice 'i' in container.
         Detach component(s) from parentage.
         Withdraw component(s) from crossing spanners.
         Preserve spanners that component(s) cover(s).'''
      from abjad.tools.parenttools.switch import _switch
      from abjad.tools.spannertools.withdraw_from_crossing import \
         _withdraw_from_crossing
      components = self[i]
      if not isinstance(components, list):
         components = [components]
      _withdraw_from_crossing(components)
      _switch(components, None)

   def __getitem__(self, i):
      '''Return component at index i in container.
         Shallow traversal of container for numeric indices only..
         For deep, recursive traversal of container for named indices,
         use Container.get(expr).'''
      return self._music[i]
            
   def __iadd__(self, expr):
      '''__iadd__ avoids unnecessary copying of structures.'''
      from abjad.tools import componenttools
      from abjad.tools import containertools
      return containertools.fuse_like_named_contiguous_containers_in_expr([self, 
         componenttools.clone_components_and_fracture_crossing_spanners([expr])[0]])

   def __imul__(self, total):
      '''Multiply contents of container 'total' times.
         Return multiplied container.'''
      from abjad.tools import containertools
      return containertools.repeat_contents_of_container(self, total = total)

   def __len__(self):
      '''Return nonnegative integer number of components in container.'''
      return len(self._music)

   def __radd__(self, expr):
      '''Extend container by contents of expr to the right.'''
      return self + expr

   def __repr__(self):
      '''String format of container for interpreter display.'''
      return self._compact_representation

   def __setitem__(self, i, expr):
      '''Set 'expr' in self at nonnegative integer index i.
         Or, set 'expr' in self at slice i.
         Find spanners that dominate self[i] and children of self[i].
         Replace contents at self[i] with 'expr'.
         Reattach spanners to new contents.
         This operation leaves all score trees always in tact.'''
      from abjad.tools import componenttools
      from abjad.tools import spannertools
      from abjad.tools.spannertools.withdraw_from_crossing import \
         _withdraw_from_crossing
      # item assignment
      if isinstance(i, int):
         assert componenttools.all_are_components([expr])
         old = self[i]
         spanners_receipt = spannertools.get_spanners_that_dominate_components([old])
         ## must withdraw from spanners before parentage!
         ## otherwise begin / end assessments don't work!
         _withdraw_from_crossing([expr])
         expr.parentage._switch(self)
         self._music.insert(i, expr)
         componenttools.remove_component_subtree_from_score_and_spanners([old])
         for spanner, index in spanners_receipt:
            spanner._insert(index, expr)
            expr.spanners._add(spanner)
      # slice assignment
      else:
         assert componenttools.all_are_components(expr)
         if i.start == i.stop and i.start is not None \
            and i.stop is not None and i.start <= -len(self):
            start, stop = 0, 0
         else:
            start, stop, stride = i.indices(len(self))
         old = self[start:stop]
         spanners_receipt = spannertools.get_spanners_that_dominate_container_components_from_to(self, start, stop)
         componenttools.remove_component_subtree_from_score_and_spanners(old)
         ## must withdraw before setting in self!
         ## otherwise circular withdraw ensues!
         _withdraw_from_crossing(expr)
         self._music[start:start] = expr
         for component in expr:
            component.parentage._switch(self)
         for spanner, index in spanners_receipt:
            for component in reversed(expr):
               spanner._insert(index, component)
               component.spanners._add(spanner)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_representation(self):
      '''Compact form used in spanner display.'''
      if not self.parallel:
         return '{%s}' % self._summary
      else:
         return '<<%s>>' % self._summary

   @property
   def _summary(self):
      '''Formatted summary of container contents for repr output.'''
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   ## PUBLIC ATTRIBUTES ##

   @property
   def brackets(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.brackets.interface.BracketsInterface`.'''
      return self._brackets

   @apply
   def parallel( ):
      def fget(self):
         '''Read / write boolean for paralllel / sequential containers.'''
         return self._parallel
      def fset(self, expr):
         from abjad.context.context import _Context
         from abjad.tools import componenttools
         assert isinstance(expr, bool)
         if expr == True:
            assert componenttools.all_are_components(self._music, klasses = (_Context, ))
         self._parallel = expr
      return property(**locals( ))

   ## PRIVATE METHODS ##

   def _initializeMusic(self, music):
      '''Insert `music` components in in container.
      Set parent of `music` components to container.'''
      from abjad.tools import componenttools
      from abjad.tools import parenttools
      from abjad.tools.parenttools.switch import _switch
      music = music or [ ]
      assert componenttools.all_are_contiguous_components_in_same_thread(music)
      parent, index, stop_index = componenttools.get_parent_and_start_stop_indices_of_components(music)
      self._music = list(music)
      _switch(self._music, self)
      if parent is not None:
         parent._music.insert(index, self)
         self.parentage._switch(parent)

   def _isOneOfMyFirstLeaves(self, leaf):
      return leaf in self._navigator._contemporaneousStartContents

   def _isOneOfMyLastLeaves(self, leaf):
      return leaf in self._navigator._contemporaneousStopContents

   ## PUBLIC METHODS ## 

   ## TODO: Spanner get silently stripped sometimes! ##

   def append(self, component):
      '''Append component to the end of container.
      Attach no new spanners to component.'''
      self[len(self):len(self)] = [component]

   def extend(self, expr):
      '''Extend container with components in 'expr'.
      Change no container spanners.
      Return container.'''
      self[len(self):len(self)] = expr[:]
      return self

   def index(self, component):
      '''Return nonnegative integer index of component in container.'''
      return self._music.index(component)

   def insert(self, i, component):
      '''Insert component 'component' at index 'i' in container.
      Attach spanners that dominate index 'i' to 'component'.'''
      self[i:i] = [component]

   def pop(self, i = -1):
      '''Find component at index 'i' in container.
      Detach component from parentage.
      Withdraw component from crossing spanners.
      Preserve spanners that component covers.
      Return component.'''
      component = self[i]
      del(self[i])
      return component

   def remove(self, component):
      '''Assert 'component' in container.
      Detach 'component' from parentage.
      Withdraw 'component' from crossing spanners.
      Carry covered spanners forward on 'component'.
      Return 'component'.'''
      i = self.index(component)
      del(self[i])
      return component
