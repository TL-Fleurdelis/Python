x = 9 # this is Global
#  Từ khóa global cho phép bạn chỉnh sửa biến bên ngoài phạm vi hiện tại.
#  Nó được sử dụng để tạo biến global và thực hiện thay đổi cho biến trong bối cảnh cục bộ.
def MyFunction():
    global x 
    x = x + 10
    print(x)
MyFunction()
print(x)