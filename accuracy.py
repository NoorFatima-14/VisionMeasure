"""Compare measure.py with your calliper readings.

    python accuracy.py --truth ground_truth.csv --photos photos
ground_truth.csv columns: image,width_mm,height_mm
"""
import argparse
import csv
from pathlib import Path

import cv2
import numpy as np

from measure import measure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--truth", required=True)
    parser.add_argument("--photos", required=True)
    args = parser.parse_args()

    errors, percents = [], []
    print("| image | calliper W x H | system W x H | abs error W / H (mm) |\n|---|---|---|---|")
    for row in csv.DictReader(open(args.truth)):
        truth = (float(row["width_mm"]), float(row["height_mm"]))
        result, _ = measure(cv2.imread(str(Path(args.photos, row["image"]))))
        if result["status"] != "ok":
            print(f"| {row['image']} | {truth[0]} x {truth[1]} | refused: {result['reason']} | - |")
            continue
        got = (result["width_mm"], result["height_mm"])
        diff = [abs(g - t) for g, t in zip(got, truth)]
        errors += diff
        percents += [100 * d / t for d, t in zip(diff, truth)]
        print(f"| {row['image']} | {truth[0]} x {truth[1]} | {got[0]} x {got[1]} | {diff[0]:.2f} / {diff[1]:.2f} |")
    if errors:
        print(f"\nMAE {np.mean(errors):.2f} mm | median {np.median(errors):.2f} mm | "
              f"worst {np.max(errors):.2f} mm | mean % error {np.mean(percents):.2f}%")


if __name__ == "__main__":
    main()
