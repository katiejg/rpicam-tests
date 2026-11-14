## Running Scripts
- Cannot run more than one script at a time that uses the camera
  - Can run `diagnostic.py` in the background of any camera script
- Currently `star_tracker.py` captures an array and then captures a jpeg, one right after another
  - Ideally, we would capture the frame once and save it in the two formats -> developing now in `single-capture.py`

## Features to Add
- Enable arguments for `star_tracker.py`
  - exposure time
  - bool for preview window

## Bugs To Fix
- `image-formats.py` -> Syntax Error on line 85, expected 'except' or 'finally' block
