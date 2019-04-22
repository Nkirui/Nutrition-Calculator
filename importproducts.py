from xmlrpc import client
import csv

server = "http://localhost:8069"
database ="mydiet"
user = "nathankirui5@gmail.com"
pwd = "monkey567"
common = client.ServerProxy(f'{server}/xmlrpc/2/common')

uid = common.authenticate(database,user,pwd,{})

odooApi = client.ServerProxy(f'{server}/xmlrpc/2/object')
data = [[('categ_id.name','=','Diet Items')]]
product_count = odooApi.execute_kw(database,uid,pwd,'product.template','search_count',data)

filename = "importdata.csv"
work = csv.reader(open(filename,'r'))
category = [[('name','=','Diet Items')]]
categ_id = odooApi.execute_kw(database, uid, pwd, 'product.category', 'search',category)
try:
    for row in work:
        productname = row[0]
        calories = row[1]
        type = row[2]
        record = [[('name','=',productname)]]
        product_id = odooApi.execute_kw(database, uid, pwd, 'product.template', 'search',record)
        if product_id:
            record = {'calories': calories,'type':type.lower(), 'categ_id': categ_id[0]}
            odooApi.execute_kw(database, uid, pwd, 'product.template', 'write', [product_id,record])
            print(f"These records are updated : {str(product_id)}")
        else:
            print(f'Adding Product : {productname}')
            record = [{'name':productname,'calories':calories,'type':type.lower(),'categ_id':categ_id[0]}]
            odooApi.execute_kw(database, uid, pwd, 'product.template', 'create',record)

except:
    pass

