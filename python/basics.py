print("Hello")
num = 2  # snake_case
print(num * 2)

# Implicit type conversions are done automatically by Python
num_int = 1  # int
num_float = 2.1  # float
print(num_int + num_float, type(num_int + num_float))  # float
# To quickly find out the class of an object we can use the built-in type function

print(type(1))  # Prints <class 'int'>
print(type("123"))  # Prints <class 'str'>
print(type([1]))  # Prints <class 'list'>
print(type({"key": "val"}))  # Prints <class 'dict'>

# Explicit type conversions are done manually in code , int(),float(),string(),bool()
int_convert = int(num_float)
print(num_int + int_convert)

str_a = "100"
print(int(str_a), str_a)
str_b = "John"
# print(int(str_b)) Raises Exception since john cannot be converted to int

str_b = "hello world, This is A test"
print(str_b.capitalize())  # Capitalizes the first character
print(
    str_b.count("a")
)  # Counts the number of times the character "a" occurs in the string
print(
    str_b.endswith("test")
)  # Returns True if the string ends with the substring "test"
print(
    str_b.find("gem")
)  # Returns the index of the first occurrence of the substring "gem" and -1 if it does not exist.
print(
    str_b.index("test")
)  # Returns the index of the first occurrence of the substring "test" and raises an exception if it does not exist.
print(str_b.upper())  # Returns a copy of the string in uppercase
print(str_b.title())  # Returns a copy of the string in title case
print(
    str_b.swapcase()
)  # Returns a copy of the string in swapcase swapcase() method returns a string where all the upper case letters are lower case and vice versa.

# functions available is to type dir() and see what functions are available.
print(dir(str_b))

# F strings are a relatively new addition to Python ( since 3.6 ), they are a way to format strings.

print(f"hello {str_b}")  # prints hello john
print(f"{str_b.upper()}")  # prints JOHN
print(f"{1+2-3}")  # prints 0
# F strings make string formatting easier and more readable.
# Note that all F strings start with f right before the start of the quotation marks
# Expressions have to be surrounded with a curly brace {} to be replaced by their value

# Functions can not return a value as well, In those cases None is the value returned by the function.
def fun(name):
    salutation = name + " Helooo"
    return salutation


print(fun("Priya"))


def fun_param(name, greeting=" Hellooo"):
    salutation = name + greeting
    return salutation


# we can also pass parameters to the function by name, that way we can change the order of the parameters
print(fun_param(name="John"))
print(fun_param("John", " Good Afternoon"))
print(fun_param("Jane"))

#  create functions without any statements in them use the pass statement
def fun_pass():
    pass


fun_pass()  # Returns None

# conditionals
print(1 > 2)  # prints False
print(2 * 2 == 4)  # prints True
print(True and False)  # prints False
print(not False)  # prints True
print((2 > 1) and (1 > 2))  # prints False ( Evaluates to True and False )
(2 > 1) and print("2 is greater than 1")  # prints 2 is greater than 1
(1 > 2) and print("1 is greater than 2")  # prints nothing

if num > 2:
    print("Greater than 2")
elif num == 2:
    print("Equals")
else:
    print("Less than 2")

# lists are mutable
lst = [1, 2, "priya", True]
print(len(lst), lst[2])
#  Lists can also be negatively indexed i.e -1 index is the last element.
# slicing
print(lst[0:2])  # prints [1, 2]
print(lst[:2])
# prints [1, 2] not specifying a start index will start from the beginning
print(lst[2:])  # prints [3, 4, 5] not specifying an end index will end at the end
print(lst[-1])  # prints 5
print(lst[-3:])  # prints [3, 4, 5] ( the last three items with the start included)

list_with_numbers = [1, 2, 3, 4, 5]
list_with_numbers.append(6)  # adds 6 to the end of the list
list_with_numbers.insert(2, 7)  # inserts 7 at index 2
list_with_numbers.remove(3)
# removes the first 3 from the list ** Based on the value not the index
list_with_numbers.pop()  # removes the last item from the list
list_with_numbers.pop(0)  # removes the first item from the list
list_with_numbers.reverse()  # reverses the order of the list, note that this function does not return anything
list_with_numbers.sort()  # sorts the list , note that this function does not return anything
list_with_numbers.sort(reverse=True)  # sorts the list in reverse order
print(list_with_numbers)

split_arr = str_b.split(" ")
print(split_arr)
join_arr = (" ").join(split_arr)
print(join_arr)

# call the function with every item in the list.
some_names = ["John", "Jane", "Mary"]


def say_hello(name):
    return "Hello " + name


print(list(map(say_hello, some_names)))

basket = ["apple", "orange", "apple", "pear", "orange", "banana"]
for f in sorted(set(basket)):
    print(f)
for f in basket:
    print(f)

for i in reversed(range(1, 10, 2)):
    print(i)
# Python comes with an immutable version of lists called tuple. Tuples do not support changes once initialized.

# A dictionary in Python is simply a collection of key-value pairs.
contact_details = {
    "Mary": {
        "address": "123 Main Street",
        "state": "NY",
        "phone": ["1234567890", "9876543210"],
    },
    "John": {
        "address": "149 Main Street",
        "state": "IN",
    },
}
print(contact_details.keys())  # prints ["John", "Jane"]
print(contact_details.values())  # prints ["1234567890", "0987654321"]
print(contact_details.get("John"))  # prints 0987654321
print(contact_details.get("Jane", "Not found"))  # prints Not found
print(contact_details["John"])

print(sorted(list(contact_details)))

for k, v in contact_details.items():
    print(k, v)

del contact_details["John"]
print(contact_details)

print("John" in contact_details, "Mary" not in contact_details)

print(dict([("sape", 4139), ("guido", 4127), ("jack", 4098)]))

for i, v in enumerate(["tic", "tac", "toe"]):
    print(i, v)

questions = ["name", "quest", "favorite color"]
answers = ["lancelot", "the holy grail", "blue"]
for q, a in zip(questions, answers):
    print("What is your {0}?  It is {1}.".format(q, a))


# Iteration
i = 10
while True:
    i = i - 1
    if i == 5:
        continue
    if i == 0:
        break
    print(i)

# Python has a concept of iterators and generators. Iterators are objects that are used to iterate over a sequence. Generators are functions that return iterators.
print(sum(i * i for i in range(10)))
# Iterator

iter_list = iter(["Geeks", "For", "Geeks"])
print(next(iter_list))
print(next(iter_list))
print(next(iter_list))

# Generator
def sq_numbers(n):
    for i in range(1, n + 1):
        yield i * i


a = sq_numbers(3)

for n in sq_numbers(3):
    print(n)

print("The square of numbers 1,2,3 are : ")
print(next(a))
print(next(a))
print(next(a))

# Exceptions and Handling them
# Exceptions in Python can also be raised by the programmer, this is done using the raise statement. This is useful when we want to force the execution to move to the except block.

try:
    numerator = 10
    denominator = 0  # Change this to see different execution flows
    if denominator > 100:
        raise ValueError("Denominator cannot be greater than 100")
    print("Answer is", numerator / denominator)
except ZeroDivisionError:
    print("You cannot divide by zero")
except ValueError:
    print("Value Error! Denominator Must be < 100")  # Catches the Value Error
except:
    print("Something Happened")
finally:
    print("All operations have been completed")


# Recursion
for i in range(10, 0, -1):  # Only counts till 1
    print(i)


def countdown(number):
    if number < 0:
        return
    print(number)
    countdown(number - 1)


countdown(10)

