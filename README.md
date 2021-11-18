# origin-protocol
Protocol Descriptions

## Protocol Buffers installation:
https://grpc.io/docs/protoc-installation/




## Uploading package manually

First the package has to be built:

    python setup.py install

The install command is used, because for unknown reasons the build currently does not generate the ./dist folder

Next the package must be uploaded to pypi

    python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

