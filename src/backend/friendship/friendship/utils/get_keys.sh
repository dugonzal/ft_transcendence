# Generate RSA keys if they don't exist

# Store current working directory
CURRENT_DIR=$(pwd)

# Check if the environment variable is set
if [ -z "$MIGRATION_CONTAINER" ]; then
  echo "MIGRATION_CONTAINER is not set in the environment."
  # Set KEY_DIR to include the default directory
  KEY_DIR="/friendship/secrets"
else
  echo "MIGRATION_CONTAINER is set to: $MIGRATION_CONTAINER"
  # Set KEY_DIR to include the current directory
  KEY_DIR="$CURRENT_DIR/friendship/secrets"
fi

# Create the directory if it doesn't exist
mkdir -p "$KEY_DIR"

FRIENDSHIP_PUBLIC_KEY_PATH="$KEY_DIR/public.pem"

# Fetch public key from JWT Key Management Service
curl -o $FRIENDSHIP_PUBLIC_KEY_PATH http://auth/api/v1/auth/public
if ! openssl rsa -pubin -in $FRIENDSHIP_PUBLIC_KEY_PATH -text -noout >/dev/null 2>&1; then
  echo "Error: Fetched public key is not valid."
  exit 1
else
  echo "Private key fetched successfully"
fi