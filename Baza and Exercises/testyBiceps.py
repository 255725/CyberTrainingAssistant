import unittest
from unittest.mock import patch, MagicMock
import biceps

class TestBicepsyJednostkowe(unittest.TestCase):
    def setUp(self):
        biceps.AKTYWNY = False
        biceps.counter = 0

    def test_zatrzymaj_trening(self):
        biceps.AKTYWNY = True
        biceps.counter = 8

        wynik = biceps.zatrzymaj_trening()

        self.assertFalse(biceps.AKTYWNY)
        self.assertEqual(wynik, 8)
        self.assertEqual(biceps.counter, 0)

class TestBicepsyPoprawnosciowe(unittest.TestCase):
    def setUp(self):
        biceps.AKTYWNY = False
        biceps.counter = 0

    @patch('exercise_utils.setup_mediapipe')
    @patch('exercise_utils.inicjalizuj_trening')
    @patch('exercise_utils.setup_cameras')
    @patch('exercise_utils.pobierz_i_przetworz_obraz')
    @patch('exercise_utils.pobierz_kat_i_rysuj')
    @patch('exercise_utils.combine_and_draw_ui')
    @patch('cv2.imencode')
    def test_logika_zliczania_powtorzen(self, mock_imencode, mock_ui, mock_kat, mock_pobierz, mock_cam,
                                        mock_inicjalizuj, mock_setup):
        mock_setup.return_value = (MagicMock(), MagicMock(), MagicMock(), MagicMock())
        mock_inicjalizuj.return_value = (0, "lifting", "", "", "")
        mock_cam.return_value = (MagicMock(), MagicMock(), False)

        mock_active_results = MagicMock()
        mock_active_results.pose_landmarks.landmark = "mock_dane"

        mock_pobierz.side_effect = [
            (True, MagicMock(), None, mock_active_results, 480, 640, False),
            (True, MagicMock(), None, mock_active_results, 480, 640, False),
            (False, None, None, None, 0, 0, False)
        ]

        mock_kat.side_effect = [160, 30]

        mock_imencode.return_value = (True, MagicMock(tobytes=lambda: b'test_frame'))

        generator = biceps.generuj_obraz_biceps()

        next(generator)
        next(generator)

        try:
            next(generator)
        except StopIteration:
            pass

        self.assertEqual(biceps.counter, 1)

if __name__ == '__main__':
    unittest.main()