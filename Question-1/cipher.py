
def get_valid_shift_value(prompt):
    while True:
        try:
            user_input = int(input(f"Enter {prompt}: "))

            if user_input >= 0:
                return user_input
            else:
                print("Please enter a non-negative integer")

        except ValueError:
            print("Please enter a non-negative integer")


def shift_character(character, shift, start_char, range_size):
    position = ord(character) - ord(start_char)
    new_position = (position + shift) % range_size
    encrypted_ord = ord(start_char) + new_position
    return chr(encrypted_ord)


def encrypt_file(shift1, shift2, input_path, output_path):

    with open(input_path, "r") as f:
        content = f.read()

    encrypted_text = ""

    for i in content:

        if "a" <= i <= "n":
            encrypted_i = shift_character(
                i, shift1 * shift2, "a", 14
            )

        elif "o" <= i <= "z":
            encrypted_i = shift_character(
                i, -(shift1 + shift2), "o", 12
            )

        elif "A" <= i <= "M":
            encrypted_i = shift_character(
                i, -shift1, "A", 13
            )

        elif "N" <= i <= "Z":
            encrypted_i = shift_character(
                i, shift2 ** 2, "N", 13
            )

        elif "0" <= i <= "9":
            encrypted_i = shift_character(
                i, shift1 - shift2, "0", 10
            )

        else:
            encrypted_i = i

        encrypted_text += encrypted_i

    with open(output_path, "w") as f:
        f.write(encrypted_text)


shift1 = get_valid_shift_value("shift1")
shift2 = get_valid_shift_value("shift2")

def decrypt_file(shift1, shift2, input_path, output_path):

    with open(input_path, "r") as f:
        content = f.read()

    decrypted_text = ""

    for i in content:

        if "a" <= i <= "n":
            decrypted_i = shift_character(
                i, -(shift1 * shift2), "a", 14
            )

        elif "o" <= i <= "z":
            decrypted_i = shift_character(
                i, shift1 + shift2, "o", 12
            )

        elif "A" <= i <= "M":
            decrypted_i = shift_character(
                i, shift1, "A", 13
            )

        elif "N" <= i <= "Z":
            decrypted_i = shift_character(
                i, -(shift2 ** 2), "N", 13
            )

        elif "0" <= i <= "9":
            decrypted_i = shift_character(
                i, -(shift1 - shift2), "0", 10
            )

        else:
            decrypted_i = i

        decrypted_text += decrypted_i

    with open(output_path, "w") as f:
        f.write(decrypted_text)

def verify_files(original_path, decrypted_path):

    with open(original_path, "r") as f:
        original_content = f.read()

    with open(decrypted_path, "r") as f:
        decrypted_content = f.read()

    return original_content == decrypted_content
        
encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
decrypt_file(shift1, shift2, "encrypted_text.txt", "decrypted_text.txt")

if verify_files("raw_text.txt", "decrypted_text.txt"):
    print("Verification successful!")
else:
    print("Verification failed!")