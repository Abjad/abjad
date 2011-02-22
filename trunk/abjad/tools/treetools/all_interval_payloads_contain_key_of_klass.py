from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def all_interval_payloads_contain_key_of_klass(intervals, key, klass):
   '''True if all intervals in `intervals` use a dictionary as their payload,
   have a key named `key` in that dictionary, and the key's value is
   an instance of `klass`.'''

   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)

   if all([isinstance(interval.data, dict) for interval in tree]) and \
      all([interval.data.has_key(key) for interval in tree]) and \
      all([isinstance(interval.data[key], klass) for interval in tree]):
      return True
   else:
      return False
