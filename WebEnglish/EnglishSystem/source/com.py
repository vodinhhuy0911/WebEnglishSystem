import itertools
import operator

from gensim.summarization.bm25 import BM25
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline


class QuestionProcessor:
    def __init__(self, nlp, keep_pos=None):
        self.nlp = nlp
        # self.keep_pos = keep_pos or {'PROPN', 'NUM', 'VERB', 'NOUN', 'ADJ', 'PRON', 'DET', 'ADV', 'PART', 'SYM'}
        self.keep_pos = keep_pos or {'ADJ','ADP','ADV','AUX','CONJ','CCONJ','DET','INTJ','NOUN','NUM','PART','PRON','PROPN','PUNCT','SCONJ','SYM', 'VERB'}
    def generate_question(self, text):
        doc = self.nlp(text)
        question = ' '.join(token.text for token in doc if token.pos_ in self.keep_pos)
        return question


class PassageRetrieval:
    def __init__(self, nlp):
        self.tokenize = lambda text: [token.lemma_ for token in nlp(text)]
        self.bm25 = None
        self.passages = None

    def pre_process(self, doc):
        # passages = [p for p in doc.split('\n') if p and len(p.split(' ')) > 5]
        passages = [p for p in doc.split('\n') if p]
        return passages

    def fit(self, docs):
        passages = list(itertools.chain(*map(self.pre_process, docs)))
        corpus = [self.tokenize(p) for p in passages]
        self.bm25 = BM25(corpus)
        self.passages = passages

    def most_similar(self, question, top=10):
        tokens = self.tokenize(question)
        scores = self.bm25.get_scores(tokens)
        pairs = [(s, i) for i, s in enumerate(scores)]
        # print(scores)
        pairs.sort(reverse=True)
        passages = [self.passages[i] for _, i in pairs[:top]]
        return passages


class AnswerExtractor:
    def __init__(self, tokenizer, model):
        tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        model = AutoModelForQuestionAnswering.from_pretrained(model)
        self.nlp = QuestionAnsweringPipeline(model=model, tokenizer=tokenizer)

    def extract(self, question, passages):
        answers_list = []
        for context in passages:
            try:
                answer = self.nlp(question=question, context=context)
                answer['text'] = context
                answers_list.append(answer)
            except KeyError:
                pass
        answers_list.sort(key=operator.itemgetter('score'), reverse=True)
        return answers_list

