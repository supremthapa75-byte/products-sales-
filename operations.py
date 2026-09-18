# operations.py

def display_products(products_data):
    """
    Displays available products in a formatted manner.
    """
    print("\n-------------------- AVAILABLE PRODUCTS --------------------")
    header = "ID\tName                  \tBrand                 \tQty\tPrice (Cost)\tOrigin"
    print(header)
    print("-" * (len(header) + 15))

    if not products_data:
        print("No products available in the inventory.")
        print("----------------------------------------------------------")
        return

    ids_to_display = list(products_data.keys())
    n = len(ids_to_display)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if int(ids_to_display[j]) < int(ids_to_display[min_idx]): # Ensure comparison as int
                min_idx = j
        ids_to_display[i], ids_to_display[min_idx] = ids_to_display[min_idx], ids_to_display[i]


    for product_id in ids_to_display:
        details = products_data[product_id]
        name = details[0]
        brand = details[1]
        quantity = details[2]
        cost_price = details[3]
        origin = details[4]

        name_col_width = 22
        brand_col_width = 22

        name_display = name
        if len(name) > name_col_width:
            name_display = name[:name_col_width-3] + "..."
        else:
            name_display = name + " " * (name_col_width - len(name))

        brand_display = brand
        if len(brand) > brand_col_width:
            brand_display = brand[:brand_col_width-3] + "..."
        else:
            brand_display = brand + " " * (brand_col_width - len(brand))

        price_str = "%.2f" % cost_price

        print(str(product_id) + "\t" + name_display + "\t" + brand_display + "\t" + \
              str(quantity) + "\t" + price_str + "\t\t" + origin)
    print("---------------------------------------------------------------------------------")


def get_valid_product_id(products_data, prompt_message, allow_zero=False):
    """
    Gets a valid product ID from user input.
    If allow_zero is True, 0 is considered a valid input (e.g., to stop adding items).
    """
    while True:
        try:
            pid_str = input(prompt_message)
            pid = int(pid_str)
            if allow_zero and pid == 0:
                return 0
            if pid not in products_data: # Assumes keys are integers
                print("Error: Product ID not found. Please enter a valid ID from the list.")
            else:
                return pid
        except ValueError:
            print("Error: Invalid input. Please enter a numerical Product ID.")
        except Exception as e:
            print("An unexpected error occurred with product ID input: " + str(e))


def get_valid_quantity(prompt_message):
    """
    Gets a valid positive integer quantity from user input.
    """
    while True:
        try:
            qty_str = input(prompt_message)
            qty = int(qty_str)
            if qty <= 0:
                print("Error: Quantity must be a positive whole number.")
            else:
                return qty
        except ValueError:
            print("Error: Invalid input. Please enter a numerical quantity.")
        except Exception as e:
            print("An unexpected error occurred with quantity input: " + str(e))


def sell_products(products_data):
    """
    Handles the process of selling one or more products to a customer.
    Updates product_data in memory and returns it along with bill details.
    """
    if not products_data:
        print("Inventory is empty. Cannot sell products.")
        return products_data, None

    customer_name = input("Enter Customer Name: ")

    sold_items_for_bill = []
    current_sale_subtotal = 0.0
    apply_clearance_discount = False # Flag to check if any item goes out of stock

    while True:
        display_products(products_data)
        product_id = get_valid_product_id(products_data, "Enter Product ID to sell (or 0 to finish current sale): ", allow_zero=True)

        if product_id == 0:
            if not sold_items_for_bill:
                print("No products were selected for this sale.")
                return products_data, None
            break

        product_details = products_data[product_id]
        product_name = product_details[0]
        current_stock = product_details[2]
        cost_price = product_details[3]
        selling_price_per_unit = cost_price * 2.0

        print("Selected: " + product_name + " (Stock: " + str(current_stock) + ", Selling Price/unit: Rs. " + ("%.2f" % selling_price_per_unit) + ")")
        requested_quantity = get_valid_quantity("Enter quantity to sell: ")

        free_items = requested_quantity // 3
        total_quantity_to_deduct_from_stock = requested_quantity + free_items

        if total_quantity_to_deduct_from_stock > current_stock:
            print("Error: Not enough stock for " + product_name + ".")
            print("Available: " + str(current_stock) + ", Required (incl. free): " + str(total_quantity_to_deduct_from_stock) + ". Please try a smaller quantity.")
            continue

        products_data[product_id][2] -= total_quantity_to_deduct_from_stock
        if products_data[product_id][2] == 0: # Check if stock became 0
            apply_clearance_discount = True
            print("INFO: Product " + product_name + " is now out of stock. Clearance discount may apply to the bill.")


        item_sale_total = requested_quantity * selling_price_per_unit
        current_sale_subtotal += item_sale_total

        sold_items_for_bill.append({
            'id': product_id,
            'name': product_name,
            'quantity': requested_quantity,
            'price_per_unit': selling_price_per_unit,
            'total': item_sale_total,
            'free_items_received': free_items,
            'total_deducted_stock': total_quantity_to_deduct_from_stock
        })

        print(str(requested_quantity) + " " + product_name + "(s) added to bill.")
        if free_items > 0:
            print("BONUS: Customer receives " + str(free_items) + " " + product_name + "(s) for free!")

        another_item_choice = input("Sell another product in this transaction? (yes/no): ")
        if not (another_item_choice == "yes" or another_item_choice == "YES" or \
                another_item_choice == "y" or another_item_choice == "Y"):
            break

    if not sold_items_for_bill:
        return products_data, None

    # Sales Invoice Logic
    discount_amount = 0.0
    if apply_clearance_discount:
        discount_amount = current_sale_subtotal * 0.10
        print("INFO: Applying 10% clearance discount to the subtotal.")

    amount_after_discount = current_sale_subtotal - discount_amount
    vat_amount = amount_after_discount * 0.13 # VAT is 13% of the (Subtotal - Discount)
    grand_total_payable = amount_after_discount + vat_amount

    bill_details_for_writing = {
        "customer_name": customer_name,
        "items_list": sold_items_for_bill,
        "subtotal": current_sale_subtotal,
        "discount_amount": discount_amount,
        "vat_amount": vat_amount,
        "grand_total": grand_total_payable,
    }

    print("\n--- Sale Transaction Summary ---")
    for item in sold_items_for_bill:
        print(item['name'] + " - Qty Paid: " + str(item['quantity']) + ", Free: " + str(item['free_items_received']) + ", Total Deducted: " + str(item['total_deducted_stock']))

    return products_data, bill_details_for_writing


def purchase_products(products_data):
    """
    Handles purchasing products: restocking existing or adding new ones.
    Updates product_data in memory and returns it along with bill details.
    """
    print("\n--- Purchase from Manufacturer/Supplier ---")

    purchased_items_for_bill = []
    current_purchase_total_cost = 0.0

    while True:
        print("\nPurchase Options:")
        print("1. Restock an existing product")
        print("2. Add a completely new product")
        print("3. Finish current purchase transaction")

        action_choice_str = input("Enter your choice (1-3): ")
        try:
            action_choice = int(action_choice_str)
        except ValueError:
            print("Invalid choice. Please enter a number (1, 2, or 3).")
            continue

        if action_choice == 1:
            if not products_data:
                print("No products exist to restock. Please add a new product first (Option 2).")
                continue

            display_products(products_data)
            product_id = get_valid_product_id(products_data, "Enter Product ID of existing product to restock: ")

            product_details = products_data[product_id]
            product_name = product_details[0]
            cost_price = product_details[3]

            print("Selected for restock: " + product_name + " (Current Stock: " + str(product_details[2]) + ", Cost Price/unit: Rs. " + ("%.2f" % cost_price) + ")")
            quantity_to_add = get_valid_quantity("Enter quantity to add to stock: ")

            products_data[product_id][2] += quantity_to_add
            item_total_purchase_cost = quantity_to_add * cost_price
            current_purchase_total_cost += item_total_purchase_cost

            purchased_items_for_bill.append({
                'id': product_id,
                'name': product_name,
                'brand': product_details[1],
                'quantity': quantity_to_add,
                'price_per_unit': cost_price,
                'total': item_total_purchase_cost
            })
            print(str(quantity_to_add) + " " + product_name + "(s) restocked. New stock: " + str(products_data[product_id][2]))

        elif action_choice == 2:
            print("\n--- Add New Product to Inventory ---")
            new_product_name = input("Enter new product's Name: ")
            new_product_brand = input("Enter new product's Brand: ")
            new_product_quantity = get_valid_quantity("Enter initial quantity for this new product: ")

            new_product_cost_price = 0.0
            while True:
                try:
                    new_product_cost_price_str = input("Enter cost price per unit for the new product: ")
                    new_product_cost_price = float(new_product_cost_price_str)
                    if new_product_cost_price <= 0:
                        print("Cost price must be a positive number.")
                    else:
                        break
                except ValueError:
                    print("Invalid price format. Please enter a number (e.g., 150.75).")

            new_product_origin = input("Enter new product's Country of Origin: ")

            new_id = 0
            if products_data:
                max_existing_id = 0
                for k_id in products_data.keys():
                    if int(k_id) > int(max_existing_id): # Ensure comparison as int
                        max_existing_id = k_id
                new_id = int(max_existing_id) + 1
            else:
                new_id = 1

            products_data[new_id] = [new_product_name, new_product_brand, new_product_quantity, new_product_cost_price, new_product_origin]
            item_total_purchase_cost = new_product_quantity * new_product_cost_price
            current_purchase_total_cost += item_total_purchase_cost

            purchased_items_for_bill.append({
                'id': new_id,
                'name': new_product_name,
                'brand': new_product_brand,
                'quantity': new_product_quantity,
                'price_per_unit': new_product_cost_price,
                'total': item_total_purchase_cost
            })
            print("New product '" + new_product_name + "' (ID: " + str(new_id) + ") added with stock " + str(new_product_quantity) + ".")

        elif action_choice == 3:
            if not purchased_items_for_bill:
                print("No products were restocked or added in this transaction.")
                return products_data, None
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    if not purchased_items_for_bill:
        return products_data, None

    # Purchase Invoice Logic
    discount_amount = 0.0 # No discount for purchases
    vat_amount = 0.0      # No VAT for purchases
    grand_total_paid_by_store = current_purchase_total_cost # Grand total is just the subtotal

    bill_details_for_writing = {
        "customer_name": "Store Purchase (Self/Supplier)",
        "items_list": purchased_items_for_bill,
        "subtotal": current_purchase_total_cost,
        "discount_amount": discount_amount, # Will be 0
        "vat_amount": vat_amount,          # Will be 0
        "grand_total": grand_total_paid_by_store,
    }

    return products_data, bill_details_for_writing
