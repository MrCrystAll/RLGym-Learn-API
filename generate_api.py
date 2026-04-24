import os


if __name__ == "__main__":
    print("Deleting directory...")
    os.system("rm -r client")
    print("Generating")
    os.system(
        "npx @openapitools/openapi-generator-cli generate -i \
        http://localhost:8000/openapi.json -g typescript-axios -o client/ \
        --additional-properties=npmName=rlgym-learn-client,withInterfaces=true,supportsES6=true"
    )
