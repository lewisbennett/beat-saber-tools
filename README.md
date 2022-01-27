# beat-saber-tools
Not an in-game mod, just simple tools for Beat Saber.

## [Custom Level Verifier](https://github.com/lewisbennett/beat-saber-tools/tree/master/custom_level_verifier)

Verifies that your custom levels exist on [Beat Saver](https://beatsaver.com/) by computing their hashes and quering the Beat Saver download link (`https://eu.cdn.beatsaver.com/[level hash].zip`). It will print the custom level's folder name if it does not exist, and give you the option to export both successful and failed queries to `.txt` files at the end, which include the levels' folder names and the levels' hash.

### Usage

`python custom_level_verifier.py [Beat Saber CustomLevels directory]`
