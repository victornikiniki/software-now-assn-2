
def get_valid_shift_value(prompt: str) -> int:
    # Get a valid non-negative integer from the user
    while True:
        try:
            user_input = int(input(f"Enter {prompt}: "))

            if user_input >= 0:
                return user_input
            else:
                print("Please enter a non-negative integer")

        except ValueError:
            print("Please enter a non-negative integer")


def shift_character(
    character: str,
    shift: int,
    start_char: str,
    range_size: int
) -> str:
    # Shift the character by the specified amount, wrapping around within the specified range.

    position = ord(character) - ord(start_char)

    # Use modulo to wrap the shifted position back to the start of the range.
    new_position = (position + shift) % range_size

    new_ord = ord(start_char) + new_position
    return chr(new_ord)

def encrypt_file(
    shift1: int,
    shift2: int,
    input_path: str,
    output_path: str
) -> None:
    # Read the content of the input file, encrypt it using the specified shift values, and write the encrypted content to the output file.
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

def decrypt_file(
    shift1: int,
    shift2: int,
    input_path: str,
    output_path: str
) -> None:
    # Read the content of the input file, decrypt it using the specified shift values, and write the decrypted content to the output file.
    with open(input_path, "r") as f:
        content = f.read()

    decrypted_text = ""

    # Decryption reverses the direction of each encryption shift.
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

def verify_files(
    original_path: str,
    decrypted_path: str
) -> bool:
    # Compare the content of the original file and the decrypted file to verify if they are identical.
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