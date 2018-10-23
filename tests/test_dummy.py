import unittest


class DummyTestCase(unittest.TestCase):
    def setUp(self):
        self.AN_ITEM = "item"

    def test_givenAnEmpyArray_whenAnItemIsAdded_thenArraySizeIncreases(self):
        array = []
        array_size_expected = 1

        array.append(self.AN_ITEM)

        self.assertEquals(array_size_expected, len(array))
