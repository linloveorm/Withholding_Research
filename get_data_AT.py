import pythainlp
import pythainlp.corpus
import pythainlp.util

import mysql.connector
# import pythainlp.thai_characters


# import stopwords
from pythainlp import sent_tokenize, word_tokenize, thai_characters
from pythainlp.corpus import remove, get_corpus_path, get_corpus
from pythainlp.corpus.common import thai_stopwords
from pylexto import LexTo
from pythainlp.tokenize import etcc
from pythainlp.tag import pos_tag
from pythainlp.util import collate



from airtable import Airtable

finance_19 = Airtable('appONgFq3YP1hnVYA','Purchase Items',api_key='keyuZ9jZifvOzDgPO')
account_payable_table = Airtable('appONgFq3YP1hnVYA','Account Payable',api_key='keyuZ9jZifvOzDgPO')

# print(finance_19.get_all(view = 'Withholding', sort = 'Purchase ID'))
page = 0
record = 0
i = 0
record_item = []
id = 0
arr_cutting = []
account_payable = []
payable_data = []

#Getting all the record of Account Payable
account_payable = account_payable_table.get_all(view = 'Grid view', sort = 'Name')


#Getting all the record of Purchase Item with withholding tax
for page in finance_19.get_iter(view = 'Withholding', sort = 'Purchase ID'):
    for record in page:
        record_item.append(record)

print(len(record_item)) #checking len of record in purchase item

main_view = finance_19.get_all(view = 'Main View', sort = 'Purchase ID') #Get all the record from main view for get the data 

#Cutting text (Short Description) and delete whitespace
for i in range(len(record_item)):
    if round(record_item[i]['fields']['Tax Withholding Amount'],2) > 0 :
        word_cutting = word_tokenize(record_item[i]['fields']['Short Description'],engine = "deepcut",keep_whitespace=False)
        request_cutting = word_tokenize(record_item[i]['fields']['Request Justification'],engine = "deepcut",keep_whitespace=False)
        #check record if record have the installment
        if 'Related Purchases' in record_item[i]['fields']:
            inv_amount = record_item[i]['fields']['THB Invoice Amount'] 
            for inv_id in range(len(main_view)):
                for rp in range(len(record_item[i]['fields']['Related Purchases'])):
                    if record_item[i]['fields']['Related Purchases'][rp] == main_view[inv_id]['id']:
                        inv_amount += main_view[inv_id]['fields']['THB Invoice Amount']
                        
                        # print("Related : "+str(i)+" : "+record_item[i]['fields']['Short Description']+" : "+str(inv_amount))
             
            bf_vat = round(inv_amount/1.07,2)
            vat = round(bf_vat*0.07,2)
            pay_amount = record_item[i]['fields']['Payment Amount']
            withholding = round(record_item[i]['fields']['Tax Withholding Amount'],2)
            # print(str(i)+" : "+str(withholding))
            percentage = round((withholding/bf_vat)*100.0,2)

            # print(len(main_view))
            #check it the record is without tax
            if percentage == 3.21 or percentage == 3.31:
                percentage = round((withholding/inv_amount)*100.0,2)

            elif percentage == 1.5:
                for inv_id in range(len(main_view)):
                    for rp in range(len(record_item[i]['fields']['Related Purchases'])):
                        if record_item[i]['fields']['Related Purchases'][rp] == main_view[inv_id]['id']:
                            # print(inv_id)
                            pay_amount += main_view[inv_id]['fields']['Payment Amount']
                            withholding += round(main_view[inv_id]['fields']['Tax Withholding Amount'],2)
                percentage = round((withholding/bf_vat)*100.0,2)

        
        else:            
            inv_amount = record_item[i]['fields']['THB Invoice Amount']
            bf_vat = round(inv_amount/1.07,2)
            vat = round(bf_vat*0.07,2)
            pay_amount = record_item[i]['fields']['Payment Amount']
            withholding = round(record_item[i]['fields']['Tax Withholding Amount'],2)
            # print(str(i)+" : "+str(withholding))
            percentage = round((withholding/bf_vat)*100.0,2)

            #check it the record is without tax
            if percentage == 3.21 or percentage == 3.31:
                percentage = round((withholding/inv_amount)*100.0,2)
            
            
            # print("non-related : "+str(i)+" : "+record_item[i]['fields']['Short Description'])


        for itr in range(len(account_payable)):
            # print(record_item[i]['fields']['Account Payable'][0])
            # print(account_payable[itr]['id'])
            if(record_item[i]['fields']['Account Payable'][0] == account_payable[itr]['id']):
                # print("Purchase: " + record_item[i]['fields']['Account Payable'][0])
                # print("Payable: "+account_payable[itr]['id'])
                # payable_data.append([account_payable[itr]['fields']['Name'],account_payable[itr]['fields']['Payable ID']])
            
                arr_cutting.append([i,record_item[i]['fields']['Category'],record_item[i]['id'],pos_tag(word_cutting, engine='unigram', corpus='pud'),pos_tag(request_cutting, engine='unigram', corpus='pud'),inv_amount,bf_vat,vat,pay_amount,withholding,percentage,[account_payable[itr]['fields']['Name'],account_payable[itr]['fields']['Payable ID']]]) #Append data to the new list

                # print(payable_data)
                 
        
        # arr_cutting.append([record_item[i]['id'],word_cutting,record_item[i]['fields']['THB Invoice Amount'],record_item[i]['fields']['Tax Withholding Amount'],payable_data])

# print(arr_cutting)

wth = []
i = 0
itr = 0
verb = []
count = 0
index_wth = 0 
keyword = []
for i in range(len(arr_cutting)):
    count = 0
    # print("percentage : "+str(arr_cutting[i][10]))
    if arr_cutting[i][10] not in wth:
        wth.append(arr_cutting[i][10])
        verb.append([])
    verb[wth.index(arr_cutting[i][10])].append([])
    sentenceIndex = len(verb[wth.index(arr_cutting[i][10])]) - 1
    # print("index : "+str(wth.index(arr_cutting[i][10])))
    # print("len : "+str(len(verb[wth.index(arr_cutting[i][10])])))
    for itr in range(len(arr_cutting[i][3])):
        
        if arr_cutting[i][3][itr][1] == 'VERB':
            
            count += 1  
            verb[wth.index(arr_cutting[i][10])][sentenceIndex].append([count,itr,arr_cutting[i][3][itr][0],arr_cutting[i][3][itr][1],arr_cutting[i][10],i])
            
        else:
            pass
       
            
            
    
# print(verb)
    

        


i = 0
itr = 0 
ite = 0
ind = 0
check = False

for i in range(len(verb)):
  
    for itr in range(len(verb[i])):
        if len(verb[i][itr]) > 1:
            for ind in range(len(verb[i][itr])):
                if ind == 0:                                 
                    for n in range(len(arr_cutting)):
                        if verb[i][itr][ind][5] == n:
                            print("full sentence: ")
                            print(arr_cutting[n][3])
                # print("ind: "+str(ind))
                print(str(ind)+":"+str(verb[i][itr][ind]))
            
                
            print("Choose the keyword number :")
            num = input()
            for ite in range(len(verb[i][itr])):
                if ite == int(num):
                    keyword.append(verb[i][itr][int(num)])
                    print("Keyword :"+str(i)) 
                    print(keyword)
                    check = True
                    break
                else:
                    if check == bool(check):
                        print("error")
                
                    

        else:
            keyword.append(verb[i][itr])
            print(keyword)


    print("Keyword "+str(i)+":")
    print(keyword)

print(keyword)





