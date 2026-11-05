# Plan

Written at the start, with 1 hour left of the 24 hours. I cannot finish the full task, so I chose a reduced version and honestly submitting the things that are done yet.

## What I will do
Measure my wallet's width and height in mm from a photo, with a bank card in the same photo as the scale, and check the result against a calliper.

- Object: my wallet. Reference: a bank card.
- Photos: due to the shortage of time i managed to create photos from chatgpt.
- Method: `measure.py` separates both objects from the table by colour, fits a rotated rectangle to each, and converts pixels to mm using the card (mm per pixel = known card size / measured card size).
- Check: `accuracy.py` compares the output with calliper readings.

## Known risks
- As currently the pictures are AI generated so, I expect a small over measurement.


