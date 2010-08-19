def get_tie_chain(component):
   '''.. versionadded:: 1.1.2

   Get tie chain from `component`.
   '''

   raise NotImplementedError('implementation coming soon.')

   count = self.count
   if count == 0:
      return (self._client, )
   elif count == 1:
      return tuple(self.spanner.leaves)
   else:
      raise ExtraSpannerError

