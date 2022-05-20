my_dict = {
    "name":"Thuy Linh",
    "age":20,
    "school":"Hust"
    }
print(my_dict)
print(my_dict['name']) # goị key trong dict
my_dict['hometown'] = 'Hai Phong'
my_dict['tuple'] = (1,2,3)
print(my_dict['tuple'])
print(my_dict);
#my_info = {'name':'Thanh Long','age':22,'school':'VMU'}
my_info =dict()
my_info['name'] = 'Thanh Long'
my_info['age'] = 22
my_info['school'] = 'VMU'
print(my_info)
print(len(my_info))
my_info.clear()
print(my_info) #return {}
'''
 dictionary (bộ từ điển) là một kiểu dữ liệu, 
 nó là một danh sách các phần tử (element), 
 mà mỗi phần tử là một cặp khóa và giá trị (Key & value)
 , nó khá giống với khái niệm Map trong Java.
'''