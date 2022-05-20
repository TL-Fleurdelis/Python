'''
Text Type:	str
Numeric Types:	int, float, complex // số nguyên, số thực, số phức 
Sequence Types:	list, tuple, range
Mapping Type:	dict
Set Types:	set, frozenset
Boolean Type:	bool
Binary Types:	bytes, bytearray, memoryview
None Type:	NoneType
'''

a = 'linh' #string
b = 20  #number
c = 'hust'  #string
#ktra kiểu dữ liệu
print(type(a))
print(type(b))
print(type(c))

print (a,b,c)

#ép kiểu
print(float(b))
print(int(b))
print(type(str(b)))

#another way 
a,b,c = 'Linh',22,'Hust'
print(a,b,c)

import fractions #Phân số

print(fractions.Fraction(4.5)) # chuyển sang kiểu phân số
print(fractions.Fraction(4,5)) # khai báo tử số mẫu số
print(fractions.Fraction('0.2')) # khai báo qua string

name = 'Truong Thanh Long'
ho = name[:7]
print(" Họ:",ho) # tách chuỗi 
uppercase = ho.upper()
print(uppercase) # in hoa 
#range 