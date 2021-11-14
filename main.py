from Accounts import Account
from datetime import date
from queue import Queue
#date.today().strftime("%d-%m-%Y")


def login():
    """ Takes user input and returns user account object and login value e.g.
    (Customer, True) or returns (True, True) if an employee"""
    valid_login = False  # variable to check if login details is right.

    user_type = user_types() #Get the Account type

    # Showcase the appropriate display based on input
    if user_type == "B":  # if the user is an employee
        pin = input("PIN >>> ") #get employee pin
        while pin != "A1234": #keep getting the pin until it is correct.
            print("Wrong information Try again.")
            pin = input("PIN >>> ")
            print()
        valid_login = True
        return True

    else: # if the user is a customer
        while not valid_login:
            first_name = input("First name >>> ")
            last_name = input("Last name >>> ")
            account_number = input("Account number >>> ")
            pin = input("pin >>> ")

            #check if the account exists. 
            customers_file = open('customers.txt', 'r')#open the customers file
            for line in customers_file:
                customer_array = line.strip("\n").split(",")
                if (account_number == customer_array[2]) and (pin == customer_array[3]): 
                    valid_login = True
                    user = Account((customer_array[0]+" "+customer_array[1]), customer_array[2], customer_array[4])
                    return user

        #if not. Display error that wrong credentials were entered
            if valid_login == False:
                print("Wrong credentials inputted.")

def user_types():
    """ Gets account type from the user and returns it.
    """
    valid = False
    while not valid:  # Bank employee or customer
        account_type = input("Are you a bank employee(B) or a Customer(C) >>> ")
        if account_type == "B" or account_type == "C":
            valid = True
    return account_type

def card_type():
    """choose between savings or Current"""
    while True: #Run until a suitable input is passed.
        question = input("Savings(S) or Current(C) >>> ")
        if question == "S":  #if savings account
            return "savings"
        elif question == "C": #if current account
            return "current"

def todays_choice():
    """choose between withdrawal or deposit"""
    while True: #Run until a suitable input is passed.
        question = input("Deposit(D) or Withdrawal(W) or History(H) or Balance(B) >>> ")
        if question == "D":  #if savings account
            return "deposit"
        elif question == "W": #if current account
            return "withdraw"
        elif question == "H":
            return "history"
        elif question == "B":
            return "balance"

def amount_entered():
    """Gets the amount to be transacted"""
    while True: #Run until a suitable input is passed.
        try:
            amt = int(input("Enter value you wish to trade >>> "))
            if amt <= 0:
                raise Exception
            return amt
        except ValueError: #if a string is entered
            print("Please enter an integer")
        except Exception:   #if a negative digit is entered
            print("Value cannot be less than or equal to 0")

def account_bal(user, card):
    """Returns account balance for the users savings & current account"""
    amount = 0
    if card == "savings":   #savings
        file = user.get_acc_num()+"-"+"savings.txt"
        file_opened = open(file)
        for line in file_opened:
            line_array =line.split("\\t")
            if line_array[1] == "deposit":
                amount += float(line_array[2]) #check this with \t
            else:
                amount -= float(line_array[2]) #check this with \t
        return amount
    else:   #current
        file = user.get_acc_num()+"-"+"current.txt"
        file_opened = open(file)
        for line in file_opened:
            line_array =line.split("\\t")
            if line_array[1] == "deposit":
                amount += float(line_array[2]) #check this with \t
            else:
                amount -= float(line_array[2]) #check this with \t
        return amount

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def final_step_customer(Xaction_type, Xcredit_type, Xcredit_file, Xusers_account):
    """handles the final step.
    Does not return anything."""
    ####################################################
    if Xaction_type == "deposit" and Xcredit_type == "savings":
        #deposit the money into the account.
        amt_entered = amount_entered()
        Xusers_account.deposit_savings(amt_entered)
        #add record to the file.
        add_this_line = "" + date.today().strftime("%m-%d-%Y") +"\\t" + Xaction_type + "\\t" + str(amt_entered) + "\\t" + str(Xusers_account.get_sav_bal())
        #append line to file
        append_new_line(Xcredit_file, add_this_line)

    if Xaction_type == "deposit" and Xcredit_type == "current":
        #deposit the money into the account.
        amt_entered = amount_entered()
        Xusers_account.deposit_current(amt_entered)
        #add record to the file.
        add_this_line = "" + date.today().strftime("%m-%d-%Y") +"\\t" + Xaction_type + "\\t" + str(amt_entered) + "\\t" + str(Xusers_account.get_cur_bal())
        #append line to file
        append_new_line(Xcredit_file, add_this_line)

    if Xaction_type == "withdraw" and Xcredit_type == "savings":
        amt_entered = amount_entered()
        #check if funds is sufficient
        if amt_entered > Xusers_account.get_sav_bal():
            print("Insufficient funds.")
        else: #withdraw the money from the account.
            Xusers_account.withdraw_savings(amt_entered)
            #add record to the file.
            add_this_line = "" + date.today().strftime("%m-%d-%Y") +"\\t" + Xaction_type + "\\t" + str(amt_entered) + "\\t" + str(Xusers_account.get_sav_bal())
            #append line to file
            append_new_line(Xcredit_file, add_this_line)

    if Xaction_type == "withdraw" and Xcredit_type == "current":
        amt_entered = amount_entered()
        #check if funds is sufficient
        if amt_entered > Xusers_account.get_cur_bal():
            print("Insufficient funds.")
        else: #withdraw the money from the account.
            Xusers_account.withdraw_current(amt_entered)
            #add record to the file.
            add_this_line = "" + date.today().strftime("%m-%d-%Y") +"\\t" + Xaction_type + "\\t" + str(amt_entered) + "\\t" + str(Xusers_account.get_cur_bal())
            #append line to file
            append_new_line(Xcredit_file, add_this_line)

    if Xaction_type == "balance" and Xcredit_type == "savings":
        print("savings total is #" + f'{users_account.get_sav_bal():,}')

    if Xaction_type == "balance" and Xcredit_type == "current":
        print("current total is #" + f'{users_account.get_cur_bal():,}')

    if Xaction_type == "history" and Xcredit_type == "savings":
        #print necessary information from the file
        print_history(Xcredit_file)

    if Xaction_type == "history" and Xcredit_type == "current":
        #print necessary information from the file
        print_history(Xcredit_file)

def print_history(Xcredit_file):
    #print necessary information from the file
    file_open = open(Xcredit_file)
    print("Your transaction History")
    print("Date---Type---amount---balance")
    for line in file_open:
        line_array = line.split("\\t")
        print(line_array[0] + "---" + line_array[1] + "---" +line_array[2] + "---"+line_array[3])

def valid_new_account(Xacc_num):
    """Checks if an account to be created already exists
    Returns True or False"""
    #open customers file
    file_opened = open('customers.txt')
    for line in file_opened:
        line_array = line.split(',')
        if Xacc_num == line_array[2]:
            return False
    return True

def valid_del_account(Xacc_num):
    """Checks if an account to be deleted exists
    Returns True or False"""
    #open customers file
    file_opened = open('customers.txt')
    for line in file_opened:
        line_array = line.split(',')
        if Xacc_num == line_array[2]: # found account
            if line_array[4].strip('\n') == "False":
                return False
            else:
                return True

def create_account(Xfirst_name, Xlast_name, Xaccn_num, Xacc_pin):
    """creates an account"""
    #1 Append account to customers.txt
    line1 = "" + Xfirst_name.title()+","+Xlast_name.title()+","+Xaccn_num+","+Xacc_pin+","+"True"
    append_new_line('customers.txt', line1)
    #2 Create savings and current text files for user
    savings_file  = Xaccn_num + "-savings.txt"
    current_file = Xaccn_num + "-current.txt"
    actual_file = open(savings_file, 'w')
    #need a minimum of a #50,000 to open a savings account
    actual_file.write("" + date.today().strftime("%m-%d-%Y") + "\\tdeposit\\t50000\\t50000")
    actual_file.close()
    #need a minimum of a #150,000 to open a current account
    actual_file = open(current_file, 'w')
    actual_file.write("" + date.today().strftime("%m-%d-%Y") + "\\tdeposit\\t150000\\t150000")
    actual_file.close()
    #3 Tell the user to login
    pass

def details_creator(Xfirst_name, Xlast_name):
    """Makes the account number & pin from the names
    of the customer and returns both """
    p1 = Xfirst_name[0].lower() + Xlast_name[0].lower()
    p2 = str(len(Xfirst_name) + len(Xlast_name))
    p3 = str(ord(Xfirst_name[0].lower()) - 96)
    p4 = str(ord(Xlast_name[0].lower()) - 96)
    pin = p3+p4
    return (("" + p1 + "-" + p2 + "-" + p3 + "-" + p4 +"") , pin)

def combined_balance(file,Xaccn_num):
    """"-----------"""
    #first get the account object
    #check if the balance is zero
    customers_file = open(file, 'r')#open the customers file
    for line in customers_file:
        customer_array = line.strip("\n").split(",")
        if (Xaccn_num == customer_array[2]):
            valid_login = True
            user = Account((customer_array[0]+" "+customer_array[1]), customer_array[2], customer_array[4])
    determinant_balance = account_bal(user,"savings")+account_bal(user,"current")
    return determinant_balance == 0

def delete_record(Xfile, Xaccn_num):
    """Changes the Exists variable of a record to False"""
    #open the file for reading 
    opened_file = open(Xfile, 'r')
    #create a queue object.
    my_queue = Queue()
    #loop through the file looking for the record.
    for line in opened_file:
        #make line array
        line_array = line.split(",")
        if Xaccn_num == line_array[2]: #if the account is found
            #change the value in the array
            line_array[4] = "False"
            line = ",".join(line_array)
        my_queue.put(line) #add line to queue
    #close the file
    opened_file.close()
    #loop through the file and write to it
    opened_file = open(Xfile,'w')
    #loop through it and write to it
    while not my_queue.empty(): #while my queue is not empty
        #Add lines to my file
        line = my_queue.get()
        if line[-1] != "\n":
            line += "\n"
        if my_queue.qsize() == 0:
            line = line[:len(line)-1]
        opened_file.write(line)
    opened_file.close()

def valid_account(text):
    """check if account is valid"""
    while True:
        Xaccn_num = input(text)
        #open the customers file
        opened_file = open('customers.txt','r')
        for line in opened_file:
            line_array = line.split(',')
            if Xaccn_num == line_array[2]:
                return Xaccn_num
        print("Account doesn't exist. ")
    
def acct_table():
    """Prints a table with customer naems and account numbers"""
    opened_file = open('customers.txt')
    opened_file.readline()
    print("Customers_name---account_number")
    for line in opened_file:
        line_array = line.split(",")
        print(line_array[0]+" "+line_array[1] + "---"+ line_array[2])
        print()

def full_table():
    """displays the full table"""
    #oen the the file
    list_of_current_account_objects = []
    opened_file =  open('customers.txt')
    opened_file.readline()
    for line in opened_file:    #get a list of all the customers accounts as objects
        line_array = line.split(",")
        customer = Account((line_array[0]+" "+line_array[1]),line_array[2],line_array[4])
        list_of_current_account_objects.append(customer)
    #update the savings & current variables for all accounts.
    for i in list_of_current_account_objects:
        i.set_sav_bal(account_bal(i,"savings"))
        i.set_cur_bal(account_bal(i,"current"))

    #print the answer
    print("customer customer account number-avings balance-current balance")
    for i in list_of_current_account_objects:
        print(i.get_name()+"---"+i.get_acc_num()+"---"+str(i.get_sav_bal())+"---"+str(i.get_cur_bal()))
        print()

def final_step_employee(Xquestion1):
    """Takes the final step """
    #if Create Account.
    if Xquestion1 == "C":
        #get values
        first_name = input("Customer first name >>> ")
        last_name = input("Customer last name >>> ")
        email = input("Customer email >>> ")
        accn_num, acc_pin = details_creator(first_name,last_name)
        #0 Check if account does not exist.
        valid = valid_new_account(accn_num)
        if valid:
            create_account(first_name, last_name, accn_num, acc_pin)
        else:
            print("That account already exists.")
            
    elif Xquestion1 == "D":
        #Delete an account.
        #Prompt employee for the account number
        accn_num = valid_account("Enter Account number to delete >>> ")
        #check if account exists
        valid = valid_del_account(accn_num)
        if valid: #if it exists
            #get balance
            zero_balance = combined_balance('customers.txt', accn_num)
            if zero_balance:
                #delete account
                #if balance is zero turn the value in customers.txt to False
                delete_record('customers.txt', accn_num)
            else: #else return error, balance not zero
                print("Cannot delete. Account balance is not zero.")
        else: #if it doesn't exists
            print("The Account you entered is already Deleted")
        
    elif Xquestion1 == "R":
        #get the account you want to acces
        valid = False
        while not valid:
            question2 = input("Account number table (N) or Account balance table (B) >>> ")
            if question2 == "N" or question2 == "B":
                valid = True
        if question2 == "N":
            #show table (customer_name|acct_number)
            acct_table()
        else:
            print("not yet made.")
            full_table()

if __name__ == "__main__":
    while True:    
    #if user or employee is returning
        users_account = login() #get users account

        #check if employee or customer
        if users_account == True: #For an Employee
            print("Create Account (C) or Delete Account (D) or Access Records (R)")
            question1 = input("Welcome Bank Employee, what would you like to do today? ^ >>>")
            while not (question1 == "C" or question1 == "D" or question1 == "R"):
                question1 = input("Create Account (C) or Delete Account (D) or Access Records (R) >>> ")
            final_step_employee(question1)

        else: #For a Customer
            if users_account._exists(): #if the account is not deleted
                print("Welcome back,", users_account.get_name()) #greet user
                #calculate users balance from the two files and add it to account object
                users_account.set_sav_bal(account_bal(users_account,"savings")) #set savings balance
                users_account.set_cur_bal(account_bal(users_account,"current")) #set current balance
                credit_type = card_type()
                credit_file = users_account.get_acc_num() +"-" + credit_type + ".txt" #Get either savings or current files name i.e file we will be working with
                action_type = todays_choice() #depsit or Withdraw or History
                #Take the final step
                final_step_customer(action_type, credit_type, credit_file, users_account)

            else: #if the account is deleted
                print("This account is Deleted")