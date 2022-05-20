class Person: 
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def get_name(self):
        print("My name is",self.name)
class Student(Person): 
    def get_age(self,age):
        print("age:",age)

Long = Person ("Long",22)
print(Long.name)
Linh = Student('Linh',20)
Linh.get_name()
