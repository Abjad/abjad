import os


class _TagParser(object):

   def __init__(self):
      self.output = [ ]

   @property
   def depth(self):
      if 'css' in os.listdir(os.curdir):
         return 0
      elif 'css' in os.listdir(os.pardir):
         return 1
      elif 'css' in os.listdir(os.pardir + os.sep + os.pardir):
         return 2
      elif 'css' in os.listdir(
         os.pardir + os.sep + os.pardir + os.sep + os.pardir):
         return 3
      else:
         raise ValueError('can not find doc root directory!')

   def parse(self):
      pass
