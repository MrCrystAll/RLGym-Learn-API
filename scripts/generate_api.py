"""The only reason this script exists is because npm link doesn't work reliably on windows"""

import json
import os
import re
import shutil
import subprocess
import sys


def normalize_version(version: str) -> str:
    return re.sub(r"\.([a-zA-Z]+)(\d+)$", r"-\1.\2", version)


if __name__ == "__main__":
    # Deleting existing generated stuff to avoid conflict
    print("Deleting directory...")
    try:
        shutil.rmtree("./client")
    except FileNotFoundError:
        pass

    # Creating the schema using fastAPI
    print("Creating schema...")
    subprocess.call([sys.executable, os.path.join(__file__, "..", "export_openapi.py")])

    # Extract the version and transform it from, for example "0.1.5.dev2" (python notation) to "0.1.5-dev.2" (node notation)
    with open("openapi.json", "r") as f:
        _version = normalize_version(json.loads(f.read())["info"]["version"])

    # Generate using openapi client
    print(f"Generating package version {_version}")
    os.system(
        f"npx @openapitools/openapi-generator-cli generate -i \
        openapi.json -g typescript-axios -o client/ \
        -c typescript-axios-config.yaml --additional-properties npmVersion={_version}"
    )

    # Packing using npm
    print(f"Creating .tgz package {_version}")
    os.system("cd client && npm i && npm pack")

    # Should output something like "rlgym-learn-client-{version}.tgz", installable locally
