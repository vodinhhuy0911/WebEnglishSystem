import os

import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from transformers import pipeline
nlp = pipeline('fill-mask',top_k = 20)
from tensorflow.keras.models import load_model
import numpy as np
import pickle

def getDataBigram():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'traningUnigram_Ver2.txt')  # full path to text.
    data_file = open(file_path, 'r',encoding="utf-8")
    result = data_file.read()
    # fr = open("traningUnigram_Ver2.txt", "r", encoding="utf-8")
    # result = fr.read()
    resultUni = {}
    temp = result.replace("Counter({('", "'")
    temp = temp.replace("})", "")
    temp = temp.replace("(", "")
    temp = temp.replace(",)", "")
    temp = temp.split(', ')
    for i in temp:
        temp1 = i.split(": ")
        temp2 = str(temp1[0]).replace("'", "")
        resultUni[temp2] = int(temp1[1])
    # fr.close()
    #########################

    module_dir2 = os.path.dirname(__file__)
    file_path2 = os.path.join(module_dir2, 'traningBigram_Ver2.txt')  # full path to text.
    data_file2 = open(file_path2, 'r', encoding="utf-8")

    result1 = data_file2.read()
    resultBi = {}
    temp = result1.replace("Counter({('", "'")
    temp = temp.replace("})", "")
    temp = temp.replace(")", "")
    temp = temp.split(', (')
    for i in temp:
        temp0 = "(" + i
        temp3 = temp0.split(": ")
        resultBi[str(temp3[0] + ")")] = int(temp3[1])
    # fr1.close()
    return resultUni, resultBi

def bigram(inputQuestion):
    frequenciesUnigramInContent, frequenciesBigramInContent = getDataBigram()
    frequenciesUnigramInContent = Counter(frequenciesUnigramInContent)
    frequenciesBigramInContent = Counter(frequenciesBigramInContent)
    contentQuestion = inputQuestion
    arr = contentQuestion.split('___')
    arr[4] = arr[4].replace(' \n', '')
    arr[4] = arr[4].replace('\n', '')
    arrQuestion = arr[0].split(' ')
    i = 0
    for x in arrQuestion:
        if x.find('.....') != -1:
            arrQuestion[i] = '%%%'
        i += 1
    space = ' '
    question = space.join(arrQuestion)
    arrAnswer = [question.replace('%%%', arr[1]), question.replace('%%%', arr[2]), question.replace('%%%', arr[3]),
                 question.replace('%%%', arr[4])]
    frequencies = Counter([])
    result = [1.0, 1.0, 1.0, 1.0]

    i = 0
    for answer in arrAnswer:

        token = nltk.word_tokenize(answer)
        bigrams = ngrams(token, 2)
        frequencies = Counter(bigrams)
        for x, y in frequencies.most_common():
            result[i] *= ((frequenciesBigramInContent[str(x)] + 1) / (
                    frequenciesUnigramInContent[x[1]] + sum(frequenciesUnigramInContent.values())))
        i += 1
    return  result

def MaskedLanguageModel(inputQuestion):
    question = inputQuestion
    a = question.split('___')
    a[4] = a[4].replace(' \n', '')
    a[4] = a[4].replace('\n', '')
    arr = a[0].split()
    for x in arr:
        if x.find('.....') != -1:
            a[0] = a[0].replace(x, '<mask>')
            break
    arr = nlp(a[0])
    flag = False
    pos = 0
    max = 0
    resultMasked = [0, 0, 0, 0]
    result = ""
    for x in arr:
        score = x.__getitem__('score')
        x = x.__getitem__('token_str')
        x = str(x).strip()
        if x in a:
            resultMasked[a.index(x) - 1] = score
            if score > max:
                min = score
                result = x
        pos += 1
    return resultMasked

def bigram_MaskedLanguageModel(inputQuestion):
    question = inputQuestion
    a = question.split('___')
    a[4] = a[4].replace(' \n', '')
    a[4] = a[4].replace('\n', '')
    resultBigram = bigram(inputQuestion)
    resultFinal = [0, 0, 0, 0]
    for r in range(0, 4):
        resultFinal[r] = resultBigram[r] / (sum(resultBigram))
    resultMasked = MaskedLanguageModel(inputQuestion)
    resultOutput = [0.0, 0.0, 0.0, 0.0]
    landa = 0.9
    for viTriDapAn in range(0, 4):
        resultOutput[viTriDapAn] = (resultFinal[viTriDapAn] * (1.0 - landa)) + (resultMasked[viTriDapAn] * (landa))
    for viTriDapAn in range(0, 4):
        resultOutput[viTriDapAn] = resultOutput[viTriDapAn]/ sum(resultOutput) *100

    percent = []
    for viTriDapAn in range(0,4):
        percent.append(a[viTriDapAn+1]+": " +str(round(resultOutput[viTriDapAn],4)) + "%")
    return percent

