import json
from myio import ReadLine, Text, Language
from ai.translator import Translator
from ai.editor import Editor
from initialize import Init


(translator, editor) = Init()

with open("resources/output_little.json", "w", encoding="utf-8") as outputfile:
    for line in ReadLine("resources/german_little"):
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


#edited = editor.Edit("Bounour tout le mond", "French")
#print(edited)

#tanslation = translator.Translate(edited, "French", "English")
#print(tanslation)
