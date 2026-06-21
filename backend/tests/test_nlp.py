from parlamente.nlp.clean import clean_text, tokenize
from parlamente.nlp.keywords import KeywordExtractor
from parlamente.nlp.stopwords_it import get_italian_stopwords
from parlamente.nlp.taxonomy import classify, load_taxonomy


def test_clean_removes_urls_and_lowercases():
    out = clean_text("Vedi https://camera.it Le LISTE d'attesa")
    assert "http" not in out
    assert out == out.lower()


def test_tokenize_filters_stopwords():
    sw = set(get_italian_stopwords())
    toks = tokenize("Il presidente parla delle liste attesa sanità", stopwords=sw)
    # 'il' e 'presidente' (rumore parlamentare) devono sparire
    assert "presidente" not in toks
    assert "liste" in toks and "sanita" not in toks or "sanità" in " ".join(toks)


def test_taxonomy_loaded():
    tax = load_taxonomy()
    assert len(tax) >= 30
    ids = {t.id for t in tax}
    assert "san_liste_attesa" in ids


def test_classify_health_topic():
    hits = dict(classify("Servono interventi sulle liste d'attesa e medicina territoriale"))
    assert "san_liste_attesa" in hits
    # le locuzioni multi-parola pesano di più
    assert hits["san_liste_attesa"] >= 1.0


def test_keyword_extractor_returns_ngrams():
    extractor = KeywordExtractor(min_df=1)
    docs = [
        "salario minimo e occupazione, salario minimo per i lavoratori",
        "fisco tasse imprese e debito pubblico",
    ]
    res = extractor.extract_per_document(docs, top_n=10)
    assert len(res) == 2
    kws0 = {k.keyword for k in res[0]}
    # almeno un bigramma atteso
    assert any(" " in k for k in kws0)
