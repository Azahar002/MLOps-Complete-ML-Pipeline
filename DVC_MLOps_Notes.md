
# 📦 DVC (Data Version Control) - MLOps Notes

## 🔹 What is DVC?
DVC is an open-source tool for data & model versioning, pipeline management, and reproducibility in machine learning projects. It complements Git by tracking large files, data sets, models, and experiments.

---

## 🔹 Key Features
- **Data Versioning**: Track changes to datasets and model files like Git tracks source code.
- **Experiment Tracking**: Save experiment configurations and results.
- **Pipeline Management**: Create reproducible ML pipelines using DVC stages.
- **Storage Agnostic**: Supports remote storage (S3, GCS, Azure Blob, etc.).
- **Collaboration**: Teams can share data and models without storing them in Git.

---

## 🔹 Core DVC Commands

### 📁 Initialize DVC
```bash
dvc init
```

### 📂 Add Data/Model for Tracking
```bash
dvc add data/train.csv
```

### 💾 Commit Changes to Git
```bash
git add data/train.csv.dvc .gitignore
git commit -m "Add training data"
```

### 🔄 Setup Remote Storage
```bash
dvc remote add -d myremote s3://mybucket/path
dvc push  # Pushes data to remote
```

### 📈 Track Experiments
```bash
dvc exp run
dvc exp show
```

---

## 🔹 DVC Pipeline
Define steps of your ML workflow in `dvc.yaml`.

### 🛠 Example
```yaml
stages:
  preprocess:
    cmd: python preprocess.py
    deps:
      - data/raw.csv
    outs:
      - data/clean.csv

  train:
    cmd: python train.py
    deps:
      - data/clean.csv
    outs:
      - model.pkl
```

---

## 🔹 Use Cases
- Version control for datasets and models
- Reproducible pipelines
- Efficient experiment tracking
- Seamless collaboration in teams

---

## 🔹 Integrations
- **Git**: For code versioning
- **MLflow**: For experiment tracking
- **DagsHub**: For hosted DVC repositories
