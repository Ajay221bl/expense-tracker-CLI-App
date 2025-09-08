# you should be able to add an expense
# you should be able to delete an expense
# you should be able to update an expense
# you should be able to list all the expenses
# you should be able to get the total expense
# you should be able to get total expense in a particular month

from datetime import datetime
import argparse
import sys
import json
# class for expense tracker object
class ExpenseTracker():
    def __init__(self):
        pass
    def main(self):

        parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="A simple command-line to track your expenses",
        epilog="Happy tracking!"
        )
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit()

        subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
        parser_add = subparsers.add_parser("add", help="Add a new expense")
        parser_add.add_argument("--description", type=str, required=True, help="Description of the expense")
        parser_add.add_argument("--amount", type=float, required=True, help="Amount of the expense")

        parser_list = subparsers.add_parser("list", help= "List all expenses")

        parser_delete = subparsers.add_parser("delete", help="Delete an expense by its ID")
        parser_delete.add_argument("--id", type=int, required=True, help="ID of the expense to delete")

        parser_update = subparsers.add_parser("update", help= "Update an expense by its ID")
        parser_update.add_argument("--id", type=int, required=True, help="ID of expense to update")
        parser_update.add_argument("--description", type=str, required=True, help=" New Description of the expense")
        parser_update.add_argument("--amount", type=float, required=True, help=" New Amount of the expense")

        parser_summary = subparsers.add_parser("summary", help="Show summary of expenses of a month")
        parser_summary.add_argument("--month", type=int, choices=range(1, 13), metavar="[1-12]", help="Filter summary by month")


        args = parser.parse_args()

        if args.command == "add":
            self.add( args.description, args.amount)
        
        elif args.command == "update":
            
            self.update(args.id, args.description, args.amount)

        elif args.command == "delete":
            self.delete(args.id)

        elif args.command== "summary":
            if args.month:
                self.monthly_summary(args.month)
            elif not args.month:
                self.summary()
        elif args.command == "list":
            self.list()

                

    
    def add(self, desc, amount):
        expense = Expense(desc, amount)
        try:
            outer_dict = self._load_data()
        except (FileNotFoundError, json.JSONDecodeError):
                outer_dict = {}
        if outer_dict:
            max_id = max([int(k) for k in outer_dict.keys()])
            id= max_id + 1
        else:
            id = 1
        outer_dict[id] = {"description": expense.desc,
                        "date": str(expense.date),
                        "amount": expense.amount
                        }
                
        self._save_data(outer_dict)
        print(f"Expense added successfully (ID: {id})")

        
    
    def update(self, id: int, desc: str, amount: int):
        try:
            
            outer_dict = self._load_data()
            id_found = False
            for k in outer_dict:
                if id == int(k):
                    id_found = True
                    outer_dict[k]["description"] = desc
                    outer_dict[k]["amount"] = amount
                    break
            if not id_found:
                print(f"No expense with (ID: {id}) exists")
            elif id_found:
                self._save_data(outer_dict)
                print(f"Expense with (ID: {id}) updated successfully")
        except json.JSONDecodeError:
            print("The list is empty")
                
                

    def delete(self, id: int):
        try:
            expenses = self._load_data()
            id_found = False
            for k in expenses.keys():
                if id == int(k):
                    id_found = True
                    break
            if id_found:
                expenses.pop(str(id))
                self._save_data(expenses)
                print(f"Expense with (ID: {id}) deleted successfully")
            elif not id_found:
                print("The expense doesn't exist")
        except json.JSONDecodeError:
            print("The list is empty")


                

    def summary(self):
        total_amount = 0
        try:
            outer_dict = self._load_data()
            for expense in outer_dict.values():
                total_amount += expense["amount"]
            print(f"Total expenses: ${total_amount}")
        except json.JSONDecodeError:
            print("The list is empty")


    def monthly_summary(self, month_num: int):
        monthly_total = 0
        month_found = False
        try:
            outer_dict = self._load_data()
            for expense in outer_dict.values():
                date_value = datetime.strptime(expense["date"], "%Y-%m-%d")
                if date_value.month ==  month_num:
                    month_found = True
                    req_month = date_value.strftime("%B")
                    monthly_total += expense["amount"]
            if month_found:
                print(f"Total expenses in {req_month}: {monthly_total}")
            elif not month_found:
                print("The expenses don't exist for this month")
        except json.JSONDecodeError:
            print("The list is empty")
        


    def list(self):
            try:
                expenses = self._load_data()
        
                list_of_length_of_descriptions = [len(info["description"]) for info in expenses.values()]
                max_len_description = max(list_of_length_of_descriptions)
            
            
                self.id_heading = "ID".ljust(6)
                self.date_heading = "Date".ljust(15)
                self.description_heading = "Description".ljust(max_len_description + 4)
                self.amount_heading = "Amount"
                print(f"{self.id_heading}{self.date_heading}{self.description_heading}{self.amount_heading}")
                for id, info in expenses.items():
                    id_string = str(id).ljust(6)
                    date_string = str(info["date"]).ljust(15)
                    desc_string = str(info["description"]).ljust(max_len_description + 4)
                    amount_string = ("$"+str(info["amount"]))
                    print(f"{id_string}{date_string}{desc_string}{amount_string}")
            except (json.JSONDecodeError, KeyError, ValueError):
                print("The list is empty")

    def _load_data(self):
        with open("content.json") as file:
            return json.load(file)
    
    def _save_data(self, content_to_dump):
        with open("content.json", "w") as file:
            json.dump(content_to_dump, file, indent=4)
 # class for expense object
class Expense():

    def __init__(self,desc : str, amount: int):
        self.desc = desc
        self.amount = amount
        self.date = datetime.now().date()


expense_tracker = ExpenseTracker()
expense_tracker.main()
