import os
import threading
import torch
import librosa
import customtkinter as ctk
from tkinter import filedialog, messagebox
from transformers import pipeline

class TranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Transcripteur Français Ultra-Léger")
        self.geometry("600x450")

        # Configuration de l'interface
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Titre
        self.label = ctk.CTkLabel(self, text="Transcription Audio (FR)", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # Bouton de sélection
        self.select_button = ctk.CTkButton(self, text="Sélectionner un fichier audio", command=self.select_file)
        self.select_button.grid(row=1, column=0, padx=20, pady=10)

        # Zone de texte pour le résultat
        self.result_text = ctk.CTkTextbox(self, width=500, height=200)
        self.result_text.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Barre de progression
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progress_bar.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)

        # État
        self.status_label = ctk.CTkLabel(self, text="Prêt", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=4, column=0, padx=20, pady=10)

        # Initialisation du modèle (chargement différé)
        self.pipe = None
        self.model_id = "LeBenchmark/wav2vec2-FR-7k-large"

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Choisir un fichier audio",
            filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac")]
        )
        if file_path:
            self.start_transcription(file_path)

    def update_status(self, text, progress=None):
        self.status_label.configure(text=text)
        if progress is not None:
            self.progress_bar.set(progress)
        self.update_idletasks()

    def transcribe_worker(self, file_path):
        try:
            self.update_status("Chargement du modèle (CPU)...", 0.1)
            if self.pipe is None:
                self.pipe = pipeline(
                    "automatic-speech-recognition",
                    model=self.model_id,
                    device="cpu",  # Forcer le CPU
                    chunk_length_s=30,  # Découpage par morceaux
                    stride_length_s=5
                )

            self.update_status("Chargement et ré-échantillonnage de l'audio (16kHz)...", 0.3)
            # Chargement audio avec librosa, forcer 16000Hz
            audio_input, _ = librosa.load(file_path, sr=16000)

            self.update_status("Transcription en cours...", 0.6)
            # Lancement de la transcription
            result = self.pipe(audio_input)
            transcription = result["text"]

            # Mise à jour de l'interface
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", transcription)
            self.update_status("Transcription terminée !", 1.0)
            messagebox.showinfo("Succès", "La transcription est terminée.")

        except Exception as e:
            self.update_status("Erreur lors de la transcription", 0)
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        finally:
            self.select_button.configure(state="normal")

    def start_transcription(self, file_path):
        self.select_button.configure(state="disabled")
        self.result_text.delete("0.0", "end")

        # Lancer dans un thread séparé pour ne pas bloquer l'UI
        thread = threading.Thread(target=self.transcribe_worker, args=(file_path,))
        thread.start()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = TranscriberApp()
    app.mainloop()
