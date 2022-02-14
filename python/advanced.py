# Object Oriented


class Person:  # This syntax creates a new class called Person
    name = "Person"  # This is a class attribute.


# Note that the data and methods of a class are defined in the class block

john = Person()  # This is the syntax used to convert a class into an objects
# Converting a class into an object is called instantiation, We create an instance of the class as an object
print(john.name)  # Prints out Person
# We can access by using the dot notation : <obj_variable>.<class_variable>
# we created a person object and assigned it to a variable called john, but the value of the attribute name was not changed, it was just a default value. Constructors can receive arguments and change attributes of the object during initialization.


class Person:
    full_name = "Person"

    def __init__(self, first_name, last_name):  # This is a constructor
        self.full_name = (
            first_name + last_name
        )  # This is an instance variable, it is unique to each instance of the class


john_doe = Person("John", "Doe")
john_doe.full_name = (
    "Jane"  # Pass the first and last name as arguments to the constructor
)
print(john_doe.full_name)  # Prints John Doe

# Notice that the first argument in the constructor was self, this is not an argument that we pass onto the constructor, it refers to the object that has called the method, so if you wanted to access another attribute of the object you can use the self.<variable_name>
class Person:  # Create a new Class Person

    name = "Person"  # Default Attributes
    salutation = "Hello "

    def __init__(
        self, name
    ):  # Note that name is both a parameter and a class attribute
        self.name = name  # self.name refers to the class attribute and the other one refers to the parameter

    def greet(self):  # Create another class method that returns a greeting
        return (
            self.salutation + self.name
        )  # self is the object on which the method is called


john = Person("John Doe")
print(john.greet())  # Prints Hello John Doe
jane = Person("Jane Doe")
print(jane.greet())  # Prints Hello Jane Doe


# Inheritance is a way to create new classes from existing classes.The new class is called a subclass while the existing class is called a superclass. The subclass can also override attributes and methods from a superclass
class LivingThing:
    def breathe(self):
        print("I am alive")


# Multi-Level Inheritance


class Plant(LivingThing):  # We are inheriting from LivingThing
    def speak(self):
        print("I am a plant")


class Animal(LivingThing):  # We specify the parent class in parenthesis
    def move(self):
        print("I am moving")


class Dog(Animal):
    def speak(self):
        print("Woof?")

    def move(self):
        print("I am moving and fast")


my_doggo = Dog()
my_doggo.breathe()  # I am alive
my_doggo.move()  # I am moving
my_doggo.speak()  # Woof?


# Multiple inheritance
class A:
    def print_a(self):
        print("A")


class B:
    def print_b(self):
        print("B")


class AB(A, B):  # This class inherits from both A and B
    def print_ab(self):
        print("AB")


ab = AB()
ab.print_a()  # A
ab.print_b()  # B
ab.print_ab()  # AB
# Each Python object has a method resolution order ( MRO ) which is a list of classes that are used to resolve the method. The MRO is used to determine which class to call when a method is called. Let's say that each of the inherited classes has the same function, to identify which method is called we use the MRO.
# print(ab.mro())
# [<class '__main__.AB'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]
# The MRO is [AB, A, B, object] so the AB class is checked first then the A class and then the B class.

# Mixins
# When developing applications you might come across common functionality that is shared between a number of classes, in Python each feature can be built into different classes and then combined together to create a new class with the functionality required.


class RunnableMixin:
    def run(self):
        print("Can Run")


class WalkableMixin:
    def walk(self):
        print("Can Walk")


class TalkingMixin:
    def talk(self):
        print("Can Talk")


class Animal(RunnableMixin, WalkableMixin):
    pass


class Human(RunnableMixin, WalkableMixin, TalkingMixin):
    pass


# Each of the feature classes is called a Mixin.
# Encapsulation is the process of wrapping the data and code together to prevent data from being accessed by other parts of the program. This is done so that we don't manually change the attributes of the object, which could cause unexpected results.
class Person:
    name = "Person"

    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, my name is " + self.name)


john = Person("John")
john.name = "Jane"
john.greet()  # Hello, my name is Jane

# Here we manually changed the value of an attribute and it caused the function to produce an unexpected result, Python does not enforce very strict rules to prevent accidental changes like these from happening, but there are standards that we can follow.

# In Python Classes there are protected members and private members, Protected members can only be accessed by the class itself or its subclasses.

# Protected members are prefixed with an underscore (_).
class Person:
    _name = "Person"  # This is a protected member

    def __init__(self, name):
        self._name = name

    def greet(self):
        print("Hello, my name is " + self._name)


john = Person("John")
john.name = (
    "Jane"  # Creates a new attribute but does not edit the existing _name attribute
)
john.greet()  # Hello, my name is John

# Protected members are only a convention, and they are not enforced by Python. You can directly change the _name value, Usually, this is not a good idea.

# Python also has a concept of private members, which are members that can only be accessed by the class itself, Even base classes cannot access these members.

# Private members are prefixed with two underscores (__).
class Person:
    __name = "Person"  # This is a private member ( Prefixed by double underscores)

    def __init__(self, name):
        self.__name = name

    def greet(self):
        print("Hello, my name is " + self.__name)


john = Person("John")
john.__name = (
    "Jane"  # Creates a new attribute but does not edit the existing __name attribute
)
john.greet()  # Hello, my name is John

# Private members are also by convention only since these members can be accessed in the following format: object._<class_name><private_member_name> or in our case john._Person__name

# Python does not do any type of enforcement on private or protected members, but it is a convention to follow when designing classes.

# Abstract Classes
# An Abstract class is a class that contains blueprints for other classes to inherit from. An Abstract class does not contain any implementation but it defines a common interface for its subclasses.

# operator overlaoding
# Python Operators like +, - can be overloaded to perform different operations based on what object is being operated on
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):  # Overloading the `+` operator
        return Point(self.x + other.x, self.y + other.y)

    # self is the object on the lhs and other is the object on the rhs

    def __sub__(self, other):  # Overloading the `-` operator
        return Point(self.x - other.x, self.y - other.y)

    # This is called when the object is printed or converted to a string
    def __str__(self):  # Overloading the `str` operator
        return f"({self.x}, {self.y})"


point_a = Point(1, 2)
point_b = Point(3, 4)
print(point_a + point_b)  # Output: (4, 6)
print(point_a - point_b)  # Output: (-2, -2)
# when the overrode the + and - operators we return a new object instead of editing the original object.
