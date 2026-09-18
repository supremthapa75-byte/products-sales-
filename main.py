# main.py
import read
import write
import operations

# Global constants for company details and filenames
COMPANY_NAME = "TopskinCare Wholesale"
COMPANY_ADDRESS = "Madhyapur, Thimi, Bhaktapur"
PRODUCTS_FILENAME = "Products.txt"
BILL_COUNTER_FILENAME = "bill_counter.txt"

def display_welcome_message():
    """Prints the welcome message for the system."""
    print("\n" * 2)
    print("\t\t\t\t\t" + COMPANY_NAME)
    print("\n")
    print("\t\t\t" + COMPANY_ADDRESS)
    print("\n")

def main_program_loop():
    """Runs the main interactive loop for the wholesale system."""
    display_welcome_message()

    products_inventory = read.load_products(PRODUCTS_FILENAME)

    system_active = True
    while system_active:
        print("\n=========== Main Menu ===========")
        print("1. Sell Product(s) to Customer")
        print("2. Purchase Product(s) (Restock/Add New)")
        print("3. Display All Available Products")
        print("4. Exit System")
        print("===============================")

        user_choice_str = input("Enter your choice (1-4): ")

        try:
            main_menu_choice = int(user_choice_str)
        except ValueError:
            print("Error: Invalid input! Please enter a number between 1 and 4.")
            continue
        except Exception as e:
            print("An unexpected error occurred with your input: " + str(e))
            continue

        if main_menu_choice == 1: # Sell Products
            updated_inventory_after_sale, sale_bill_details = operations.sell_products(products_inventory)

            if sale_bill_details:
                products_inventory = updated_inventory_after_sale

                current_bill_num = read.read_bill_counter(BILL_COUNTER_FILENAME)
                new_bill_num = current_bill_num + 1
                unique_bill_id = write.generate_unique_bill_id(new_bill_num)

                write.print_and_save_bill(
                    unique_bill_id,
                    sale_bill_details["customer_name"],
                    sale_bill_details["items_list"],
                    sale_bill_details["subtotal"],
                    sale_bill_details["discount_amount"],
                    sale_bill_details["vat_amount"],
                    sale_bill_details["grand_total"],
                    "SALE",
                    COMPANY_NAME,
                    COMPANY_ADDRESS
                )
                write.save_products(PRODUCTS_FILENAME, products_inventory)
                write.write_bill_counter(new_bill_num, BILL_COUNTER_FILENAME)
            else:
                print("Sale operation did not complete or no items were sold. No bill generated.")

        elif main_menu_choice == 2: # Purchase Products
            updated_inventory_after_purchase, purchase_bill_details = operations.purchase_products(products_inventory)

            products_inventory = updated_inventory_after_purchase # Persist any changes even if no bill

            if purchase_bill_details:
                current_bill_num = read.read_bill_counter(BILL_COUNTER_FILENAME)
                new_bill_num = current_bill_num + 1
                unique_bill_id = write.generate_unique_bill_id(new_bill_num)

                write.print_and_save_bill(
                    unique_bill_id,
                    purchase_bill_details["customer_name"],
                    purchase_bill_details["items_list"],
                    purchase_bill_details["subtotal"],
                    purchase_bill_details["discount_amount"], # Will be 0
                    purchase_bill_details["vat_amount"],       # Will be 0
                    purchase_bill_details["grand_total"],
                    "PURCHASE",
                    COMPANY_NAME,
                    COMPANY_ADDRESS
                )
                write.write_bill_counter(new_bill_num, BILL_COUNTER_FILENAME)
            else:
                print("Purchase operation did not complete with billable items or was cancelled.")

            write.save_products(PRODUCTS_FILENAME, products_inventory) # Save after any purchase op


        elif main_menu_choice == 3: # Display Products
            operations.display_products(products_inventory)

        elif main_menu_choice == 4: # Exit
            print("\nThank you for using the " + COMPANY_NAME + " system.")
            print("Exiting now...")
            system_active = False

        else:
            print("Error: Invalid choice. Please select an option from 1 to 4.")

if __name__ == "__main__":
    main_program_loop()
