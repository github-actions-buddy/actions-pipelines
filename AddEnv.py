import os

env_file_path = ".env.devci"
github_env_file = os.getenv('GITHUB_ENV')

existing_keys = set()

try:
    with open(env_file_path, 'r') as file:
        with open(github_env_file, 'a') as env_file:
            for line in file:
                line = line.strip()
                if line.startswith("export "):
                    line = line[len("export "):]
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"')
                        if key in existing_keys:
                            print(f"Duplicate variable found: {key}")
                            exit(1)
                        else:
                            existing_keys.add(key)
                            env_file.write(f"{key}={value}\n")

except FileNotFoundError:
    print(f"Error: File {env_file_path} not found.")
    exit(1)

except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
