def main():
    sum=0
    user_input=input('Type number you want to sum up, split with space e.g.\n1 3 25 4.1 \nThen type enter. Invalid input would be ingored\nNow type your input:')
    data=user_input.split(' ')
    for d in data:
        try:
            num=float(d)
            sum+=num
        except:
            continue
    print('The sum of your input is ',sum)
main()