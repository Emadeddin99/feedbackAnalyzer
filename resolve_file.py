import os
import random
import string

def resolve_filename(filename):
    """
    If the file already exists, prompt the user:
      [O] Overwrite   [K] Keep both (new file gets a suffix)   [C] Cancel
    Returns the final filename to save to, or None if cancelled.
    """
    if not os.path.exists(filename):
        return filename

    # If file exists, split into base and extension for suffixing
    base, ext = os.path.splitext(filename)
 
    print(f"\nFile already exists: {filename}")
    print("  [O] Overwrite")
    print("  [K] Keep both (new file gets a random suffix)")
    print("  [C] Cancel saving")

    # Loop until valid input is received
    while True:
        choice = input("Your choice (O/K/C): ").strip().upper()

        if choice == "O":
            return filename

        #if user chooses to keep both, generate a random suffix and create a new filename
        elif choice == "K":
            suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))#generate a random 5-character suffix using lowercase letters and digits
            new_filename = f"{base}_{suffix}{ext}" #create new filename by inserting suffix before the file extension
            print(f"New file will be saved as: {new_filename}") #inform user of the new filename that will be used to save the file
            return new_filename

        elif choice == "C":
            print("Save cancelled.")
            return None

        else:
            print("Invalid input. Please enter O, K, or C.")