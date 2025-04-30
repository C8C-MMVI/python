# Python program to find the factorial of a number provided by the user.

# change the value for a different result
num = input("Enter a number: ")

# To take input from the user
#num = int(input("Enter a number: "))

factorial = 1

# check if the number is negative, positive or zero
if int(num) < 0:
   print("Sorry, factorial does not exist for negative numbers")
elif int(num) == 0:
   print("The factorial of 0 is 1")
else:
   for i in range(1, int(num) + 1):
       factorial = factorial*i
   print("The factorial of",num,"is",factorial)
