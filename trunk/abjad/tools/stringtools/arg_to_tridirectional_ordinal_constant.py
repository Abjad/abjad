def arg_to_tridirectional_ordinal_constant(arg):
    lookup = {
        Up: Up,
        '^': Up,
        'up': Up,
        1: Up,
        Down: Down,
        '_': Down,
        'down': Down,
        -1: Down,
        Center: Center,
        '-': Center,
        0: Center,
        'center': Center,
        'default': Center,
        'neutral': Center,
    }
    if arg is None:
        return None
    elif arg in lookup:
        return lookup[arg]
    raise ValueError

