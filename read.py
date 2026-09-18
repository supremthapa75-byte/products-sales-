# read.py

def load_products(filename="Products.txt"):
    """
    Loads product data from a specified file.
    Each line in the file should be: name,brand,quantity,price,origin
    Returns a dictionary of products.
    """
    products_data = {}
    try:
        with open(filename, "r") as file:
            product_id_counter = 1
            for line in file:
                # Manually remove newline character if present at the end of the line
                if line and line[-1] == '\n': # Check if line is not empty before accessing -1
                    line = line[:-1]

                if not line: # Skip empty lines
                    continue

                parts = line.split(",")
                if len(parts) == 5:
                    name = parts[0]
                    brand = parts[1]
                    try:
                        quantity = int(parts[2])
                        price = float(parts[3])
                    except ValueError:
                        # Using string concatenation as f-strings/format are disallowed
                        print("Warning: Invalid quantity or price for product data: '" + line + "'. Skipping.")
                        continue
                    origin = parts[4]
                    products_data[product_id_counter] = [name, brand, quantity, price, origin]
                    product_id_counter += 1
                else:
                    print("Warning: Malformed line in " + filename + ": '" + line + "'. Skipping.")
    except FileNotFoundError:
        print("Error: " + filename + " not found. Starting with an empty inventory.")
    except Exception as e:
        # Using str(e) for error message
        print("An unexpected error occurred while loading products: " + str(e))
    return products_data

def read_bill_counter(filename="bill_counter.txt"):
    """
    Reads the current bill counter value from its file.
    Returns the counter value, or 0 if file not found or invalid.
    """
    try:
        with open(filename, "r") as file:
            counter_line = file.readline()
            # Remove newline if present, as int() can fail with it. No strip() allowed.
            if counter_line and counter_line[-1] == '\n':
                counter_line = counter_line[:-1]

            if not counter_line: # Handle empty file or line
                print("Warning: " + filename + " is empty. Resetting counter to 0.")
                return 0

            counter = int(counter_line)
            return counter
    except FileNotFoundError:
        return 0 # Start from 0 if file doesn't exist
    except ValueError:
        print("Warning: " + filename + " contains invalid data. Resetting counter to 0.")
        return 0
    except Exception as e:
        print("Error reading bill counter from " + filename + ": " + str(e))
        return 0
