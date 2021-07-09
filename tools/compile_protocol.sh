set -e

SELF_FOLDER=$(dirname "$0")
SRC_PATH="$SELF_FOLDER/../protocol"
DST_PATH="$SELF_FOLDER/../src/energytt/messages"

protoc -I="$SRC_PATH" --python_betterproto_out="$DST_PATH" "$SRC_PATH/measurements.proto"
protoc -I="$SRC_PATH" --python_betterproto_out="$DST_PATH" "$SRC_PATH/meteringpoints.proto"
protoc -I="$SRC_PATH" --python_betterproto_out="$DST_PATH" "$SRC_PATH/users.proto"
