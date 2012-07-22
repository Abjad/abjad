from experimental import quantizationtools


def test_UnmeteredQSchema___init___01():

    item_a = quantizationtools.UnmeteredQSchemaItem(tempo=((1, 4), 76))
    item_b = quantizationtools.UnmeteredQSchemaItem(beatspan=(1, 8))
    #item_c = quantizationtools.UnmeteredQSchemaItem(search_tree=None)

    schema = quantizationtools.UnmeteredQSchema({
        2: item_a,
        4: item_b
        })
