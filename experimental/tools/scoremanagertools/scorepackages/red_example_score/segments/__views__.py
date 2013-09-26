# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.scoremanagertools import io


view_inventory=datastructuretools.TypedList([
	io.View([
		'segment 03',
		'segment 02',
		'segment 01'
		],
		name='reverse order'
		)
	])