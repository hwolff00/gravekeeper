def fizz_buzz(limit):
    for i in range(1, limit+1):
        if i % 3 == 0:
            print('fizz')
        if i % 5 == 0:
            print('buzz')
        if i % 3 and i % 5:
            print(i)

def main():
    fizz_buzz(10)

if __name__ == "__main__":
   main()
