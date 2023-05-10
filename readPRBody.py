import re
import sys
import os
import argparse

# Create an argument parser to parse the command line arguments
parser = argparse.ArgumentParser(description="Search for tests to be run in a text file.")
parser.add_argument("-s", "--source", type=str, required=True, help="the path to the text file to search")

# Parse the command line arguments
args = parser.parse_args()

# Try to open the text file and read its contents
try:
    with open(args.source, "r") as f:
        filetext = f.read()
        print(filetext)
except FileNotFoundError:
    raise FileNotFoundError(f"File not found: {args.source}")

# Define the regular expression pattern to match
pattern = r"testsToBeRun\s*([\w, \n]*)"

# Check if the file contents are empty
if not filetext:
    print("No match found.")
# If a match is found, print the contents of the capture group
else:
    # Search for the pattern in the text
    new_s = re.search(pattern, filetext)

    # If a match is found, print the contents of the capture group
    if new_s:
        test_names = new_s.group(1)
        print("\n")
        print("Group 1 of Unit tests from PR Body: " + test_names)
        test_names = re.sub(r",\s*", ",", test_names)  # Remove existing spaces after commas
        test_names = re.sub(r"[,\n]+", ", ", test_names)  # Replace commas and newlines with ", "
        test_names = re.sub(r", $", "", test_names)  # Remove trailing comma and space if present

        print("Number of unit tests: " + str(test_names.count(',') + 1))

        # Get environment file
        env_file = os.getenv('GITHUB_ENV')

        # Open and write test names into environment file
        with open(env_file, "w") as myfile:
            myfile.write('PR_TESTS'+'='+test_names+'\n')

        # Close the file
        f.close()
    else:
        print('There are no test class names found in PR Body')
        f.close()
