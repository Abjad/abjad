from abjad.tools import contexttools


def apply_dynamic_marks(score):

    voice = score['Bell Voice']
    contexttools.DynamicMark('ppp')(voice[0][1])
    contexttools.DynamicMark('pp')(voice[8][1])
    contexttools.DynamicMark('p')(voice[18][1])
    contexttools.DynamicMark('mp')(voice[26][1])
    contexttools.DynamicMark('mf')(voice[34][1])
    contexttools.DynamicMark('f')(voice[42][1])
    contexttools.DynamicMark('ff')(voice[52][1])
    contexttools.DynamicMark('fff')(voice[60][1])
    contexttools.DynamicMark('ff')(voice[68][1])
    contexttools.DynamicMark('f')(voice[76][1])
    contexttools.DynamicMark('mf')(voice[84][1])
    contexttools.DynamicMark('pp')(voice[-1][0])

    voice = score['First Violin Voice']
    contexttools.DynamicMark('ppp')(voice[6][1])
    contexttools.DynamicMark('pp')(voice[15][0])
    contexttools.DynamicMark('p')(voice[22][3])
    contexttools.DynamicMark('mp')(voice[31][0])
    contexttools.DynamicMark('mf')(voice[38][3])
    contexttools.DynamicMark('f')(voice[47][0])
    contexttools.DynamicMark('ff')(voice[55][2])
    contexttools.DynamicMark('fff')(voice[62][2])

    voice = score['Second Violin Voice']
    contexttools.DynamicMark('pp')(voice[7][0])
    contexttools.DynamicMark('p')(voice[12][0])
    contexttools.DynamicMark('p')(voice[16][0])
    contexttools.DynamicMark('mp')(voice[25][1])
    contexttools.DynamicMark('mf')(voice[34][1])
    contexttools.DynamicMark('f')(voice[44][1])
    contexttools.DynamicMark('ff')(voice[54][0])
    contexttools.DynamicMark('fff')(voice[62][1])

    voice = score['Viola Voice']
    contexttools.DynamicMark('p')(voice[8][0])
    contexttools.DynamicMark('mp')(voice[19][1])
    contexttools.DynamicMark('mf')(voice[30][0])
    contexttools.DynamicMark('f')(voice[36][0])
    contexttools.DynamicMark('f')(voice[42][0])
    contexttools.DynamicMark('ff')(voice[52][0])
    contexttools.DynamicMark('fff')(voice[62][0])

    voice = score['Cello Voice']
    contexttools.DynamicMark('p')(voice[10][0])
    contexttools.DynamicMark('mp')(voice[21][0])
    contexttools.DynamicMark('mf')(voice[31][0])
    contexttools.DynamicMark('f')(voice[43][0])
    contexttools.DynamicMark('ff')(voice[52][1])
    contexttools.DynamicMark('fff')(voice[62][0])

    voice = score['Bass Voice']
    contexttools.DynamicMark('mp')(voice[14][0])
    contexttools.DynamicMark('mf')(voice[27][0])
    contexttools.DynamicMark('f')(voice[39][0])
    contexttools.DynamicMark('ff')(voice[51][0])
    contexttools.DynamicMark('fff')(voice[62][0])
