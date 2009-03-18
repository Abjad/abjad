from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_components import _are_components
from abjad.helpers.are_components_in_same_parent import _are_components_in_same_parent
from abjad.helpers.are_components_in_same_score import _are_components_in_same_score
from abjad.helpers.are_components_in_same_thread import _are_components_in_same_thread
from abjad.helpers.are_strictly_contiguous_components import _are_strictly_contiguous_components
from abjad.helpers.are_strictly_contiguous_components_in_same_parent import _are_strictly_contiguous_components_in_same_parent
from abjad.helpers.are_strictly_contiguous_components_in_same_score import _are_strictly_contiguous_components_in_same_score
from abjad.helpers.are_strictly_contiguous_components_in_same_thread import _are_strictly_contiguous_components_in_same_thread
from abjad.helpers.are_thread_contiguous_components import _are_thread_contiguous_components


## TODO: Maybe a decorator can eliminate all this?

def _assert_are_components(expr):
   if not _are_components(expr):
      raise TypeError('Must be list of Abjad components.')

def _assert_are_components_in_same_parent(expr, allow_orphans = True):
   if not _are_components_in_same_parent(expr, allow_orphans):
      raise ContiguityError

def _assert_are_components_in_same_score(expr, allow_orphans = True):
   if not _are_components_in_same_score(expr, allow_orphans):
      raise ContiguityError

def _assert_are_components_in_same_thread(expr, allow_orphans = True):
   if not _are_components_in_same_thread(expr, allow_orphans):
      raise ContiguityError

def _assert_are_strictly_contiguous_components(expr, allow_orphans = True):
   if not _are_strictly_contiguous_components(expr, allow_orphans):
      raise ContiguityError

def _assert_are_strictly_contiguous_components_in_same_parent(
   expr, allow_orphans = True):
   if not _are_strictly_contiguous_components_in_same_parent(
      expr, allow_orphans):
      raise ContiguityError

def _assert_are_strictly_contiguous_components_in_same_score(
   expr, allow_orphans = True):
   if not _are_strictly_contiguous_components_in_same_score(
      expr, allow_orphans):
      raise ContiguityError

def _assert_are_strictly_contiguous_components_in_same_thread(
   expr, allow_orphans = True):
   if not _are_strictly_contiguous_components_in_same_thread(
      expr, allow_orphans):
      raise ContiguityError

def _assert_are_thread_contiguous_components(expr, allow_orphans = True):
   if not _are_thread_contiguous_components(expr, allow_orphans):
      raise ContiguityError
