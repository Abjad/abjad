def nearest_neighbor(pitchNumber, pc):
   targetPC = pitchNumber % 12
   down = (targetPC - pc) % 12
   up = (pc - targetPC) % 12
   if up < down:
      return pitchNumber + up
   else:
      return pitchNumber - down
