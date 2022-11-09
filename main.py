# make sure your downloaded the english model with "python -m spacy download en"

import spacy
nlp_en = spacy.load('en_core_web_lg')
nlp_de = spacy.load('de_core_news_lg')


def select_contexts(sentence, lang):
    doc = nlp_en(sentence) if lang == 'en' else nlp_de(sentence)
    lemma_prev = None
    for token in doc:
        lemma = token.lemma_
        if (lemma_prev == 'have' and lemma == 'to') or (lemma_prev == 'need' and lemma == 'to'):
            return sentence
        if (lemma == 'müssen') or (lemma == 'brauchen'):
            return sentence
        lemma_prev = lemma
    return None


def compile_text(filename, lang):
    selected = []
    file = open(filename, "r")
    for id, sentence in enumerate(list(file), start=1):
        result = select_contexts(sentence, lang)
        if result is not None:
            selected.append((str(id), lang, result))
    file.close()
    return selected


results = compile_text('woland/text/de.txt', 'de')
results.extend(compile_text('woland/text/en.txt', 'en'))
results.sort(key=lambda x: int(x[0]))

file = open("result.tsv", "w")
for sentence in results:
    file.write("\t".join(sentence))
file.close()
