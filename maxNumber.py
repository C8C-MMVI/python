print("Number 1: Finding the max number in a list")
numList = [1,2,3,4,5,6,7]

max_list = max(numList)   

print(max_list)

"""
Algorithm:
1. Start Program
2. Declare a list variable numList containing numbers
3. Declare another variable max_list that determines the maximum number
in the list
4. Display the maximum number
5. Program ends
"""

print ("Number 2: Adding the digits in a number")
num = input("Enter a number: ")

if (int(num) <= 9999):
    thousand = int(num) / 1000 % 10
    hundred = int(num) / 100 % 10
    ten = int(num) / 10 % 10
    one = int(num) % 10
    sum = int(thousand) + int(hundred) + int(ten) + int(one)
    print("Sum of all digits:", str(sum))
else:
    print("Too much digits. Try again")

"""
Algorithm:
1. Start Program
2. Let the user input a number and store it to variable num
4. If the variable num is less than or equal to 9999, declare variables
thousand, hundred, ten, and one that extracts the user's number to
individual data
5. Program continues by adding each individual variables and stores it to
variable sum
5. Display the sum
6. Unless the user's input exceeds the condition,
the program displays the prompt "Too much digits. Try again"
7. Program ends

"""

"""
print("Number 3: Finding the average of a list")
def find_average(numbers):
    if not numbers:
        return "List is empty, cannot compute average."
    return sum(numbers) / len(numbers)

numbers = [5, 10, 15, 20, 25]
average = find_average(numbers)
print(f"The average is: {average}")
"""

print ("Number 4: Finding the GCF of two numbers")
def find_gcf(num1, num2):
    gcf = 0
    for i in range(1, min(num1, num2) + 1):
        if num1 % i == 0 and num2 % i == 0:
            gcf = i
    return gcf

# Taking input from the user
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

# Finding and displaying the GCF
gcf = find_gcf(num1, num2)
print(f"The GCF between {num1} and {num2} is {gcf}")


