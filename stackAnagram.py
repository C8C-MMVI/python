def isAnagram(str1, str2):
    # lower() converts a string to lowercase
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()

    # If lengths don't match (e.g., taco and cat (though they're palindromes)),
    # they can't be anagrams (e.g., Poll and Loc)
    if len(str1) != len(str2):
        return False

    # Stack to reverse str1
    stack = list(str1)
    reversed_str1 = "" # a variable to store the reversed stack of str1
    while stack:
        reversed_str1 += stack.pop()

    return sorted(reversed_str1) == sorted(str2) # determines whether the reversed and stagnant strings match

# User input
string1 = input("Enter String1: ")
string2 = input("Enter String2: ")

# Checks and print the result (True/False)
result = isAnagram(string1, string2)
print("The anagram word is:", "TRUE" if result else "FALSE")
