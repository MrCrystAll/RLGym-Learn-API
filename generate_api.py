import os
import shutil

if __name__ == "__main__":
    print("Deleting directory...")
    try:
        shutil.rmtree("./client")
    except (FileNotFoundError, PermissionError):
        pass
    print("Generating")
    os.system(
        "npx @openapitools/openapi-generator-cli generate -i \
        http://localhost:8000/openapi.json -g typescript-axios -o client/ \
        -c typescript-axios-config.yaml"
    )
    # print("Creating .tgz package")
    # os.system("cd client && npm i && npm pack")
