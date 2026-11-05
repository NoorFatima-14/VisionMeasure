
import argparse
import json
import sys

import cv2
import numpy as np

CARD_LONG_MM = 85    
CARD_SHORT_MM = 54
MAX_SCALE_MISMATCH = 0.03
BORDER_PX = 5
MIN_AREA_FRACTION = 0.005


def find_blobs(image):
    """Return the two largest blobs that differ from the table colour."""
    lab = cv2.cvtColor(cv2.GaussianBlur(image, (7, 7), 0), cv2.COLOR_BGR2LAB).astype(np.float32)
    frame = np.concatenate([lab[:20].reshape(-1, 3), lab[-20:].reshape(-1, 3),
                            lab[:, :20].reshape(-1, 3), lab[:, -20:].reshape(-1, 3)])
    distance = np.linalg.norm(lab - np.median(frame, axis=0), axis=2)
    distance = cv2.normalize(distance, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    _, mask = cv2.threshold(distance, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel), cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    minimum = MIN_AREA_FRACTION * image.shape[0] * image.shape[1]
    big = [c for c in contours if cv2.contourArea(c) > minimum]
    return sorted(big, key=cv2.contourArea, reverse=True)[:2]


def rect_sides(contour):
    (_, _), (a, b), _ = rect = cv2.minAreaRect(contour)
    return max(a, b), min(a, b), cv2.boxPoints(rect)


def touches_border(contour, shape):
    x, y, w, h = cv2.boundingRect(contour)
    return x < BORDER_PX or y < BORDER_PX or x + w > shape[1] - BORDER_PX or y + h > shape[0] - BORDER_PX


def mm_per_pixel(card_long_px, card_short_px):
    """THE pixels-to-millimetres conversion: known card size / measured card size.
    Valid only if card and wallet are in the same plane and the camera looks
    straight at that plane. Returns the scale and how much the two sides disagree."""
    along_long = CARD_LONG_MM / card_long_px
    along_short = CARD_SHORT_MM / card_short_px
    mean = (along_long + along_short) / 2
    return mean, abs(along_long - along_short) / mean


def measure(image):
    blobs = find_blobs(image)
    if len(blobs) < 2:
        return {"status": "refused", "reason": "object_or_reference_not_found"}, []
    wallet, card = blobs  # the wallet is the larger of the two
    if touches_border(wallet, image.shape) or touches_border(card, image.shape):
        return {"status": "refused", "reason": "object_touches_frame_edge"}, []
    card_long, card_short, card_box = rect_sides(card)
    wallet_long, wallet_short, wallet_box = rect_sides(wallet)
    scale, mismatch = mm_per_pixel(card_long, card_short)
    if mismatch > MAX_SCALE_MISMATCH:
        return {"status": "refused", "reason": "reference_scale_mismatch",
                "scale_mismatch": round(mismatch, 4)}, []
    result = {"status": "ok", "width_mm": round(wallet_long * scale, 2),
              "height_mm": round(wallet_short * scale, 2), "mm_per_px": round(scale, 5),
              "scale_mismatch": round(mismatch, 4)}
    return result, [wallet_box, card_box]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    image = cv2.imread(args.image)
    if image is None:
        sys.exit(f"cannot read image: {args.image}")
    result, boxes = measure(image)
    overlay = image.copy()
    for box in boxes:
        cv2.polylines(overlay, [box.astype(np.int32)], True, (0, 255, 0), 4)
    text = (f"{result['width_mm']} x {result['height_mm']} mm" if result["status"] == "ok"
            else f"REFUSED: {result['reason']}")
    cv2.putText(overlay, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 0), 7)
    cv2.putText(overlay, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 255, 255), 3)
    cv2.imwrite(args.out, overlay)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "ok" else 3)


if __name__ == "__main__":
    main()
