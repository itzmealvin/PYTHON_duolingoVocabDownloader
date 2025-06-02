import html
import os
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from gtts import gTTS
from tqdm import tqdm


class DuolingoVocabularyExtractor:
    def __init__(
        self, filename="duolingo.txt", langcode="fr-en", output_folder="audio"
    ):
        self.filename = filename
        self.langcode = langcode
        self.output_folder = output_folder
        self.first_code, self.second_code = langcode.split("-")
        self.current_date = datetime.now().strftime("%d%m")
        self.txt_output_file = f"{self.current_date}_{langcode}_merged_vocabulary.txt"
        self.csv_output_file = f"{self.current_date}_{langcode}_anki_vocabulary.csv"
        self.source_vocab = []
        self.target_vocab = []

    def extract_vocabulary(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
            word_pairs = soup.find_all("div")

            first_vocab = []
            second_vocab = []

            for word_pair in word_pairs[3:]:
                first_word = word_pair.find("h3")
                second_word = word_pair.find("p")
                if first_word and second_word:
                    first_vocab.append(html.unescape(first_word.text.strip()))
                    second_vocab.append(
                        html.unescape(second_word.text.strip()).replace(",", "/")
                    )

            self.source_vocab = first_vocab[5:][::3]
            self.target_vocab = second_vocab[5:][::3]

    def save_vocabulary_text_file(self):
        with open(self.txt_output_file, "w", encoding="utf-8") as file:
            for src, tgt in zip(self.source_vocab[2:], self.target_vocab[2:]):
                file.write(f"{src}\t{tgt}\n")
        print(f"Saved TXT vocabulary to {self.txt_output_file}")

    def generate_audio_files(self):
        os.makedirs(self.output_folder, exist_ok=True)
        for word in tqdm(self.source_vocab, desc="Generating audio"):
            self._generate_and_save_pronunciation(word, self.first_code)

    def _generate_and_save_pronunciation(self, word, lang_code):
        try:
            tts = gTTS(word, lang=lang_code)
            filename = f"{lang_code}_{word}.mp3"
            filepath = os.path.join(self.output_folder, filename)
            tts.save(filepath)
        except Exception as e:
            print(f"Failed to generate audio for '{word}': {e}")

    def create_anki_csv(self):
        audio_col = [
            f"{word} [sound:{self.first_code}_{word}.mp3]" for word in self.source_vocab
        ]
        df = pd.DataFrame(
            {
                self.first_code: self.source_vocab,
                self.second_code: self.target_vocab,
                "Audio": audio_col,
            }
        )
        df.to_csv(self.csv_output_file, index=False)
        print(f"Saved CSV to {self.csv_output_file}")

    def run(self):

        print("===== EXTRACTING WORDS FROM HTML =====")
        self.extract_vocabulary()
        for src, tgt in zip(self.source_vocab, self.target_vocab):
            print(f"{src} \t {tgt}")

        print("===== SAVING VOCABULARY TEXT FILE =====")
        self.save_vocabulary_text_file()

        print("===== GENERATING AUDIO FILES =====")
        self.generate_audio_files()

        print("===== CREATING ANKI CSV FILE =====")
        self.create_anki_csv()


if __name__ == "__main__":
    print("===== DUOLINGO VOCABULARY EXTRACTOR =====")
    filename = input("Enter the filename (default 'duolingo.txt'): ") or "duolingo.txt"
    langcode = input("Enter the language code (default 'fr-en'): ") or "fr-en"
    output_folder = input("Enter the output folder (default 'audio'): ") or "audio"

    extractor = DuolingoVocabularyExtractor(filename, langcode, output_folder)
    extractor.run()
