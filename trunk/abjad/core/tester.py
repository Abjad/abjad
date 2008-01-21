class Tester(object):

   def __init__(self, target):
      self._target = target

   ### REPR ###

   def __repr__(self):
      return 'Tester' 

   ### TESTS ### 
   
   def testParents(self, report = True, ret = 'violators'):
      '''
      Each node needs a parent;
      each node needs the *correct* parent.
      '''
      class Visitor(object):
         def __init__(self, target):
            self.parents = [target._parent]
            self.total = 0
            self.bad = 0
            self.violators = [ ]
         def visit(self, node):
            self.total += 1
            if node._parent != self.parents[-1]:
               self.bad += 1
               print '%s has parent %s instead of expected %s.\n' % (
                  node, node._parent, self.parents[-1])
               self.violators.append(node)
            if hasattr(node, '_music'):
               self.parents.append(node)
         def unvisit(self, node):
            if hasattr(node, '_music'):
               self.parents.pop( )
      v = Visitor(self._target)
      self._target._navigator._traverse(v)
      if report:
         print '%4d / %4d bad parents.' % (v.bad, v.total)
      if ret == 'violators':
         return v.violators
      elif ret:
         return v.bad == 0
      else:
         return None

   def testNextLeaves(self, report = True, ret = 'violators'):
      violators = [ ]
      leaves = self._target.leaves
      total, bad = 0, 0
      if leaves:
         leaves.pop( )
         total += 1
         for l in leaves:
            if not l.next:
               violators.append(l)
               bad += 1
            total += 1
      if report:
         print '%4d / %4d bad leaves.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None

   def testPitchlessNotesChords(self, report = True, ret = 'violators'):
      violators = [ ]
      leaves = self._target.getInstances(('Note', 'Chord'))
      total, bad = 0, 0
      for leaf in leaves:
         total += 1
         if leaf.kind('Note'):
            if leaf.pitch is None or leaf.pitch.number is None:
               bad += 1
         elif leaf.kind('Chord'):
            if leaf.pitches is None or leaf.pitches == [ ]:
               bad += 1
      if report:
         print '%4d / %4d notes or chords without pitch.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None

   def testDurationlessLeaves(self, report = True, ret = 'violators'):
      violators = [ ]
      leaves = self._target.getInstances('Leaf')
      total, bad = 0, 0
      for leaf in leaves:
         total += 1
         if leaf.duration is None :
            violators.append(leaf)
            bad += 1
      if report:
         print '%4d / %4d leaves without duration.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None

   
   def testBadFlags(self, report = True, ret = 'violators'):
      violators = [ ]
      leaves = self._target.leaves
      for leaf in leaves:
         flags = leaf.beam.flags
         left, right = leaf.beam.counts
         if left is not None:
            if left > flags or (left < flags and right not in (flags, None)):
               if leaf not in violators:
                  violators.append(leaf)
         if right is not None:
            if right > flags or (right < flags and left not in (flags, None)):
               if leaf not in violators:
                  violators.append(leaf)
      bad = len(violators)
      total = len(leaves)
      if report:
         print '%4d / %4d leaves with bad flags.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None


   def testContainers(self, report = True, ret = 'violators'):
      violators = [ ]
      containers = self._target.getInstances('Container')
      bad, total = 0, 0
      for t in containers:
         if len(t) == 0:
            violators.append(t)
            bad += 1
         total += 1
      if report:
         print '%4d / %4d bad containers.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None

   # TODO add testTuplets to check label harmony

   def testMeasures(self, report = True, ret = 'violators'):
      violators = [ ]
      total, bad = 0, 0
      for p in self._target.getInstances('Measure'):
         if not p.testDuration( ):
            violators.append(p)
            bad += 1
         total += 1
      if report:
         print '%4d / %4d bad measures.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None
            
   def testSpanners(self, report = True, ret = 'violators',
      interface = None, grob = None, attribute = None, value = None):
      violators = [ ]
      total, bad = 0, 0
      spanners = self._target.spanners.get(interface, grob, attribute, value)
      for spanner in spanners:
         contiguousLeaves = True
         leaves = spanner.leaves
         for i in range(len(leaves) - 1):
            if leaves[i].next != leaves[i + 1]:
               contiguousLeaves = False
         if not contiguousLeaves:
            violators.append(spanner)
            bad += 1
         total += 1
      if report:
         print '%4d / %4d bad spanners.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None 


   def testShortHairpins(self, report = True, ret = 'violators'):
      violators = [ ]
      total, bad = 0, 0
      for hairpin in self._target.spanners.get(classname = '_Hairpin'):
         if len(hairpin) <= 1:
            violators.append(hairpin)
            bad += 1
         total += 1
      if report:
         print '%4d / %4d short hairpins.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None 

   def testIntermarkedHairpins(self, report = True, ret = 'violators'):
      violators = [ ]
      total, bad = 0, 0
      for hairpin in self._target.spanners.get(classname = '_Hairpin'):
         if len(hairpin) > 2:
            for leaf in hairpin.leaves[1 : -1]:
               if leaf.dynamics.mark:
                  violators.append(hairpin)
                  bad += 1
                  break
         total += 1
      if report:
         print '%4d / %4d intermarked hairpins.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None 


   def testOverlappingGlissandi(self, report = True, ret = 'violators'):
      '''Overlapping glissandi are a problem;
         dove-tailed glissandi are OK.'''
      violators = [ ] 
      for leaf in self._target.leaves:
         glissandi = leaf.glissando.spanners
         if len(glissandi) > 1:
            if len(glissandi) == 2:
               common_leaves = set(glissandi[0].leaves) & \
                  set(glissandi[1].leaves)
               if len(common_leaves) == 1:
                  x = list(common_leaves)[0]
                  if (glissandi[0]._isMyFirstLeaf(x) and 
                     glissandi[1]._isMyLastLeaf(x)) or \
                     (glissandi[1]._isMyFirstLeaf(x) and 
                      glissandi[0]._isMyLastLeaf(x)):
                     break  

            for glissando in glissandi:
               if glissando not in violators:
                  violators.append(glissando)
      bad = len(violators)
      total = len(self._target.spanners.get(classname = 'Glissando'))
      if report:
         print '%4d / %4d overlapping glissando spanners.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None

   def testGnashingGlissandi(self, report = True, ret = 'violators'):
      '''Glissando interface may set on 
         only last glissando spanner leaf.'''
      violators =  [ ]
      for leaf in self._target.leaves:
         if leaf.glissando:
            glissandi = leaf.glissando.spanners
            for glissando in glissandi:
               if not glissando._isMyLastLeaf(leaf):
                  violators.append(leaf)
      bad = len(violators)
      total = len(self._target.leaves)
      if report:
         print '%4d / %4d gnashing glissando interfaces.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None


   def testOverlappingOctavation(self, report = True, ret = 'violators'):
      violators = [ ]
      for leaf in self._target.leaves:
         octavations = leaf.spanners.get(classname = 'Octavation')
         if len(octavations) > 1:
            for octavation in octavations:
               if octavation not in violators:
                  violators.append(octavation)
      bad = len(violators)
      total = len(self._target.spanners.get(classname = 'Octavation'))
      if report:
         print '%4d / %4d overlapping octavation spanners.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None 


   def testOverlappingBeams(self, report = True, ret = 'violators'):
      violators = [ ]
      for leaf in self._target.leaves:
         beams = leaf.spanners.get(classname = 'Beam')
         if len(beams) > 1:
            for beam in beams:
               if beam not in violators:
                  violators.append(beam)
      bad = len(violators)
      total = len(self._target.spanners.get(classname = 'Beam'))
      if report:
         print '%4d / %4d overlapping beam spanners.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None 


   def testUnrecognizedBeams(self, report = True, ret = 'violators'):
      violators = [ ]
      leaves = self._target.leaves
      for leaf in leaves:
         if len(leaf.spanners.get(classname = 'Beam')) != \
            len(leaf.beam.spanners):
               violators.append(leaf)
      bad = len(violators)
      total = len(leaves)
      if report:
         print '%4d / %4d leaves with unrecognized beam spanners.' % (bad, total)
      if ret == 'violators':
         return violators
      elif ret:
         return bad == 0
      else:
         return None 


   def testAll(self, report = True, ret = None,
      interface = None, grob = None, attribute = None, value = None):
      result = [ ]
      result.append(self.testParents(report = report, ret = ret))
      result.append(self.testNextLeaves(report = report, ret = ret))
      result.append(self.testPitchlessNotesChords(report = report, ret = ret))
      result.append(self.testDurationlessLeaves(report = report, ret = ret))
      result.append(self.testBadFlags(report = report, ret = ret))
      result.append(self.testContainers(report = report, ret = ret))
      result.append(self.testMeasures(report = report, ret = ret))
      result.append(self.testOverlappingGlissandi(report = report, ret = ret))
      result.append(self.testGnashingGlissandi(report = report, ret = ret))
      result.append(
         self.testSpanners(report, ret, interface, grob, attribute, value))
      result.append(self.testShortHairpins(report = report, ret = ret))
      result.append(self.testIntermarkedHairpins(report = report, ret = ret))
      result.append(self.testOverlappingOctavation(report = report, ret = ret))
      result.append(self.testOverlappingBeams(report = report, ret = ret))
      result.append(self.testUnrecognizedBeams(report = report, ret = ret))
      if report:
         print ''
      if ret == 'violators':
         new = [ ]
         for sublist in result:
            new.extend(sublist)
         return new
      elif ret:
         return all(result)
