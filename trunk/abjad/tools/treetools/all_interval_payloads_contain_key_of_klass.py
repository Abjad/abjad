from abjad.tools.treetools import *


def all_interval_payloads_contain_key_of_klass(intervals, key, klass):
   '''True if all intervals in `intervals` use a dictionary as their payload,
   have a key named `key` in that dictionary, and the key's value is
   an instance of `klass`.'''

   if all([isinstance(interval.data, dict) for interval in intervals]) and \
      all([interval.data.has_key(key) for interval in intervals]) and \
      all([isinstance(interval.data[key], klass) for interval in intervals]):
      return True
   else:
      return False
