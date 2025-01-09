import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 unpack-kngstn-ssd-fw.py input_firmware output_firmware")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # Open the input irmware file in binary mode
    with open(input_filename, 'rb') as f_in:
        data = f_in.read()

    # Check for the 'KINGSTON' signature at the beginning of the file
    if data[:8] != b'KINGSTON':
        print("Error: 'KINGSTON' signature not found at the beginning of the file.")
        sys.exit(1)

    key_length_byte = data[0x0E]
    start_key = data[0x0F]

    end_key = start_key + key_length_byte
    if len(data) < end_key:
        print("Error: File is too short to read the key.")
        sys.exit(1)
    key = data[start_key:end_key]

    # Read the body from position 0x10 + key_length_byte
    body = data[end_key:]
    if not body:
        print("Error: No body found after the key.")
        sys.exit(1)

    # Apply XOR operation to the body in blocks equal to the key length
    transformed_body = bytearray()
    for i in range(len(body)):
        transformed_byte = body[i] ^ key[i % key_length_byte]
        transformed_body.append(transformed_byte)

    # Save the transformed body to the output file
    with open(output_filename, 'wb') as f_out:
        f_out.write(transformed_body)

    print(f"Transformation complete. Output saved to '{output_filename}'.")

if __name__ == '__main__':
    main()
