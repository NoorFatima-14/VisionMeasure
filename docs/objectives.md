# Objectives

All numbers come from my own runs of `accuracy.py`.

## MO-1: measurement accuracy

| Field | Entry |
|---|---|
| What is measured | Absolute error of wallet width and height versus my calliper reading. |
| How | `python accuracy.py --truth ground_truth.csv --photos photos` |
| Target | Mean absolute error <= <<FILL, e.g. 3>> mm. Why: <<FILL>>. |
| Conditions | Phone straight above, wallet and card flat on a plain table, both fully in frame, no undistortion. |
| Not included | Photos the system refuses (counted separately). |
| Result 
| image | calliper W x H | system W x H | abs error W / H (mm) |
|---|---|---|---|
| photo_1.jpg | 130.0 x 90.0 | 114.11 x 93.57 | 15.89 / 3.57 |
| photo_2.jpg | 130.0 x 90.0 | 116.33 x 100.87 | 13.67 / 10.87 |
| photo_3.jpg | 130.0 x 90.0 | 122.59 x 97.51 | 7.41 / 7.51 |
| photo_4.jpg | 130.0 x 90.0 | 122.58 x 104.03 | 7.42 / 14.03 |
| photo_5.jpg | 130.0 x 90.0 | 123.32 x 98.28 | 6.68 / 8.28 |

MAE 9.53 mm | median 7.90 mm | worst 15.89 mm | mean % error 8.85% |

## Not measured
Calibration error, model metrics and timing: not done.
