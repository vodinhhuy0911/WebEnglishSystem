import os
import spacy
import warnings
from .com import QuestionProcessor,  PassageRetrieval, AnswerExtractor

warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)


def get_context(text):
    context1 = text.split("Questions:")
    return context1[0].strip()


def get_question_list(text):
    context = text.split("Questions:")
    question = context[1].strip().split("\n")
    return question


def get_question(q_list):
    questions = q_list.split("__")
    return questions


def question_classification(question):
    question = str(question).lower()
    # Exception Question
    if question.find("except") != -1 or question.find("excepts") != -1:
        # print(question)
        return 1

    # Incomplete Question
    elif question.find("-------") != -1:
        # print(question + " ")
        return 2
    elif question[len(question) - 1] not in '''!?.''':
        # if question.find("closest") == -1 and question.find("meaning") == -1 and question.find("refers to") == -1:
        #     print(question + " dytdg")
        # else:
        #     print("bbb")
        return 3

    # Complete Question
    else:
        # print('aaaa')
        return 4


def get_final_answer(answer_list, answers, maxrange):
    final_answers = [0.0, 0.0, 0.0, 0.0]
    max_score = 0
    fa = ""
    for answer in answers:
        if nlp(answer['answer']).vector_norm:
            sum_similarity = 0
            for temp0 in range(0, maxrange):
                sum_similarity += float(nlp(answer_list[temp0]).similarity(nlp(answer['answer'])))
            if sum_similarity == 0:
                sum_similarity = 1
            for temp1 in range(0, maxrange):
                if final_answers[temp1] < answer['score'] * float(nlp(answer_list[temp1]).similarity(nlp(answer['answer']))) / sum_similarity:
                    final_answers[temp1] = answer['score'] * float(nlp(answer_list[temp1]).similarity(nlp(answer['answer']))) / sum_similarity
                if max_score <= final_answers[temp1]:
                    max_score = final_answers[temp1]
                    if temp1 == 0:
                        fa = "A. "
                    elif temp1 == 1:
                        fa = "B. "
                    elif temp1 == 2:
                        fa = "C. "
                    else:
                        fa = "D. "
                    # fa += answer_list[temp1]
    return  final_answers
    # return "Answer: " + fa

def get_exception_question_answer(text, questions, answer_list, question_processor, passage_retriever):
    final_answers = [0.0, 0.0, 0.0, 0.0]
    SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_lg')
    nlp = spacy.load(SPACY_MODEL)
    passage_retriever.fit([text])
    questions = questions.lower().replace("excepts", "").replace("except", "")
    question = question_processor.generate_question(questions)
    passages = passage_retriever.most_similar(question)
    final_ans = 0
    step = 0
    min = 1
    for ans in answer_list:
        for p in passages:
            for sents in nlp(p).sents:
                # print(float(nlp(sents.text).similarity(nlp(question + " " + ans))))
                if min >= float(nlp(sents.text).similarity(nlp(question + " " + ans))):
                    min = float(nlp(sents.text).similarity(nlp(question + " " + ans)))

                    final_answers[answer_list.index(sents)] = float(nlp(sents.text).similarity(nlp(question + " " + ans)))
                    final_ans = step
        step += 1
    if final_ans == 0:
        fa = "A. "
    elif final_ans == 1:
        fa = "B. "
    elif final_ans == 2:
        fa = "C. "
    else:
        fa = "D. "
    return final_answers
    # return "Answer: " + fa + "\n"


def show(list_result):
    final_resul = ["","","",""]
    for ind in list_result:
        score = ind / sum(list_result) * 100
        final_resul[list_result.index(ind)] = chr(65 + list_result.index(ind)) + ": " + str(round(score,4)) + "%"
    return final_resul

SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_lg')
QA_MODEL = os.environ.get('QA_MODEL', 'deepset/roberta-base-squad2')
nlp = spacy.load(SPACY_MODEL)

def reading_comprehension(text):
    question_processor = QuestionProcessor(nlp)
    passage_retriever = PassageRetrieval(nlp)
    answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)
    flag = True
    context = get_context(text)
    question_list = get_question_list(text)
    doc = [context]
    print("\n" + doc[0])

    question_num = 1
    answer_identity = ['A', 'B', 'C', 'D', 'E', 'F']

    for q in question_list:
        count = 0
        answer_list = []

        max_range = q.count("__")
        question = q.split("__")[0]
        print("\nQuestion " + str(question_num) + ": " + question)
        temp = get_question(q)

        for i in range(1, max_range + 1):
            if i == 4 or temp[i] == "(A)" or temp[i] == "(B)" or temp[i] == "(C)" or temp[i] == "(D)":
                answer_list.append(temp[i].split("(")[0].strip())
                print(answer_identity[count] + ". " + temp[i].split("(")[0].strip())
            else:
                answer_list.append(temp[i])
                print(answer_identity[count] + ". " + temp[i])
            count += 1

        question_num += 1
        passage_retriever.fit(doc)
        q_type = question_classification(question)
        if q_type == 1:
            return show(get_exception_question_answer(context, question, answer_list, question_processor, passage_retriever))
        else:
            question = question_processor.generate_question(question)
            passages = passage_retriever.most_similar(question)
            answers = answer_extractor.extract(question, passages)
            return show(get_final_answer(answer_list, answers, max_range))
        flag = False
