# Transcripteur Français Ultra-Léger

## Installation
```bash
pip install -r requirements.txt
```

## Distribution (Exécutable Windows)
Pour créer l'exécutable .exe, utilisez la commande suivante :
```bash
pyinstaller --onefile --windowed --collect-all customtkinter --collect-all transformers --collect-all torch --name "TranscripteurAudioFR" transcribe_app.py
```
Note : Assurez-vous d'avoir assez d'espace disque car PyInstaller inclura PyTorch (environ 1-2 Go).

## Utilisation
1. Lancez l'exécutable.
2. Sélectionnez un fichier audio (.mp3, .wav, .m4a).
3. Attendez la fin de la transcription (CPU uniquement).
