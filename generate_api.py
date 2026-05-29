import os
import shutil
import subprocess
import sys

if __name__ == "__main__":
    print("Deleting directory...")
    try:
        shutil.rmtree("./client")
    except (FileNotFoundError, PermissionError):
        pass
    print("Generating")
    subprocess.call([sys.executable, "scripts\\export_openapi.py"])
    os.system(
        "npx @openapitools/openapi-generator-cli generate -i \
        openapi.json -g typescript-axios -o client/ \
        -c typescript-axios-config.yaml"
    )
    print("Creating .tgz package")
    os.system("cd client && npm i && npm pack")
