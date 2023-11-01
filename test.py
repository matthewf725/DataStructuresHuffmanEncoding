def print_file_bytes(file_path):
    try:
        with open(file_path, 'rb') as file:
            byte_data = file.read()
            hex_data = " ".join(f"{byte_data[i]:02X}" for i in range(len(byte_data)))
            print(hex_data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

print_file_bytes("file1_out.txt")

print_file_bytes("file1_soln.txt")
