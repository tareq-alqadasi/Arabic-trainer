# Prompt: translate the interface into one language

Use it once per language with a cheap model (or let `translate_ui.py` do the loop for you).
Replace `{{LANGUAGE}}` (name in English, e.g. `French`) and `{{JSON}}` (one batch of `ui/en.json`, see below).

---

You are a professional UI localizer. Translate the VALUES of the JSON object below from English into **{{LANGUAGE}}**.

Context: a small offline language-learning app (flash-card sentence practice with levels, spaced repetition, notes on words, themes, deck options). The user is a learner who speaks {{LANGUAGE}}.

Hard rules (the output is checked by a program; a wrong answer is rejected):
1. Output ONE JSON object only. No explanation, no markdown fence, no comments.
2. Keep every KEY exactly as given and keep ALL keys. Only values change.
3. Placeholders must be kept exactly and the same number of times: `{n}` = a number, `{L}` = the name of a language. Do not translate, rename, add or remove them. You may move them where the grammar of {{LANGUAGE}} needs it.
4. Keep emoji, arrows (← → ↶ ↷ ▶), ellipsis (…), ＋, ✓ ✗, 🚩, ✎, 👁, ⬇, ⬆ and similar symbols where they are. Keep `“ ”` quotes style natural for {{LANGUAGE}}.
5. Short and natural, like real app buttons and hints. Buttons: imperative or noun, as usual in {{LANGUAGE}} apps. Friendly, not formal-legal. Use the singular "you" form that apps normally use in {{LANGUAGE}}.
6. Some keys are sentence FRAGMENTS (they continue after a bold word, or end with a colon or “·”). Translate the fragment so it still reads correctly when fragments are shown one after the other.
7. Do not translate: `CSV`, `JSON`, `CSS`, `Anki`, `AI`, `XP` unless {{LANGUAGE}} has a well-established form; the characters `…` in pattern examples; the Arabic example text ي-غادر-ون, ال… and similar examples.
8. Words used in the app and how to render them:
   - "sentence" = a full example sentence being studied;
   - "level" and "chunk" = a step of the course and a small batch inside it;
   - "group" / "deck" = a collection of sentences;
   - "deck options" / "preset" = settings of a deck and a named saved set of them;
   - "note" = the learner's own note on a word, affix or construction;
   - "construction" = a note about the shape of a phrase (e.g. X X), not a word;
   - "tag" = a label on a note;
   - "flag" = a mark to find a sentence again;
   - "Again / Good" = the two self-rating buttons (like Anki);
   - "known language" = the language the learner speaks; sentences are explained in it;
   - "side translation" = an extra translation shown beside the known-language sentence;
   - "interface language" = the language of menus and buttons;
   - "grading": Self = the learner rates the answer, Auto = the app decides;
   - "tashkīl" = Arabic vowel marks (keep the word as is);
   - "known words" = words the learner already knows from outside the app.
9. If the target language is written right-to-left, simply write the translation normally; do not add direction marks.

The object has two parts, translate both:
- "strings": interface texts.
- "names": names of languages. Give each name as a native speaker of {{LANGUAGE}} calls that language (e.g. German → «Allemand» in French). If {{LANGUAGE}} itself is in the list, keep the usual name.

JSON:
{{JSON}}