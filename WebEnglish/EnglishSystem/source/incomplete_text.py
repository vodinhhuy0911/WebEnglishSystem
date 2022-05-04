import nltk
from transformers import pipeline
nlp = pipeline('fill-mask',top_k = 20)
from nltk import tokenize
from nltk.util import ngrams
from collections import Counter

def getDataBigram(pathUnigram, pathBigram):
    fr = open(pathUnigram, "r", encoding="utf-8")
    result = fr.read()
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
    fr.close()
    #########################

    fr1 = open(pathBigram, "r", encoding="utf-8")
    result1 = fr1.read()
    resultBi = {}
    temp = result1.replace("Counter({('", "'")
    temp = temp.replace("})", "")
    temp = temp.replace(")", "")
    temp = temp.split(', (')
    for i in temp:
        temp0 = "(" + i
        temp3 = temp0.split(": ")
        resultBi[str(temp3[0] + ")")] = int(temp3[1])
    fr1.close()
    return resultUni, resultBi

def bigram(inputQuestion,pathUnigram, pathBigram):
    frequenciesUnigramInContent, frequenciesBigramInContent = getDataBigram(pathUnigram, pathBigram)
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




for number in range(3,4):
    fr = open("../../Data/Câu hỏi/Incomplete/Đoạn/"+str(number)+".txt","r",encoding="utf-8")
    inputQuestion = fr.read()
    # print(inputQuestion)
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
            data += i +'__'
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
        max = 0
        resultMasked = [0,0,0,0]
        result = ""
        # print(arr)
        for x in arr:
            score = x.__getitem__('score')
            x = x.__getitem__('token_str')
            x = str(x).strip()
            if x in a:
                resultMasked[a.index(x)-1] = score
                if score > max:
                    min = score
                    result = x
            pos += 1
        # print(resultMasked)
        # print(a)
        try:
            content = content.replace(indexQuestion,result)
            # print("Acc:", score)
            # print(content)
            print(chr(65 + a.index((result))-1),result)
            # fw.write(chr(65 + a.index((result))-1))
        except:
            bigram()
    fr.close()
# fw.close()
