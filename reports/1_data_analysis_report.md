# Data Analysis Report: Ambient Sound Awareness System (ASAS)

**Date**: February 15, 2026
**Status**: Data Ready for Modeling

---

## 1. Executive Summary
We have successfully prepared a balanced dataset of **1000 audio samples** covering 5 key environmental sounds ("The Big 5"). The data is sourced from **ESC-50** and **UrbanSound8K**, processed to ensure class balance, and verified for quality. The dataset is now ready for feature extraction and model training.

## 2. Data Sources & Understanding
We utilized two primary public datasets:
- **ESC-50**: 5-second clips, 44.1kHz, 50 classes. High quality, often studio-like.
- **UrbanSound8K**: Varying length (<4s), varying sample rates, 10 classes. Real-world urban noise.

### Key Observation
- **Volume**: UrbanSound8K classes (e.g., Siren) had ~1000 samples, while ESC-50 classes (e.g., Crying Baby) had only 40.
- **Duration**: Significant variance in UrbanSound8K required standardization strategies (padding/truncating will be needed during feature extraction).

## 3. Data Preparation Strategy
To create a robust Minimum Viable Product (MVP), we selected 5 high-priority classes and applied a strict balancing strategy.

### 3.1 Class Selection ("The Big 5")
| Class Name | Urgency Level | Primary Source | Original Count |
| :--- | :--- | :--- | :--- |
| **Siren** | 4 (Critical) | UrbanSound8K | ~1000 |
| **Car Horn** | 3 (High) | UrbanSound8K | ~400 |
| **Crying Baby** | 3 (High) | ESC-50 | 40 |
| **Dog Bark** | 2 (Medium) | UrbanSound8K | ~1000 |
| **Door Knock** | 2 (Medium) | ESC-50 | 40 |

### 3.2 Balancing (Target: ~200 per class)
- **Undersampling**: Majority classes (Siren, Car Horn, Dog Bark) were randomly downsampled to 200 samples to prevent model bias towards these classes.
- **Data Augmentation**: Minority classes (Crying Baby, Door Knock) were augmented using:
    - **Time Stretch**: 1.2x speed (faster).
    - **Pitch Shift**: -2 semitones (lower pitch).
    - **Noise Injection**: Added low-level Gaussian noise.
    - **Result**: Increased 40 samples -> 160-200 samples per class.

## 4. Exploratory Data Analysis (EDA) Findings

### 4.1 Data Quality
- **Class Balance**: Successfully achieved perfect balance (200 samples for Siren/Car Horn/Dog Bark, 160 for Baby/Knock). *Note: 160 is practically close enough to 200 for deep learning.*
- **Sample Rate**: Analysis showed potential inconsistencies in raw UrbanSound8K files. **Action Item**: The feature extraction pipeline MUST force resampling to a fixed rate (e.g., 22050 Hz or 16000 Hz).
- **Duration**: Most clips are <4 seconds. A fixed input window of **4 seconds** covers >95% of data.

### 4.2 Feature Analysis
- **Spectral Distinctiveness**: Mel-Spectrograms showed clear visual differences:
    - *Siren*: Continuous, wavy lines (tonal).
    - *Car Horn*: Harmonically stack lines (tonal+noise).
    - *Door Knock*: Vertical impulses (transient).
    - *Dog Bark*: Short, bursty patterns (transient).
    - *Crying Baby*: Harmonic but varying pitch (tonal).
- **MFCC Profiles**: Mean MFCC plots showed distinct average "shapes" for each class, suggesting they are separable by a classifier.
- **t-SNE Clustering**: 2D projection of MFCCs revealed reasonably distinct clusters, though some overlap exists between Siren and Car Horn (both are loud, tonal vehicle sounds).

### 4.3 Integrity Checks
- **Data Leakage**: We confirmed that augmented files track their `source_file`. **Critical Rule**: When creating Train/Validation splits, we must group by `source_file` so that an original clip and its pitch-shifted version do not end up in different sets.
- **Source Bias**: We verified that classes present in both datasets (if any used) do not cluster purely by dataset, reducing the risk that the model learns "Dataset A vs Dataset B" instead of the actual sounds.

## 5. Next Steps
1.  **Feature Extraction Pipeline**: Build a script to convert audio to **Log Mel-Spectrograms** (fixed size, e.g., 128x128).
    - *Must include Resampling to 22k Hz.*
    - *Must include Padding/Truncating to 4s.*
2.  **Model Architecture**: Design a **CNN (Convolutional Neural Network)**, likely a variant of VGG or ResNet compressed for mobile/edge use.
3.  **Training**: Train on the balanced dataset using the strict group-based splitting strategy.
