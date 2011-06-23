def compare_timepoints_to_q_grid(timepoints, q_grid, lookup):
   '''Compare `timepoints` to `q_grid`, with the aid of `lookup`
   for determining actual millisecond position.

   Returns the cumulative quantization error and the best-match
   Q-grid points.

   This function does no error-checking for purpose of speed,
   and should be used with caution.'''

   points = [ ]
   error = 0
   for timepoint in timepoints:
      q = q_grid[0]
      best_point = q
      best_error = int(abs(lookup[q] - timepoint))
      for q in q_grid[1:]:
         curr_error = int(abs(lookup[q] - timepoint))
         if curr_error < best_error:
            best_point = q
            best_error = curr_error
      points.append(best_point)
      error += best_error
   return error, points
