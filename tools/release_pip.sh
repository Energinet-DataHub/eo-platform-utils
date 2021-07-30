# Releasimg PIP packages:
# https://packaging.python.org/tutorials/packaging-projects/
set -e

SELF_FOLDER=$(dirname "$0")
ROOT_PATH="$SELF_FOLDER/.."
DIST_PATH="$ROOT_PATH/dist"

echo $ROOT_PATH

rm -rf "$DIST_PATH/*"
python $ROOT/setup.py sdist --dev



python setup.py sdist --dev
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
