from os import error
from BankException import BankException

class Account:

    def __init__(self, name, acc_num, allowed, sav_bal=0, cur_bal =0): #might remove sav_bal and cur_bal
        self.name = name
        self.acc_num = acc_num
        self.sav_bal = 0
        self.cur_bal = 0
        if allowed == "False":
            self.exists = False #if the account is deleted or not.
        else:
            self.exists = True

    def set_name(self):
        raise BankException("Cannot change name")

    def set_acc_num(self):
        raise BankException("Cannot change account number")

    def get_name(self):
        return self.name
    
    def get_acc_num(self):
        return self.acc_num

    def get_sav_bal(self):
        return self.sav_bal

    def get_cur_bal(self):
        return self.cur_bal

    def set_sav_bal(self, Xbal):
        self.sav_bal = Xbal

    def set_cur_bal(self, Xbal):
        self.cur_bal = Xbal

    def savings_details(self):
        pass

    def current_details(self):
        pass

    def _exists(self):
        return self.exists

    def deposit_savings(self, num):
        self.sav_bal += num
    
    def deposit_current(self,num):
        self.cur_bal += num

    def withdraw_savings(self, num):
        self.sav_bal -= num
    
    def withdraw_current(self, num):
        self.cur_bal -= num