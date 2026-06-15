import unittest
import cv2

class TestCameraHardware(unittest.TestCase):
    
    def test_main_camera_opens_successfully(self):
        """Test sprawdza, czy fizyczna kamera o indeksie 0 się otwiera."""
        
        cap = cv2.VideoCapture(0)
        
        is_opened = cap.isOpened()
        
        if is_opened:
            success, frame = cap.read()
            cap.release()
            
            self.assertTrue(success, "Kamera się otworzyła, ale nie potrafi pobrać obrazu (klatka jest pusta).")
        else:
            cap.release()
            
        self.assertTrue(is_opened, "BŁĄD: Nie można otworzyć kamery o indeksie 0. Sprawdź menedżer urządzeń.")

if __name__ == '__main__':
    unittest.main()