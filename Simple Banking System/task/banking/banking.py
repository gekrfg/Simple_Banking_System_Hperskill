from random import randrange
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY AUTOINCREMENT,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0
);
''')
conn.commit()

current_number = ''
current_pin = ''
current_balance = 0

class CreditCard:
    def __init__(self):
        self.balance = 0
        account_number = str(randrange(000000000, 999999999))
        while len(account_number) != 9:
            account_number = str(randrange(000000000, 999999999))
        cn = str(f"400000{account_number}")
        self.account_number = account_number
        self.credit_card_number = luhn(cn)
        pin = str(randrange(0000, 9999))
        while len(pin) != 4:
            pin = str(randrange(0000, 9999))
        self.pin = pin
        cur.execute("insert into card(number, pin) values ({}, {})".format(int(self.credit_card_number), int(self.pin)))
        conn.commit()

    def create_card(self):
        print("\nYour card has been created")
        print("Your card number:")
        print(self.credit_card_number)
        print("Your card PIN:")
        print(self.pin)
        print("")

# functions


def menue():
    print("""1. Create an account
2. Log into account
0. Exit""")

    choice = input()

    if choice == "1":
        cc = CreditCard()
        cc.create_card()
        menue()

    elif choice == "2":
        login()
        menue()

    elif choice == "0":
        print("")
        print("Bye!")
        exit()

    else:
        print("invalid selection.\n")
        menue()


def login():
    global current_number
    global current_pin
    global current_balance
    print("Enter your card number:")
    input_cc = input()
    print("Enter your PIN:")
    input_pin = input()
    # check whether combination is in dict with all the cards/pins
    cur.execute(f'select * from card where number = {input_cc} and pin = {input_pin}')
    row = cur.fetchall()
    if row:
        print("\nYou have successfully logged in!\n")
        current_number = input_cc
        current_pin = input_pin
        current_balance = int(row[0][3])
        balance_menue()
    else:
        print("Wrong card number or PIN!")
        menue()





def balance_menue():
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")

    choice = input()
    global current_number
    global current_balance

    if choice == "1":
        print(f"\nBalance: {current_balance}\n")
        balance_menue()

    elif choice == "2":
        print("\nEnter income:")
        income = int(input())
        current_balance += income
        cur.execute(f"UPDATE card SET balance = {current_balance} WHERE number = {current_number}")
        conn.commit()
        print('Income was added!\n')
        balance_menue()

    elif choice == "3":
        print("\nTransfer")
        print("Enter card number:")
        target_number = input()
        if not is_luhn(target_number):
            print('Probably you made mistake in the card number. Please try again!\n')
            balance_menue()
        cur.execute(f'select * from card where number = {target_number}')
        row = cur.fetchall()
        if not row:
            print('Such a card does not exist.\n')
            balance_menue()
        print('Enter how much money you want to transfer:')
        trans_amount = int(input())
        if trans_amount > current_balance:
            print('Not enough money!\n')
            balance_menue()
        current_balance = current_balance - trans_amount
        target_balance = int(row[0][3])
        target_balance += trans_amount
        cur.execute(f"UPDATE card SET balance = {current_balance} WHERE number = {current_number}")
        conn.commit()
        cur.execute(f"UPDATE card SET balance = {target_balance} WHERE number = {target_number}")
        conn.commit()
        print('Success!\n')
        balance_menue()

    elif choice == "4":
        cur.execute(f"delete from card WHERE number = {current_number}")
        conn.commit()
        print("\nThe account has been closed!\n")
        menue()


    elif choice == "5":
        print("\nYou have successfully logged out!\n")
        menue()

    elif choice == "0":
        print("Bye!")
        exit()


def balance():
    print("\nBalance: 0\n")


def luhn(card_num):
    t = 1
    s = 0
    for i in card_num:
        i = int(i)
        if t % 2 == 0:  # print("当前是偶数位")
            s += i

        else:
            # print("当前为奇数位")
            if (i * 2) < 10:
                s = s + (i * 2)
            else:
                s = s + (i * 2) - 9
        t += 1
    if s % 10 == 0:
        finald = 0
    else:
        finald = 10 - (s % 10)
    return str(f"{card_num}{finald}")


def is_luhn(card_id):
    odd_as_int = [int(x) for x in card_id[::-2]]
    even_as_int = [int(x) for x in card_id[-2::-2]]
    total1 = 0
    total2 = 0
    for x in even_as_int:
        if (x * 2) > 9:
            total1 += ((x * 2) - 9)
        else:
            total1 += x * 2

    for y in odd_as_int:
        total2 += y

    if (total1 + total2) % 10 == 0:
        return True
    else:
        return False


# Program
# Dict with CC numbers & PINs
#cards = {}

# run the menue for the first time
menue()
