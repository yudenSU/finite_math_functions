import math

# finds all units of a number system ℤn
# returns a list of units
def find_units(num):
    counter = 0
    answers = []
    while counter < num: 
        if math.gcd(counter, num) == 1:
            answers.append(counter) 
        counter += 1
    
    print(answers)
    return answers

# given two integers, returns a list of the format
# [gcd, x, y] where x and y are the values ax + ny = GCD 
# in Bezout's Identity
# if visualise is set to true, it will print a table in terminal
# showing steps
def extended_euclid_gcd(a, b, visualise = False):

    x_right = 0
    x_left = 1
    y_right = 1
    y_left = 0
    remainder_right = b
    remainder_left = a
    visualise_table = []

    if visualise:
        visualise_table.append(["quotient","remainder","Xi","Yi",])
        visualise_table.append(["","","","",])

    while remainder_right != 0:            
        quotient = remainder_left//remainder_right 
        
        remainder_left, remainder_right = remainder_right, remainder_left - quotient*remainder_right

        x_left, x_right = x_right, x_left - quotient*x_right

        y_left, y_right = y_right, y_left - quotient*y_right

        if visualise:
            row = [str(quotient), str(remainder_right), str(x_right), str(y_right)]
            visualise_table.append(row)

    if visualise:
        for row in visualise_table:
            print("{: >10} {: >10} {: >10} {: >10}".format(*row))
    return [remainder_left, x_left, y_left]

# finds all inverses of a number system ℤn
# [gcd, x, y] where x and y are the values ax + ny = GCD 
# in Bezout's Identity
# if visualise is set to true, it will print all inverses in a sentence
def find_all_inverses_in_num_system_Zn(num, visualise = False):
    units = find_units(num)
    ans = []
    for i in units:
        x = extended_euclid_gcd(i, num, False)[1]
        x = x % num
        ans.append(x)
        if visualise:
            print(f"The inverse of {i} in ℤ{num} is {x}")
    return ans

# finds the inverse of a int number_to_check in the ℤnum number system
# if visualise is set to true, it will print the inverse in a sentence

def find_inverses_in_num_system_Zn(num_to_check,num, visualise = False):
    if math.gcd(num_to_check,num) != 1:
        print("this number dows not have an inverse in ℤ{num}")

    x = extended_euclid_gcd(num_to_check, num, False)[1]
    x = x % num
    if visualise:
        print(f"The inverse of {num_to_check} in ℤ{num} is {x}")
    return x

    
if __name__ =="__main__":
    print(extended_euclid_gcd(234, 856, visualise = True))