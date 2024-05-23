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
    # User input with default values
    filename = input("Enter the filename (default 'duolingo.txt'): ") or "duolingo.txt"
    langcode = input("Enter the language code (default 'fr-en'): ") or "fr-en"
    output_folder = input("Enter the output folder (default 'audio'): ") or "audio"

    current_date = str(datetime.now().date())
    languages = langcode.split("-")
    first_code = languages[0]
    second_code = languages[1]
    output_file = f"{current_date}_merged_vocabulary_for_{langcode}.txt"
    output_filename = f"{current_date}_vocabulary_list_for_anki_{langcode}.csv"

    print("===== EXTRACT WORDS FROM HTML =====")
    first_vocab, second_vocab = extract_vocabulary(filename)
    for i in range(len(first_vocab)):
        print(f"{first_vocab[i]} \t {second_vocab[i]}")

    print("===== SAVING VOCABULARY TEXT FILE =====")
    merge_vocabulary(first_vocab, second_vocab, output_file)
    print(f"📄 Vocabulary text file saved as '{output_file}'")

    print("===== SAVING VOCABULARY AUDIO FILES =====")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for word in first_vocab:
        generate_and_save_pronunciation(word, first_code, output_folder)

    print("===== SAVING ANKI FILE =====")
    audio_column = [f"{word} [sound:{first_code}_{word}.mp3]" for word in first_vocab]
    df = pd.DataFrame(
        {first_code: first_vocab, second_code: second_vocab, "Audio": audio_column}
    )
    df.to_csv(output_filename, index=False)
    print(f"📝 DataFrame saved as '{output_filename}'")


if __name__ == "__main__":
    main()
