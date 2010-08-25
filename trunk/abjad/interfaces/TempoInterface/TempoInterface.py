#from abjad.interfaces._BacktrackingInterface import _BacktrackingInterface
from abjad.interfaces._ObserverInterface import _ObserverInterface
#from abjad.tools import tempotools


class TempoInterface(_ObserverInterface):

   def __init__(self, _client, update_interface):
      _ObserverInterface.__init__(self, _client, update_interface)
      self._effective = None

   ## PRIVATE ATTRIBUTES ##

   def _get_effective(self):
      from abjad.tools.marktools.get_effective_mark import get_effective_mark
      from abjad.tools.marktools.TempoMark import TempoMark
      return get_effective_mark(self._client, TempoMark)

   def _update_component(self):
      self._effective = self._get_effective( )

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      self._update_prolated_offset_values_of_all_score_components_if_necessary( )
      self._update_observer_interfaces_of_all_score_components_if_necessary( )
      return self._effective


#class TempoInterface(_ObserverInterface, _BacktrackingInterface):
#   '''Handle LilyPond MetronomeMark grob and Abjad TempoSpanner.
#
#   The implementation of `effective` given here allows for
#   tempo indication to be set either be a tempo spanner or
#   by a forced value set directly on the tempo interface.
#   As such, `TempoInterface` implements two different and
#   competing patterns for the way in which tempo indications
#   can be set.
#
#   This probably isn't the best situation and, in fact, the
#   implementation will clean up considerably is we allow for
#   only one way to set tempo indications, most likely
#   through spanners only.
#
#   Both patterns remain for now, though this situation is
#   unstable and should probably resolve at some point in 
#   the future.
#   '''
#   
#   def __init__(self, _client, _update_interface):
#      _ObserverInterface.__init__(self, _client, _update_interface)
#      _BacktrackingInterface.__init__(self, 'tempo')
#      self._acceptableTypes = (tempotools.TempoIndication, )
#      self._effective = None
#      self._forced = None
# 
#   ## PRIVATE ATTRIBUTES ##
#
#   @property
#   def _opening(self):
#      '''Format contribution at container opening or before leaf.'''
#      from abjad.tools import spannertools
#      result =  [ ] 
#      #if self.forced or self.change and not (
#      #   self.spanned and self.spanner._is_my_first_leaf(self._client)):
#      if self.forced or self.change and not (
#         spannertools.get_all_spanners_attached_to_component(
#         self._client, spannertools.TempoSpanner) and
#         spannertools.get_the_only_spanner_attached_to_component(
#         self._client, spannertools.TempoSpanner)._is_my_first_leaf(self._client)):
#         result.append(self.effective.format)
#      return result
#
#   ## PUBLIC ATTRIBUTES ##
#
#   @property
#   def effective(self):
#      '''Effective tempo governing client.
#         Decisions here arbitrate between spanner and forced attribute.'''
#      from abjad.tools import spannertools
#      if self.forced:
#         return self.forced
#      #if self.parented:
#      if bool(spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
#         self._client, spannertools.TempoSpanner)):
#         #return self.spanner_in_parentage.tempo_indication
#         return spannertools.get_the_only_spanner_attached_to_any_improper_parent_of_component(
#         self._client, spannertools.TempoSpanner).tempo_indication
#      return _BacktrackingInterface.effective.fget(self)
