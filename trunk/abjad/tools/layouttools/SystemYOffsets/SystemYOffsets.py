from abjad.core import _StrictComparator
from abjad.core import _Immutable


class SystemYOffsets(_StrictComparator, _Immutable):
   '''Used to specify systems starting at even intervals running
   down every page.

   Set `interval` to a positive number.
   Set `systems_per_page` to a positive number.
   Set `skip_systems_on_first_page` to a positive integer less than 
   `systems_per_page`, defaulting to ``1``. ::

      abjad> specification = SystemYOffsets(38, 5)
      SystemYOffsets([0], 44, 88, 132, 176 | 0, 44, 88, 132, 176 | ...) 

   Pass instances of this class to other layout functions.
   '''

   def __init__(self, interval, systems_per_page, skip_systems_on_first_page = 1):
      #self.interval = interval
      #self.systems_per_page = systems_per_page
      #self.skip_systems_on_first_page = skip_systems_on_first_page
      object.__setattr__(self, 'interval', interval)
      object.__setattr__(self, 'systems_per_page', systems_per_page)
      object.__setattr__(self, 'skip_systems_on_first_page', skip_systems_on_first_page)

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, SystemYOffsets):
         if self.interval == expr.interval and \
            self.systems_per_page == expr.systems_per_page and \
            self.skip_systems_on_first_page == expr.skip_systems_on_first_page:
            return True
      return False

   def __getitem__(self, i):
      return self._y_offset_list.__getitem__(i)

   def __ne__(self, expr):
      return not self == expr

   def __repr__(self):
      skip = self._skip_on_first_page_list
      if skip:
         skip = [str(x) for x in skip]
         skip = ', '.join(skip)
         skip = '[%s]' % skip
      show = self._show_on_first_page_list
      show = [str(x) for x in show]
      show = ', '.join(show)
      first_page = ', '.join((skip, show))
      second_page = self._y_offset_list
      second_page = [str(x) for x in second_page]
      second_page = ', '.join(second_page)
      third_page = '...'
      pages = ' | '.join((first_page, second_page, third_page))
      return 'SystemYOffsets(%s)' % pages

   ## PRIVATE ATTRIBUTES ##

   @property
   def _show_on_first_page_list(self):
      return self._y_offset_list[self.skip_systems_on_first_page:]

   @property
   def _skip_on_first_page_list(self):
      return self._y_offset_list[:self.skip_systems_on_first_page]

   @property
   def _y_offset_list(self):
      return [self.interval * x for x in range(self.systems_per_page)]
