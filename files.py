def get_file_contents(file_path):
    """
    Reads the entire content of a specified file and returns it as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The entire content of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: For other input/output errors during file operations.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

# Example usage:
file_name = "my_document.txt"

# Create a sample file for demonstration
with open(file_name, 'w') as f:
    f.write("This is the first line.\n")
    f.write("This is the second line.\n")
    f.write("And this is the final line.")

file_content = get_file_contents(file_name)

if file_content is not None:
    print("File content:")
    print(file_content)

# Example with a non-existent file
non_existent_file = "non_existent.txt"
get_file_contents(non_existent_file)