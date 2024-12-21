import csv
from datetime import datetime

class AccountingApp:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, trans_type, amount, vat_applicable, description, category):
        vat_rate = 0.2 if vat_applicable else 0
        vat_amount = amount * vat_rate if trans_type == "Income" else -amount * vat_rate
        net_amount = amount + vat_amount if trans_type == "Income" else amount + vat_amount
        transaction = {
            "type": trans_type,
            "amount": amount,
            "vat_applicable": vat_applicable,
            "vat_amount": vat_amount,
            "net_amount": net_amount,
            "description": description,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        self.transactions.append(transaction)

    def generate_report(self):
        if not self.transactions:
            print("\nNo transactions recorded yet.")
            return

        income = sum(t["net_amount"] for t in self.transactions if t["type"] == "Income")
        expenses = sum(t["net_amount"] for t in self.transactions if t["type"] == "Expense")
        vat_total = sum(t["vat_amount"] for t in self.transactions)
        print("\n--- Accounting Report ---")
        print(f"Total Income: £{income:.2f}")
        print(f"Total Expenses: £{expenses:.2f}")
        print(f"VAT Owed: £{vat_total:.2f}")
        print(f"Net Profit: £{income + expenses:.2f}\n")

    def export_to_csv(self, filename="accounting_report.csv"):
        if not self.transactions:
            print("\nNo transactions to export.")
            return

        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.transactions[0].keys())
                writer.writeheader()
                writer.writerows(self.transactions)
            print(f"Report exported to {filename}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

def main():
    app = AccountingApp()
    print("Welcome to the UK Small Business Accounting App!")

    while True:
        print("\n1. Add Transaction")
        print("2. Generate Report")
        print("3. Export to CSV")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            while True:
                trans_type = input("Enter transaction type (Income/Expense): ").strip().capitalize()
                if trans_type in ["Income", "Expense"]:
                    break
                else:
                    print("Invalid entry. Please enter 'Income' or 'Expense'.")

            while True:
                try:
                    amount = float(input("Enter amount (in GBP): ").strip())
                    if amount > 0:
                        break
                    else:
                        print("Amount must be a positive number.")
                except ValueError:
                    print("Invalid entry. Please enter a valid number.")

            while True:
                vat_applicable = input("Is VAT applicable? (Yes/No): ").strip().lower()
                if vat_applicable in ["yes", "no"]:
                    vat_applicable = vat_applicable == "yes"
                    break
                else:
                    print("Invalid entry. Please enter 'Yes' or 'No'.")

            description = input("Enter description: ").strip()
            category = input("Enter category (e.g., Sales, Rent, Utilities): ").strip()
            app.add_transaction(trans_type, amount, vat_applicable, description, category)

        elif choice == "2":
            app.generate_report()
        elif choice == "3":
            app.export_to_csv()
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
