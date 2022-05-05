import os

import nltk
from transformers import pipeline
nlp = pipeline('fill-mask',top_k = 20)
from nltk import tokenize
from nltk.util import ngrams
from collections import Counter
from transformers import pipeline

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

def incomplete_text(inputQuestion):
    result_incomplete_text = []
    resultFinal = [0.0,0.0,0.0,0.0]
    content = inputQuestion.split('Questions:')[0]
    listAnswer = inputQuestion.split('Questions:')[1].split("\n")
    del listAnswer[0]
    print(content)
    print((listAnswer))


    for i in range (0,len(listAnswer)):
        listContent = tokenize.sent_tokenize(content)
        input = ""
        indexQuestion = str(i+1)+".-------"
        flag = True
        for text in listContent:
            if text.find('.-------') != -1:
                if flag == False:
                    break
                else:
                    flag = False
            input += text
        question = input + "__" + listAnswer[i]
        question = question.replace(indexQuestion, '........')




        a = question.split('__')
        del a[1]
        data = ''
        for i in a:
            data += i +'___'
        print(data)
        # a = question.split('__')
        a[4] = a[4].replace(' \n', '')
        a[4] = a[4].replace('\n', '')
        a[4] = a[4].split(' ')[0]
        arr = question.split()
        # print(question)
        for x in arr:
            if x.find('.....') != -1:
            # if x.find('-----') != -1:
                a[0] = a[0].replace(x, '<mask>')
                break
        # print(a[0])
        arr = nlp(a[0])
        flag = False
        pos = 0
        scr_max = 0
        resultMasked = [0,0,0,0]
        result = ""
        # print(arr)
        for x in arr:
            score = x.__getitem__('score')
            x = x.__getitem__('token_str')
            x = str(x).strip()
            if x in a:

                if score > scr_max:
                    min = score
                    result = x
                    resultMasked[a.index(x) - 1] = score
            pos += 1

        resultBigram = bigram(data)
        print(resultBigram)
        print(resultMasked)
        for viTri in range(0,4):
            resultFinal[viTri] = resultBigram[viTri]*0.1 + resultMasked[viTri] * 0.9
        result_incomplete_text.append(resultFinal)
        result = a[resultFinal.index(max(resultFinal))+1]

        print(chr(65 +resultFinal.index(max(resultFinal))),a[resultFinal.index(max(resultFinal))+1])
        print(resultFinal)
        content = content.replace(indexQuestion, result)
    return result_incomplete_text

