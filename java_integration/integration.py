import subprocess

def addJAVA(fileName, *args):
    """Compile and run a Java program with multiple arguments."""
    # Remove the `.java` extension if it's included in the fileName
    if fileName.endswith(".java"):
        fileName = fileName[:-5]

    # Compile the Java file
    try:
        subprocess.run(['javac', f'{fileName}.java'], check=True)
    except subprocess.CalledProcessError as e:
        return f'Error compiling Java program: {e.stderr.strip()}'

    # Run the Java file
    try:
        result = subprocess.run(
            ['java', '-cp', '.', fileName] + list(map(str, args)),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f'Error executing Java program: {e.stderr.strip()}'

# Example usage
if __name__ == "__main__":
    print(addJAVA('AddNumbers', 10, 20))