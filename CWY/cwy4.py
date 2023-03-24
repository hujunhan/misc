def main():
    user_input = input("Enter a integer: ")
    try:  ## In normal situation, this block would be trigged
        n = int(user_input)  # transfrom from str to int
        if n <= 0:  # deal with the corner case
            print("Invalid value ", n)
            return  # finish program
    except:  ## if user_input can't be transformed into int, this block would be trigged
        print("Invalid input")
        return  # finish program

    for d in user_input:
        print(d)


main()
