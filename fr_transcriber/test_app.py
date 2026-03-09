import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add current directory to path so we can import transcribe_app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import customtkinter as ctk
    from transcribe_app import TranscriberApp
except ImportError:
    # If dependencies aren't installed in the environment, we might need to skip
    pass

class TestTranscriberApp(unittest.TestCase):
    @patch('customtkinter.CTk.__init__', return_value=None)
    @patch('customtkinter.CTk.grid_columnconfigure')
    @patch('customtkinter.CTk.grid_rowconfigure')
    def test_init(self, mock_row, mock_col, mock_init):
        # Basic check to see if the app can be initialized without crashing
        # (Mocking CTk specifically to avoid display issues in headless environments)
        with patch('customtkinter.CTkLabel'),              patch('customtkinter.CTkButton'),              patch('customtkinter.CTkTextbox'),              patch('customtkinter.CTkProgressBar'):
            app = TranscriberApp()
            self.assertEqual(app.model_id, "LeBenchmark/wav2vec2-FR-7k-large")
            self.assertIsNone(app.pipe)

if __name__ == "__main__":
    unittest.main()
