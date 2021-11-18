# origin-protocol
Protocol Descriptions

## Protocol Buffers installation:
https://grpc.io/docs/protoc-installation/




## Uploading package manually

Steps to uploading package manually.
- Using pipenv first sync with development packages.
- Next build the tar.
- last upload it to pypi

Commands to run:

    pipenv sync -d 
    pipenv run build
    python run upload

