import unittest
from speech import talk, recognize_speech
import speech_recognition as sr

class TestSpeechModule(unittest.TestCase):

    def test_talk(self):
        self.assertIsNone(talk("Test message"))

if __name__ == '__main__':
    unittest.main()
