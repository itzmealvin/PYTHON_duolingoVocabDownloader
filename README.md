# SEMI-AUTO DUOLINGO VOCABULARY LIST DOWNLOADER

## PRE-REQUISITES

Before using this tool, ensure you have the following:

- A Python environment set up on your system.
- The necessary libraries installed. You can do this by running the command:
  ```sh
  pip3 install -r requirements.txt
  ```
- A Duolingo Plus account.

## STEPS TO USE THE TOOL

Follow these steps to download and process your Duolingo vocabulary:

### 1. Log In to Duolingo

Log in to your Duolingo account using your web browser.

### 2. Navigate to the Words Section

Go to the following URL:
[Duolingo Practice Hub - Words](https://www.duolingo.com/practice-hub/words)

### 3. Open Developer Tools

Right-click on any area of the page and select "Inspect" to open the Developer Tools.

### 4. Load All Words

Scroll down the list of words and click "Load more" until you reach the end of the list.

### 5. Copy HTML Content

Right-click on the first `<html>` element in the Developer Tools, then select "Copy" > "Copy element".

### 6. Save HTML to File

Paste the copied HTML content into a text file. You can name this file anything you like, but for the default settings, save it as `duolingo.txt` or any name you want.

### 7. Run the Script

Open a terminal and run the following command:

```sh
python3 main.py
```

### 8. Provide Script Inputs

The script will prompt you for some information:

- **Filename**: Enter the name of the file where you saved the HTML content (default is `duolingo.txt`).
- **Language Code**: Enter the language code for the words you want to download (default is `fr-en`). For more language codes, refer to the [gTTS documentation](https://gtts.readthedocs.io/en/latest/module.html).
- **Output Folder**: Enter the name of the folder where you want to save the audio files (default is `audio`).

## OUTPUT

After running the script, you will get the following outputs:

- **Vocabulary File**: A text file named `{current_date}_merged_vocabulary_for_{langcode}.txt` containing the merged vocabulary pairs.
- **Anki File**: A CSV file named `{current_date}_vocabulary_list_for_anki_{langcode}.csv` compatible with Anki for flashcard creation.
- **Audio Files**: An output folder (default `audio`) containing TTS (Text-to-Speech) audio files generated using Google TTS for each word.

The files are named with the current date and the language code to help keep them organized.
