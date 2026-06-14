import unittest
from unittest.mock import patch, MagicMock
import wyskok
import mediapipe as mp
import numpy as np

class MockLandmark:
    def __init__(self, y):
        self.y = y

def generuj_mock_results(nose_y, hip_y, ankle_y, wrist_y):
    lms = [MockLandmark(0.0) for _ in range(33)]
    lms[0] = MockLandmark(nose_y)
    lms[24] = MockLandmark(hip_y)
    lms[28] = MockLandmark(ankle_y)
    lms[15] = MockLandmark(wrist_y)
    lms[16] = MockLandmark(wrist_y)

    mock_res = MagicMock()
    mock_res.pose_landmarks.landmark = lms
    return mock_res

class TestWyskokJednostkowe(unittest.TestCase):
    def setUp(self):
        wyskok.AKTYWNY = False
        wyskok.counter = 0

    def test_zatrzymaj_trening(self):
        wyskok.AKTYWNY = True
        wyskok.counter = 5

        wynik = wyskok.zatrzymaj_trening()

        self.assertFalse(wyskok.AKTYWNY)
        self.assertEqual(wynik, 5)
        self.assertEqual(wyskok.counter, 0)

class TestWyskokPoprawnosciowe(unittest.TestCase):
    def setUp(self):
        wyskok.AKTYWNY = False
        wyskok.counter = 0

    @patch('exerciseUtils.setup_mediapipe')
    @patch('exerciseUtils.inicjalizuj_trening')
    @patch('exerciseUtils.setup_cameras')
    @patch('exerciseUtils.pobierz_i_przetworz_obraz')
    @patch('exerciseUtils.combine_and_draw_ui')
    @patch('cv2.imencode')
    @patch('time.time')
    def test_logika_zliczania_powtorzen(self, mock_time, mock_imencode, mock_ui, mock_pobierz, mock_cam,
                                        mock_inicjalizuj, mock_setup):
        mock_setup.return_value = (mp.solutions.pose, MagicMock(), MagicMock(), MagicMock())
        mock_inicjalizuj.return_value = (0, None, "", "", "")
        mock_cam.return_value = (MagicMock(), MagicMock(), False)
        mock_ui.return_value = np.zeros((480, 640, 3), dtype=np.uint8)

        mock_time.side_effect = [100.0, 100.0, 104.0, 104.0, 104.0, 104.0]

        mock_pobierz.side_effect = [
            (True, MagicMock(), None, generuj_mock_results(0.5, 0.6, 1.0, 0.1), 480, 640, False),
            (True, MagicMock(), None, generuj_mock_results(0.5, 0.6, 1.0, 0.1), 480, 640, False),
            (True, MagicMock(), None, generuj_mock_results(0.5, 0.8, 1.0, 0.8), 480, 640, False),
            (True, MagicMock(), None, generuj_mock_results(0.5, 0.4, 1.0, 0.8), 480, 640, False),
            (True, MagicMock(), None, generuj_mock_results(0.5, 0.6, 1.0, 0.8), 480, 640, False),
            (False, None, None, None, 0, 0, False)
        ]

        mock_imencode.return_value = (True, MagicMock(tobytes=lambda: b'test_frame'))

        generator = wyskok.generuj_obraz_wyskok()

        for _ in range(5):
            next(generator)

        try:
            next(generator)
        except StopIteration:
            pass

        self.assertEqual(wyskok.counter, 1)

if __name__ == '__main__':
    unittest.main()