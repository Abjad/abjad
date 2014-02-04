# -*- encoding: utf-8 -*_


def zip_sequences(sequences, cyclic=False, truncate=True):
    r'''Zips `sequences`.
    '''
    
    if cyclic: 
        max_length = max([len(x) for x in sequences])
        result = []
        for i in range(max_length):
            part = []
            for sequence in sequences:
                index = i % len(sequence)
                element = sequence[index]
                part.append(element)
            part = tuple(part)
            result.append(part)
    elif not truncate:
        result = []
        max_length = max([len(x) for x in sequences])
        for i in range(max_length):
            part = []
            for sequence in sequences:
                try:
                    part.append(sequence[i])
                except IndexError:
                    pass
            result.append(tuple(part))
    elif truncate:
        result = zip(*sequences)

    return result
