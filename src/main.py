import os
import json
import argparse
import logging
import ioutil
from tqdm import tqdm
from ai.types import Text, Language
from ai.editor import Editor
from ai.translator import Translator
from initialize import initialize_services

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Silence verbose logs from the HTTP client libraries
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


def process_line(line: str, editor: Editor, translator: Translator) -> dict | None:
    """Processes a single line of text: edits, translates, and formats it."""
    original = Text(contents=line, language=Language.GERMAN)

    edited = editor.edit(original)
    if not edited:
        logging.warning(f"Skipping line due to editing error: '{original.contents}'")
        return None

    english = translator.translate(edited, Language.ENGLISH)
    if not english:
        logging.warning(f"Skipping line due to English translation error: '{edited.contents}'")
        return None

    serbian = translator.translate(edited, Language.SERBIAN)
    if not serbian:
        logging.warning(f"Skipping line due to Serbian translation error: '{edited.contents}'")
        return None

    return dict(
        original=original._asdict(),
        edited=edited._asdict(),
        translations=[english._asdict(), serbian._asdict()]
    )

def process_flashcards(input_path: str, output_path: str):
    """
    Reads sentences from an input file, edits them, translates them,
    and writes the results to a JSONL output file.
    """
    try:
        translator, editor = initialize_services()
    except ValueError as e:
        logging.error(f"Initialization failed: {e}")
        return

    file_size = ioutil.get_file_size(input_path)
    logging.info(f"Processing {input_path} ({float(file_size) / 1024:.2f} KB) to '{output_path}'.")

    lines_processed = 0
    lines_skipped = 0
    try:
        with open(output_path, "w", encoding="utf-8") as outputfile, \
            tqdm(total=file_size, unit="B", unit_scale=True, desc="Processing", unit_divisor=1024, ascii="->=", colour='green') as pbar:

            for line in ioutil.read_lines(input_path):
                output_data = process_line(line.contents, editor, translator)
                pbar.update(line.bytes)

                if not output_data:
                    lines_skipped += 1
                    continue
                lines_processed += 1

                json.dump(output_data, outputfile, ensure_ascii=False)
                outputfile.write("\n")
    except KeyboardInterrupt:
        logging.info(f"Processing interrupted by user.")

    logging.info(f"Processed {lines_processed} lines")
    logging.info(f"Skipped {lines_skipped} lines")
    logging.info("Completed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process text notes to create flashcards.")
    parser.add_argument("-i", "--input", default="resources/german", help="Path to the input file with sentences.")
    parser.add_argument("-o", "--output", default="resources/output.jsonl", help="Path to the output JSONL file.")
    args = parser.parse_args()
    process_flashcards(args.input, args.output)