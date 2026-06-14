import unittest
import barki


class TestBarkiJednostkowe(unittest.TestCase):
    def setUp(self):
        barki.AKTYWNY = False
        barki.counter = 0

    def test_zatrzymaj_trening(self):
        barki.AKTYWNY = True
        barki.counter = 12

        wynik = barki.zatrzymaj_trening()

        self.assertFalse(barki.AKTYWNY)
        self.assertEqual(wynik, 12)
        self.assertEqual(barki.counter, 0)


if __name__ == '__main__':
    unittest.main()