import os
import shutil

ARCHIVE = "archive"
OUT = "data"

MAX_SAMPLES = {
    "train": 1200,
    "test": 300
}

def normalize_label(raw):
    raw = raw.lower()
    if "positive" in raw or "covid" in raw:
        return "covid"
    if "negative" in raw or "normal" in raw:
        return "normal"
    return None

def prepare_split(split):
    label_file = os.path.join(ARCHIVE, f"{split}.txt")
    image_dir = os.path.join(ARCHIVE, split)

    selected = {"covid": 0, "normal": 0}

    with open(label_file, encoding="latin-1") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            # filename is always the second column
            fname = parts[1]
            label = normalize_label(parts[2])

            if label is None:
                continue

            if selected[label] >= MAX_SAMPLES[split]:
                continue

            src = os.path.join(image_dir, fname)
            if not os.path.exists(src):
                continue

            dst = os.path.join(OUT, split, label)
            os.makedirs(dst, exist_ok=True)

            shutil.copy(src, dst)
            selected[label] += 1

    print(f"✅ {split} done →", selected)

# RUN
prepare_split("train")
prepare_split("test")
