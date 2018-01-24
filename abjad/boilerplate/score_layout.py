import baca


breaks = baca.breaks(
    baca.page( # 1
        [1, 75, (15, 20)],
        [16, 170, (15, 20)],
        ),
    baca.page( # 2
        [33, 20, (15, 20)],
        [49, 130, (15, 20)],
        ),
    )
