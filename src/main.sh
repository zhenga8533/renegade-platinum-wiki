# Set the current working directory to the directory of the script
cd "$(dirname "$0")"

# Check for .env file
if [ -f .env ]; then
  echo ".env file found"
else
  echo "Creating .env file"
  cp ../.env.example .env
  echo ".env file created"
fi
echo ""


# Check for i/o paths
echo "Checking for i/o paths"
OVERWRITE=$(grep "^OVERWRITE" .env | cut -d '=' -f2- | tr -d ' "')
OUTPUT_PATH=$(grep "^OUTPUT_PATH" .env | cut -d '=' -f2- | tr -d ' "')
NAV_OUTPUT_PATH=$(grep "^NAV_OUTPUT_PATH" .env | cut -d '=' -f2- | tr -d ' "')
POKEMON_INPUT_PATH=$(grep "^POKEMON_INPUT_PATH" .env | cut -d '=' -f2- | tr -d ' "')
WILD_ENCOUNTER_PATH=$(grep "^WILD_ENCOUNTER_PATH" .env | cut -d '=' -f2- | tr -d ' "')

rm -rf $OUTPUT_PATH
rm -rf $NAV_OUTPUT_PATH
rm -rf $WILD_ENCOUNTER_PATH
if [ -d $POKEMON_INPUT_PATH ]; then
  echo "Pokemon input data found"
else
  echo "Pokemon input data not found"
  echo "Please use the following link to download the data:"
  echo "https://github.com/zhenga8533/pokeapi-parser/tree/v1"
fi
echo ""


# Check if "python" is available and is version 3
if command -v python &> /dev/null && [[ $(python -c "import sys; print(sys.version_info.major)" 2>/dev/null) == "3" ]]; then
    PYTHON="python"
    PIP="pip"
# Check if "python3" is available and is version 3
elif command -v python3 &> /dev/null && [[ $(python3 -c "import sys; print(sys.version_info.major)" 2>/dev/null) == "3" ]]; then
    PYTHON="python3"
    PIP="pip3"
else
    echo "No compatible Python 3 interpreter found."
    exit 1
fi
echo "Using $PYTHON"
echo ""


# Install requirements
if [ -f ../requirements.txt ]; then
  $PIP install -r ../requirements.txt
  echo "Requirements installed"
else
  echo "No requirements file found"
fi
echo ""


# Run all parsers
echo "Running all parsers"
$PYTHON evolution_changes.py
$PYTHON item_changes.py
$PYTHON move_changes.py
$PYTHON pokemon_changes.py
$PYTHON special_events.py
$PYTHON trainer_pokemon.py
$PYTHON type_changes.py
$PYTHON wild_pokemon.py
echo "Finished running all parsers"
echo ""

# Give option to update markdown files
if ! [[ $OVERWRITE == "True" ]]; then
  echo "Markdown files not updated"
  exit 0
fi

echo "Updating Markdown files in docs"

mkdir -p ../docs/mechanics
mkdir -p ../docs/pokemon
mkdir -p ../docs/wild_encounters

# Check for rsync
if ! command -v rsync &> /dev/null; then
  cp -r -f -u $OUTPUT_PATH/* ../docs/mechanics
  cp -r -f -u $WILD_ENCOUNTER_PATH/* ../docs/wild_encounters
else
  rsync -av --update $OUTPUT_PATH/ ../docs/mechanics
  rsync -av --update $WILD_ENCOUNTER_PATH/ ../docs/wild_encounters
fi
echo "Markdown files updated"
