import pythainlp
import pythainlp.corpus
import pythainlp.util
# import pythainlp.thai_characters


# import stopwords
from pythainlp import sent_tokenize, word_tokenize, thai_characters
from pythainlp.corpus import remove, get_corpus_path, get_corpus
from pythainlp.corpus.common import thai_stopwords
from pylexto import LexTo
from pythainlp.tokenize import etcc
from pythainlp.tag import pos_tag
from pythainlp.util import collate




text = "ร้านนี้บริการลูกค้าดีจัง"
text2 =  "การบริการที่ดี ควรบริการมาจากใจ"

text_cutting = word_tokenize(text, engine = "deepcut")
text2_cutting = word_tokenize(text2, engine = "deepcut")
# text_collate = collate(text_cutting)
print("deepcut  :", text_cutting) #Engine ที่เหมาะกับงานเราที่สุด










# text_tag_list = pos_tag(text_collate)
# print(text_tag_list)














# ส่วนการหา part of speech แะละเลือกเอาเฉพาะ verb มาใช้
# text_pos = []
# pos_vact = []
# pos = ""

# for itr in range(len(text_tag_list)):
#     text_pos.append([text_tag_list[itr][0],text_tag_list[itr][1]])

         
#     if text_pos[itr][1] == None:
#         print("Word : "+text_pos[itr][0])
#         pos = input()
#         print("POS : "+pos)
#         text_pos[itr][1] = pos
#     if text_pos[itr][1] == 'VACT':
#         pos_vact.append(text_pos[itr][0])
    

# print(pos_vact)
    


# print(text_pos)



# print(vact)

# print(collate(text_tag_list))
# print("Roman    :",romanization(text_cutting,engine='royin'
# 
# ))

# from pythainlp.number import *
# from hunspell import Hunspell
# from pythainlp.romanization import romanization


# h = Hunspell()
# print("Hunspell : "+str(h.suggest('ไทย'))) #Spell Checking
# h.suggest('run')

# print(pythainlp.thai_consonants)
# print(pythainlp.thai_characters)

# ลองเทสตัวทำ POS tag ทั้งหมด
print(text)
print("pos_tag  :",pos_tag(text_cutting,engine='old'))
# text_tag_list = pos_tag(text_collate,engine='old')
# text_tag_list = pos_tag(text_collate,engine='perceptron', corpus='pud')
# print(text_tag_list)
print("\n\nPerceptron + PUD : "+str(pos_tag(text_cutting,engine='perceptron', corpus='pud'))) # << ตัวนี้น่าจะตอบโจทย์มากที่สุด
print("\n\nPerceptron + orchid_ud : "+str(pos_tag(text_cutting,engine='perceptron', corpus='orchid_ud')))
print("\n\nPerceptron + orchid : "+str(pos_tag(text_cutting,engine='perceptron', corpus='orchid')))

print("\n\nunigram + PUD : "+str(pos_tag(text_cutting,engine='unigram', corpus='pud')))
# print("\n\nunigram + orchid_ud : "+str(pos_tag(text_cutting,engine='unigram', corpus='orchid_ud')))
print("\n\nunigram + orchid : "+str(pos_tag(text_cutting,engine='unigram', corpus='orchid')))

print("\n\nartagger + PUD : "+str(pos_tag(text_cutting,engine='artagger', corpus='pud')))
# print("\n\nartagger + orchid_ud : "+str(pos_tag(text_cutting,engine='artagger', corpus='orchid_ud')))
print("\n\nartagger + orchid : "+str(pos_tag(text_cutting,engine='artagger', corpus='orchid')))

print("\n\n"+text2)

print("\n\nPerceptron + PUD : "+str(pos_tag(text2_cutting,engine='perceptron', corpus='pud'))) # << ตัวนี้น่าจะตอบโจทย์มากที่สุด
print("\n\nPerceptron + orchid_ud : "+str(pos_tag(text2_cutting,engine='perceptron', corpus='orchid_ud')))
print("\n\nPerceptron + orchid : "+str(pos_tag(text2_cutting,engine='perceptron', corpus='orchid')))

print("\n\nunigram + PUD : "+str(pos_tag(text2_cutting,engine='unigram', corpus='pud')))
# print("\n\nunigram + orchid_ud : "+str(pos_tag(text_cutting,engine='unigram', corpus='orchid_ud')))
print("\n\nunigram + orchid : "+str(pos_tag(text2_cutting,engine='unigram', corpus='orchid')))

print("\n\nartagger + PUD : "+str(pos_tag(text2_cutting,engine='artagger', corpus='pud')))
# print("\n\nartagger + orchid_ud : "+str(pos_tag(text_cutting,engine='artagger', corpus='orchid_ud')))
print("\n\nartagger + orchid : "+str(pos_tag(text2_cutting,engine='artagger', corpus='orchid')))

































# lexto = LexTo()

# print("newmm    :", word_tokenize(text))  # default engine is "newmm"
# print("longest  :", word_tokenize(text, engine="longest"))
# print("multi_cut:", word_tokenize(text, engine="multi_cut"))
# print("deepcut  :", word_tokenize(text, engine="deepcut"))
# print("ulmfit   :", word_tokenize(text, engine="ulmfit"))
# print("etcc     :", word_tokenize(text, engine="etcc"))


# text = u"แมวกินปลาแมวมันชอบนอนนอนกลางวันนอนแล้วนอนอีกเป็นสัตว์ที่ขี้เกียจจริงๆเลยแมวแต่แมวมันเข้ากับคนได้ดีฉันชอบแมว"
# words, types = lexto.tokenize(text)
# print('|'.join(words))
# print(types)


