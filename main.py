"""
This module extracts vocabulary from Duolingo HTML files,
saves them into a text file, generates audio, and outputs
an Anki-compatible CSV.

Functions:
    main(): Runs the vocabulary extraction and export workflow.
    extract_vocabulary(filename): Parses the HTML and returns vocab lists.
    merge_vocabulary(list1, list2, output_file): Writes merged vocab to a text file.
    generate_and_save_pronunciation(word, lang_code, output_folder): Saves MP3 for each word.
"""

import html
import os
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from gtts import gTTS


def extract_vocabulary(filename):
    """
    Extract vocabulary pairs from the given HTML file.

    Args:
        filename (str): Path to the HTML file.

    Returns:
        tuple: Lists of first and second vocabulary words.
    """
    first_vocabulary = []
    second_vocabulary = []

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
        soup = BeautifulSoup(text, "html.parser")

        word_pairs = soup.find_all("div")

        for word_pair in word_pairs[3:]:
            first_word = word_pair.find("h3")
            second_word = word_pair.find("p")
            if first_word and second_word:
                first_vocabulary.append(html.unescape(first_word.text.strip()))
                second_vocabulary.append(
                    html.unescape(second_word.text.strip()).replace(",", "/")
                )

    first_vocabulary = first_vocabulary[5:]
    second_vocabulary = second_vocabulary[5:]
    return first_vocabulary[::3], second_vocabulary[::3]


def merge_vocabulary(first_vocabulary, second_vocabulary, output_file):
    """
    Merge the first and second vocabulary lists into a single file.

    Args:
        first_vocabulary (list): List of first vocabulary words.
        second_vocabulary (list): List of second vocabulary words.
        output_file (str): Path to the output file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        for first_word, second_word in zip(first_vocabulary[2:], second_vocabulary[2:]):
            line = f"{first_word}\t{second_word}\n"
            file.write(line)


def generate_and_save_pronunciation(word, lang_code, output_folder):
    """
    Generate and save the pronunciation of a word.

    Args:
        word (str): The word to generate pronunciation for.
        lang_code (str): The language code for pronunciation.
        output_folder (str): The folder to save the audio file.
    """
    tts = gTTS(word, lang=lang_code)
    filename = f"{lang_code}_{word}.mp3"
    filepath = os.path.join(output_folder, filename)
    tts.save(filepath)
    print(f"📥 Saved audio for '{word}' to '{filepath}'")

def main():
    """
    Driver code to extract Duolingo vocabulary, generate audio, and prepare an Anki-friendly CSV.
    """
    filename = input("Enter the filename (default 'duolingo.txt'): ") or "duolingo.txt"
    langcode = input("Enter the language code (default 'fr-en'): ") or "fr-en"
    output_folder = input("Enter the output folder (default 'audio'): ") or "audio"

    current_date = datetime.now().strftime("%Y-%m-%d")
    first_code, second_code = langcode.split("-")
    txt_output_file = f"{current_date}_merged_vocabulary_for_{langcode}.txt"
    csv_output_file = f"{current_date}_vocabulary_list_for_anki_{langcode}.csv"

    print("===== EXTRACTING WORDS FROM HTML =====")
    source_vocab, target_vocab = extract_vocabulary(filename)
    for src, tgt in zip(source_vocab, target_vocab):
        print(f"{src} \t {tgt}")

    print("===== SAVING VOCABULARY TEXT FILE =====")
    merge_vocabulary(source_vocab, target_vocab, txt_output_file)
    print(f"📄 Saved vocabulary as '{txt_output_file}'")

    print("===== GENERATING AUDIO FILES =====")
    os.makedirs(output_folder, exist_ok=True)

    for word in source_vocab:
        generate_and_save_pronunciation(word, first_code, output_folder)

    print("===== CREATING ANKI CSV FILE =====")
    audio_col = [f"{word} [sound:{first_code}_{word}.mp3]" for word in source_vocab]
    df = pd.DataFrame({
        first_code: source_vocab,
        second_code: target_vocab,
        "Audio": audio_col
    })
    df.to_csv(csv_output_file, index=False)
    print(f"📝 CSV saved as '{csv_output_file}'")

if __name__ == "__main__":
    main()
