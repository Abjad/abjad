from abjad import *

def test_leaves_fuse_binary_01( ):
   '''Wokrs with list of leaves.'''
   fused = leaves_fuse_binary(Note(0, (1, 4))*8)
   assert len(fused) == 1 
   assert fused[0].duration.written == 2 

def test_leaves_fuse_binary_02( ):
   '''Works with Leaf component.'''
   fused = leaves_fuse_binary(Note(0, (1, 4)))
   assert len(fused) == 1 
   assert fused[0].duration.written == Rational(1, 4) 

def test_leaves_fuse_binary_03( ):
   '''Wokrs with Containers.'''
   t = Voice(Note(0, (1, 4)) * 8)
   fused = leaves_fuse_binary(t)
   assert len(fused) == 1 
   assert fused[0].duration.written == 2 
   assert t[0] is fused[0]

def test_leaves_fuse_binary_04( ):
   '''Fussion results in tied notes.'''
   t = Voice([Note(0, (2, 16)), Note(9, (3, 16))])
   fused = leaves_fuse_binary(t)
   assert len(fused) == 2 
   assert fused[0].duration.written == Rational(1, 4) 
   assert fused[1].duration.written == Rational(1, 16) 
   assert fused[0].tie.spanner is fused[1].tie.spanner
   assert t[0] is fused[0]
   assert t[1] is fused[1]
   assert t[0].pitch == t[1].pitch

