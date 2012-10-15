def apply_bass_edits(score, durated_reservoir):
    voice = score['Bass Voice']
    descents = durated_reservoir['Bass']
    voice[-3:] = '<e, e>\maxima <d, d>\longa <c, c>\maxima <b,>\longa <a,>\maxima r4 r2.'
