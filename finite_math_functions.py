import math
from re import A
import numpy as np
from numpy import append
from sympy import euler, false, prime, true
from base64 import encode
from sympy.solvers import solve
from sympy import Symbol, false, true
from numpy.polynomial import polynomial as P

# finds all units of a number system ℤn
# returns a list of units
def find_units(num):
    counter = 0
    answers = []
    while counter < num: 
        if math.gcd(counter, num) == 1:
            answers.append(counter) 
        counter += 1
    
    #print(answers)
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
        visualise_table.append(["",a,"1","0",])
        visualise_table.append(["",b,"0","1",])

    while remainder_right != 0:            
        quotient = remainder_left//remainder_right 
        
        remainder_left, remainder_right = remainder_right, remainder_left - quotient*remainder_right

        x_left, x_right = x_right, x_left - quotient*x_right

        y_left, y_right = y_right, y_left - quotient*y_right

        if visualise:
            row = [str(quotient), str(remainder_right), str(x_right), str(y_right)]
            visualise_table.append(row)

    if visualise:
        print("\n")
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

# finds the totient of a given number
def euler_totient(num, visualise = False):
    ans = len(find_units(num))
    if visualise:
        print(ans)
    return ans
# calculates the order of a integer modulo number system
def order_of_mod(mod, visualise = False):
    a = []
    for number in range (1,mod):
        for counter in range (1,mod):
            if ((number**counter) % mod) == 1:
                a.append(counter)
                break
    if visualise:
        print(sorted(set(a)))
    return sorted(set(a))

# calculates the order of a integer modulo number system, however the 
# answer is left unsorted
def order_of_mod_unsorted(mod, visualise = False):
    a = []
    for number in range (1,mod):
        for counter in range (1,mod):
            if ((number**counter) % mod) == 1:
                a.append(counter)
                break
    if visualise:
        print(a)
    return a


# finds all the pseudo primes given a base and exponent
def pseudo_prime(base,exponent):
    if is_prime(exponent):
        return false
    num = base**(exponent-1)
    if ((num % exponent) == 1):
        return True
    else:
        return False

def prime_factors(num):
    prime_factors = []
    counter = 2
    while num != 1:
        if not is_prime(counter):
            counter += 1
            continue
        if (num % counter) == 0:
            prime_factors.append(counter)
            num = num/counter
            counter = 2
        if counter >= num:
            break
        counter += 1

    return prime_factors

# rsa breaker for small primes
def rsa_breaker(known_key,pq):
    prime_factor_list = prime_factors(pq)
    if len(prime_factor_list) != 2:
        return False

    # calculate order
    order = (prime_factor_list[0] -1 )*(prime_factor_list[1] - 1)

    key = extended_euclid_gcd(known_key,order)[1]
    
    if (key < 0):
        key = order + key
    

    return key

# decypt a rsa message if the primes are small enough and 1 key
def message_rsa_decrypt(message_list, known_key, pq):
    new_key = rsa_breaker(known_key,pq)
    new_message = []
    for num in message_list:
        new_num = (num**new_key) % pq
        new_message.append(new_num)
    
    print(new_message)
    return new_message

# def topic_6_question_8(message_list, known_key, pq):
#     message = message_rsa_decrypt(message_list, known_key, pq)
#     new_message_list = []
#     for num in message:
#         character = chr(num+64)
#         new_message_list.append(character)
#         print(character, end ="")
           
#     return new_message_list

# small function to help calculare different sums of vectors for 7 4 encoding
def hamming_7_4_encode_assist(byte_list):

    return [   (byte_list[0]+byte_list[1]+byte_list[3])%2, 
        (byte_list[0]+byte_list[2]+byte_list[3])%2,
        (byte_list[0]),
        (byte_list[1]+byte_list[2]+byte_list[3])%2,
        (byte_list[1]),
        (byte_list[2]),
        (byte_list[3]),
    ]

# decode a standard 7 4 hamming encoding 
def hamming_7_4_decode(encoded_array):
    hamming_matrix = np.array([
                                [1, 0, 1, 0, 1, 0, 1],
                                [0, 1, 1, 0, 0, 1, 1],
                                [0, 0, 0, 1, 1, 1, 1],])
    coded_list = np.asarray(encoded_array)
    ans = np.dot(hamming_matrix,coded_list)
    counter = 0
    for counter in range(len(ans)):
        ans[counter] = ans[counter] % 2
    print (ans)
    return ans


# returns a list of the primitive elements of an integer modulo system
def primitive_element(mod):
    answers = []
    totient = euler_totient(mod)
    order = order_of_mod_unsorted(mod)
    for counter in range(1, len(order)):
        if order[counter] == totient:
            answers.append(counter)

    # if show_power_list:
    if answers == []:
        return []
    return answers

# checking if a number is prime method, definitely not good for larger numbers
def is_prime(n):
  for i in range(2,n):
    if (n % i) == 0:
      return False
  return True

# shows working in terminal for the euclidean algorthim on two integers
def ECD_workout(a, b):

    x_right = 0
    x_left = 1
    y_right = 1
    y_left = 0
    remainder_right = b
    remainder_left = a
    visualise_table = []

    print("\n")
    while remainder_right != 0:
        start_remainder_left = remainder_left
        start_remainder_right = remainder_right
                    
        quotient = remainder_left//remainder_right 
        
        remainder_left, remainder_right = remainder_right, remainder_left - quotient*remainder_right

        x_left, x_right = x_right, x_left - quotient*x_right

        y_left, y_right = y_right, y_left - quotient*y_right

        print(f"{start_remainder_left} = {quotient} X {start_remainder_right} + {remainder_right}")
    print(f"\nThe GCD is {start_remainder_right}.")
    
    return [remainder_left, x_left, y_left]


# calculates the number of exact solutions for a congruence equation
# TODO this was made for a question I was answering and may need to be revised.
def number_of_exact_solutions_congruence(first_num_from_left, number_in_middle, modulus, visualise = False):
    ans = math.gcd(first_num_from_left, modulus)
    # print(ans)
    if ans == 1:
        if visualise:
            print(ans)        
        return 1
    if (number_in_middle == 0):
        if visualise:
            print(ans)
        return ans
    if (number_in_middle % ans) == 0:
        if visualise:
            print(ans)
            return ans

    if (ans % number_in_middle) == 0:
        if visualise:
            print(ans)
            return ans
    if visualise:
        print("there is no solution")    
    return 0



def Calculate_inverse_in_mod(a,modulus, visualise = False):
    for num in range (0, (modulus-1)):
        if ((a*num) % modulus) == 1:
            if visualise:
                print(num)
            return num
    if visualise:
        print("no inverse")
    return False


def calculate_set_of_all_orders(base):
    list = order_of_mod(base)
    list_string = str(list)
    list_string = list_string.replace("[","set(")
    list_string = list_string.replace("]",")")

    print(list_string)

def Calculate_number_of_primitive_elements(base):
    a = len(primitive_element(base))
    print(a)
    return a

def smallest_RSA_key(modulus):
    """An RSA cryptosystem uses 33 as its modulus. 
    What is the smallest composite number k for which x↦xk is
     a valid encryption function in this cryptosystem?"""
    totient = euler_totient(modulus)

    for number in range (1, totient):
        if is_prime(number):
            continue
        if math.gcd(number, totient) == 1:
            print(number)
            return number

def DFS_calculate_secret_key_brute(modulus, primitive_element, encrypted_num, other_encrypted_num):
    for num in range (0, (modulus-1)):
        if ((primitive_element**num) % modulus) == encrypted_num:
            ans = (other_encrypted_num**num) % modulus
            print(ans)
            return(ans)


# some helpful links I use
#ax +by = c
#https://www.math.uwaterloo.ca/~snburris/htdocs/linear.html

# polynomial modulo calc
#https://www.wolframalpha.com/input?i=PolynomialMod%5B6x%5E3%2B2x%5E2%2B2x%2C+5x%5E2%2B3x%2B1%5D

#Polynomial factorization in a finite field
# https://planetcalc.com/8372/

#fraction to decimal
#https://coolconversion.com/math/fraction-to-decimal/
# convert number base with fract
#     #http://www.knowledgedoor.com/2/calculators/convert_a_number_with_a_mixed_fractional_part.html


# the list of all possible orders is: factors of totient(modulus)

if __name__ =="__main__":
    # a = 846
    # b = 402

    # ECD_workout(a,b)

    print(prime_factors(99))

