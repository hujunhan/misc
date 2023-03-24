def main():
    user_input = input("Enter a integer: ")
    try:  ## In normal situation, this block would be trigged
        m = float(user_input)  # transfrom from str to int
    except:  ## if user_input can't be transformed into int, this block would be trigged
        print("Invalid input")
        return  # finish program

    n = 0
    while n * n < m:
        n = n + 1
    print(n)


main()
