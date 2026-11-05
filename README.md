# Measure It 

Measures my wallet's width and height in mm from one photo. A bank card in the same photo is the scale.

**This is an unfinished submission.** Done: a colour-based measurement command and an accuracy check against a calliper. Not done: camera calibration, labelled dataset, trained model, items 6 to 10. See `docs/definition_of_done.md`.


## Setup and run
```bash
pip install -r requirements.txt
python measure.py --image photos/photo_1.jpg --out results/photo_1.jpg   
python accuracy.py --truth ground_truth.csv --photos photos              
```
`measure.py` exits with 0 when it reports a measurement and 3 when it refuses (wallet or card not found, touching the frame edge, or the card looks distorted).

## Dataset summary
No training dataset. photos are generated `photos/`, measured by a online scale `ground_truth.csv`.
