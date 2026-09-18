# write.py
import datetime # Allowed for datetime.datetime.now() parts, not strftime

def save_products(filename, products_data):
    """
    Saves the current product data back to the specified file.
    """
    try:
        with open(filename, "w") as file:
            product_ids_to_write = list(products_data.keys())
            n = len(product_ids_to_write)
            for i in range(n):
                for j in range(0, n-i-1):
                    # Ensure keys are comparable, assuming they are integers
                    if int(product_ids_to_write[j]) > int(product_ids_to_write[j+1]):
                        product_ids_to_write[j], product_ids_to_write[j+1] = product_ids_to_write[j+1], product_ids_to_write[j]

            for product_id in product_ids_to_write:
                details = products_data[product_id]
                line_parts = [
                    str(details[0]), # name
                    str(details[1]), # brand
                    str(details[2]), # quantity
                    "%.2f" % details[3], # price
                    str(details[4])  # origin
                ]
                file.write(",".join(line_parts) + "\n")
    except Exception as e:
        print("Error saving products to " + filename + ": " + str(e))

def write_bill_counter(new_counter, filename="bill_counter.txt"):
    """
    Writes the new bill counter value to its file.
    """
    try:
        with open(filename, "w") as file:
            file.write(str(new_counter))
    except Exception as e:
        print("Error writing to " + filename + ": " + str(e))

def generate_unique_bill_id(counter):
    """
    Generates a unique bill ID using current date/time components and a counter.
    No strftime is used.
    """
    now = datetime.datetime.now()
    year = str(now.year)

    month_val = now.month
    month_str = str(month_val)
    if month_val < 10:
        month_str = "0" + month_str

    day_val = now.day
    day_str = str(day_val)
    if day_val < 10:
        day_str = "0" + day_str

    return year + month_str + day_str + "_" + str(counter)

def print_and_save_bill(bill_id, customer_name, items_list,
                        subtotal, discount_amount, vat_amount, grand_total,
                        bill_type, company_name, company_address):
    """
    Formats, prints to console, and saves a bill to a unique file.
    bill_type can be "SALE" or "PURCHASE".
    items_list is a list of dictionaries, each:
    {'name': str, 'quantity': int, 'price_per_unit': float, 'total': float}
    """
    bill_content_list = []

    bill_content_list.append("\n" * 2)
    bill_content_list.append("\t\t\t\t" + company_name + "\n")
    bill_content_list.append("\t\t\t" + company_address + "\n")
    bill_content_list.append("\n")

    if bill_type == "SALE":
        bill_content_list.append("-------------------- SALE INVOICE --------------------\n")
    elif bill_type == "PURCHASE":
        bill_content_list.append("------------------ PURCHASE INVOICE ------------------\n")

    now = datetime.datetime.now()
    month_val = now.month
    month_str = str(month_val)
    if month_val < 10: month_str = "0" + month_str
    day_val = now.day
    day_str = str(day_val)
    if day_val < 10: day_str = "0" + day_str
    date_str = str(now.year) + "-" + month_str + "-" + day_str

    hour_val = now.hour
    hour_str = str(hour_val)
    if hour_val < 10: hour_str = "0" + hour_str
    minute_val = now.minute
    minute_str = str(minute_val)
    if minute_val < 10: minute_str = "0" + minute_str
    second_val = now.second
    second_str = str(second_val)
    if second_val < 10: second_str = "0" + second_str
    time_str = hour_str + ":" + minute_str + ":" + second_str

    bill_content_list.append("Bill ID: " + bill_id + "\n")
    bill_content_list.append("Date: " + date_str + "\tTime: " + time_str + "\n\n")

    if bill_type == "SALE":
        bill_content_list.append("Customer Name: " + customer_name + "\n\n")
    elif bill_type == "PURCHASE":
        bill_content_list.append("Supplier: Manufacturer/Internal\n\n")

    header_line = "S.N.\tProduct Name          \tQty\tUnit Price\tTotal Price\n"
    separator_line = "-" * 65 + "\n"

    bill_content_list.append(separator_line)
    bill_content_list.append(header_line)
    bill_content_list.append(separator_line)

    item_serial_number = 1
    for item in items_list:
        name_col = item['name']
        max_name_len = 20
        if len(name_col) > max_name_len:
            name_col = name_col[:max_name_len-3] + "..."
        else:
            name_col = name_col + " " * (max_name_len - len(name_col))

        unit_price_str = "%.2f" % item['price_per_unit']
        item_total_str = "%.2f" % item['total']

        line = str(item_serial_number) + "\t" + \
               name_col + "\t" + \
               str(item['quantity']) + "\t" + \
               unit_price_str + "\t\t" + \
               item_total_str + "\n"
        bill_content_list.append(line)
        item_serial_number += 1

    bill_content_list.append(separator_line)

    if bill_type == "SALE":
        bill_content_list.append("\t\t\t\tSubtotal: \tRs. " + ("%.2f" % subtotal) + "\n")
        if discount_amount > 0: # Only print discount if it's applied
            bill_content_list.append("\t\t\t\tClearance Discount (10%): Rs. " + ("%.2f" % discount_amount) + "\n")
        net_amount_for_display = subtotal - discount_amount
        bill_content_list.append("\t\t\t\tNet Amount: \tRs. " + ("%.2f" % net_amount_for_display) + "\n")
        bill_content_list.append("\t\t\t\tVAT (13%): \tRs. " + ("%.2f" % vat_amount) + "\n")
    elif bill_type == "PURCHASE":
        bill_content_list.append("\t\t\t\tSubtotal: \tRs. " + ("%.2f" % subtotal) + "\n")
        # No Discount or VAT lines for purchase from manufacturer

    bill_content_list.append(separator_line)
    bill_content_list.append("\t\t\t\tGRAND TOTAL: \tRs. " + ("%.2f" % grand_total) + "\n")
    bill_content_list.append(separator_line)

    if bill_type == "SALE":
        bill_content_list.append("\nThank you for your purchase, " + customer_name + "!\n")
    elif bill_type == "PURCHASE":
        bill_content_list.append("\nItems purchased/restocked successfully.\n")
    bill_content_list.append("\n" * 2)

    final_bill_string = "".join(bill_content_list)
    print(final_bill_string)

    bill_filename_prefix = "SALE_BILL_" if bill_type == "SALE" else "PURCHASE_BILL_"
    bill_filename = bill_filename_prefix + bill_id + ".txt"
    try:
        with open(bill_filename, "w") as file:
            file.write(final_bill_string)
        print("Bill successfully saved as " + bill_filename)
    except Exception as e:
        print("Error saving bill to file " + bill_filename + ": " + str(e))
