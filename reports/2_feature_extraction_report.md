# Feature Extraction Report

**Date**: February 17, 2026
**Notebook**: `notebooks/5_feature_extraction.ipynb`
**Status**: Success

---

## 1. Execution Summary
The feature extraction pipeline was executed on the balanced dataset combined from ESC-50 and UrbanSound8K. All audio files were processed using the strict standardized pipeline:
`Load` -> `Resample (22050)` -> `Fix Duration (2s)` -> `MelSpec (128)` -> `Log` -> `Norm` -> `Tensor`

## 2. Results Analysis

### 2.1 Output Dimensions
- **Final Tensor Shape (`X`)**: `(920, 1, 128, 87)`
    - **920**: Total samples (Successfully processed 100% of the dataset).
    - **1**: Channel dimension (Mono).
    - **128**: Mel frequency bins (Height).
    - **87**: Time frames (Width, corresponding to 2 seconds).
- **Labels Shape (`y`)**: `(920,)`

### 2.2 Statistical Validation
| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **Mean** | `~ 0` (`-4.92e-09`) | **Perfect**. Centered at zero. |
| **Std Dev** | `1.0` | **Perfect**. Unit variance. |
| **Min Value** | `-5.18` | Normal Z-score range. |
| **Max Value** | `7.79` | Normal Z-score range. |

### 2.3 Integrity Checks
- **NaNs**: `False` (0 found).
- **Silent Audio**: No files resulted in errors or zero-variance (which would cause normalization NaNs).

## 3. Conclusion
The data is **fully standardized and normalized**. The shape `(Batch, Channel, Freq, Time)` is compatible with standard 2D CNN architectures (like VGG, ResNet, or custom CNNs) available in PyTorch or TensorFlow.

**Next Step**: Proceed to **Model Training**.
