import os

env_file_path = ".env.devci"
existing_keys = set()

try:
    with open(env_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                if key in existing_keys:
                    print(f"Duplicate variable found: {key}")
                    exit(1)
                else:
                    existing_keys.add(key)
                    print(f'echo "{key}={value}" >> "$GITHUB_ENV"')

except FileNotFoundError:
    print(f"Error: File {env_file_path} not found.")
    exit(1)

except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
