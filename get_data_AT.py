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
            
                arr_cutting.append([i,record_item[i]['fields']['Category'],record_item[i]['id'],word_cutting,request_cutting,inv_amount,bf_vat,vat,pay_amount,withholding,percentage,[account_payable[itr]['fields']['Name'],account_payable[itr]['fields']['Payable ID']]]) #Append data to the new list

                # print(payable_data)
                 
        
        # arr_cutting.append([record_item[i]['id'],word_cutting,record_item[i]['fields']['THB Invoice Amount'],record_item[i]['fields']['Tax Withholding Amount'],payable_data])

i = 0
for i in range(len(arr_cutting)):

    if arr_cutting[i][10] != 5.0 and arr_cutting[i][10] != 3.0 and arr_cutting[i][10] != 2.0:
        print(str(i)+":")
        print(arr_cutting[i])

# print(str(len(account_payable))+" ID[0]: "+account_payable[0]['id'])
# print("arr 189: ")
# print(arr_cutting[189])
# print("record 189: ")
# print(record_item[189])
        

# print(record_item[0]['id'])



# cnx = mysql.connector.connect(user='root', password='keep1234',host='192.168.99.100:3306',database='keeplearning')

# cursor = cnx.cursor()

# query = ("SELECT IncomeTaxAssessable"
#         "FROM IncomAssessable"
#         "WHERE IncomeTaxAssessable = %s")


# cursor.execute(query)

# print(cursor)


# cursor.close()
# cnx.close()