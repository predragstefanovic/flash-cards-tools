# flash-cards-tools

Tools to process notes from a langauge conversation course.

## Editor

Proof-reads and edits short sentences for a given language. Integrates with OPENAI API.

## Translator

Translates short sentences between given langauges. Integrates with OPENAI API.

## Flash Cards Pre-processor

Simple pipeline consisting of the Editor and Translator tools to prepare data for flashcard-deck. 

```
German Sentence -> Edits German -> Translates German to English
                                -> Translates German to Serbian
```

Runs for about 400 sentences and 1800 words with chatgpt4.1-nano, totalling ~1 cent in costs.
Note, it takes several minutes to run and without any tolarance to transient errors, the pipeline runs all or nothing.