a= "This is the thing "
print(a)
number=-10
if  number >0 :
    print("positive")
elif number<0:
    print("negative")
else :
    print("zero")
try:
    number = int(input("Enter a number: "))
    print(100 / number)
except ZeroDivisionError:
    print("You can't divide by zero!")
except ValueError:
    print("That's not a valid number.")

book = {
    "title": "some title",
    "author": "name of the author",
    "year": 2003
}

# update and add
book["pages"] = 567
book["year"] = 2004

# print key-value pairs
for key in book:
    print(key, ":", book[key])
colors = {"red", "blue", "green", "yellow", "blue"}  # "blue" is the duplicate

print(colors)

from math import pi
print(pi)
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def display(self):
        print(f"{self.name} - ID: {self.student_id}")

s1 = Student("Alex", 1001)
s1.display()
