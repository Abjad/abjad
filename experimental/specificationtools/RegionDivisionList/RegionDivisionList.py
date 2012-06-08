from specificationtools.DivisionList import DivisionList


class RegionDivisionList(DivisionList):
    r'''What is a region?
    A region is an uniterrupted block of time over which a division source 'lays out' without interruption.
    A context given 1 *nontruncating* division specification interprets as 1 region.
    Generally, a context given d *nontruncating* division specifications interprets as d regions.
    A context given 1 *truncating* division source interprets as r regions, with r the number of regions.
    (The interaction between d *truncating* division sources and r regions is more complex.)
    '''

    pass
