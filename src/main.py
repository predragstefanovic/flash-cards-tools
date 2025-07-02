import json
from myio import ReadLine, Text, Language
from initialize import Init


(translator, editor) = Init()

with open("resources/output.json", "w", encoding="utf-8") as outputfile:
    for line in ReadLine("resources/german"):
        original = Text(contents=line, language=Language.GERMAN)
        edited = Text(
            contents=editor.Edit(original.contents, original.language), 
            language=original.language
        )

        english = Text(
            contents=translator.Translate(edited.contents, edited.language,  Language.ENGLISH),
            language=Language.ENGLISH
        )
        
        serbian = Text(
            contents=translator.Translate(edited.contents, edited.language, Language.SERBIAN),
            language=Language.SERBIAN
        )

        output = dict(
            original=original._asdict(),
            edited=edited._asdict(),
            translations=[english._asdict(), serbian._asdict()]
        )

        json.dump(output, outputfile, ensure_ascii=False)