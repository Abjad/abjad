from abjad import *
from abjad.tools import seqtools


def test_seqtools_interlace_sequences_01( ):

   k = range(100, 103)
   l = range(200, 201)
   m = range(300, 303)
   n = range(400, 408)
   t = seqtools.interlace_sequences(k, l, m, n)

   assert t == [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]


def test_seqtools_interlace_sequences_02( ):

   a = 'introductory'
   b = 'text'

   t = seqtools.interlace_sequences(a, b)
   t = ''.join(t)

   assert t == 'itnetxrtoductory'
