def main():
    user_input = input(
        "Type a number, program would show you prime number that smaller than the number you type in: "
    )
    try:  ## In normal situation, this block would be trigged
        n = int(user_input)  # transfrom from str to int
        if n <= 2:  # deal with the corner case
            print("No prime number under ", n)
            return  # finish program
    except:  ## if user_input can't be transformed into int, this block would be trigged
        print("Invalid input")
        return  # finish program

    count = 0
    for i in range(2, n):  # iterate every number from 2 to n-1
        is_prime = True  # default assume the number is a prime
        for k in range(2, i):  # the definition of a prime: can't be get from axb
            if i % k == 0:  # if i/k=x.....0
                is_prime = False  # then the number i is not a prime
        if is_prime:
            print(
                i, end=" "
            )  # don't make new line everytime, so the end is a space ' '
            count += 1
            if count == 8:
                count = 0
                print()
    print()


main()
