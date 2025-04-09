
# 🚀 End-to-End ML Pipeline with Git, DVC, and Experiments

This guide walks you through setting up a full machine learning pipeline using Git, DVC, and DVC Live for experiment tracking.

---

## 📁 Initial Git Setup

1. **Create a GitHub repository** and clone it locally:

   ```bash
   git clone <repo-url>
   cd <project-directory>
   ```

2. Add your `src/` folder with all your pipeline components (run each script individually to test them).

3. Add the following folders to your `.gitignore` file:

   ```text
   data/
   models/
   reports/
   ```

4. Stage and push the initial files:

   ```bash
   git add .
   git commit -m "Initial pipeline setup"
   git push
   ```

---

## ⚙️ Setting Up DVC Pipeline (Without `params.yaml`)

5. Create a `dvc.yaml` file manually or by running individual stages using `dvc stage add`.

6. Initialize DVC and test the pipeline:

   ```bash
   dvc init
   dvc repro
   dvc dag  # to visualize the pipeline
   ```

7. Push DVC setup to Git:

   ```bash
   git add .
   git commit -m "Add DVC pipeline"
   git push
   ```

---

## ⚙️ Setting Up DVC Pipeline (With `params.yaml`)

8. Create a `params.yaml` file for pipeline configuration values.

9. Add the parameter loading function in your scripts (see code block below in `params.yaml setup` section).

10. Run the pipeline:

    ```bash
    dvc repro
    ```

11. Push all updates:

    ```bash
    git add .
    git commit -m "Integrate params.yaml into DVC pipeline"
    git push
    ```

---

## 🧪 Running Experiments with DVC

12. Install DVC Live:

    ```bash
    pip install dvclive
    ```

13. Add the **DVC Live** experiment logging code (provided below).

14. Run an experiment:

    ```bash
    dvc exp run
    ```

15. View your experiments:

    ```bash
    dvc exp show
    ```

    Or use the **DVC Extension** in VSCode for a UI.

16. Manage experiments:

    ```bash
    dvc exp remove <exp-name>     # optional
    dvc exp apply <exp-name>      # apply a previous experiment
    ```

17. Change values in `params.yaml` and re-run:

    ```bash
    dvc exp run
    ```

18. Commit your experiment tracking:

    ```bash
    git add .
    git commit -m "Track DVC experiments"
    git push
    ```

---

## 📄 `params.yaml` Setup

### 1. Import `yaml`

```python
import yaml
```

### 2. Define a function to load parameters

```python
def load_params(params_path: str) -> dict:
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logger.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logger.error('YAML error: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error: %s', e)
        raise
```

### 3. Use the `params` inside `main()` as needed

```python
# data_ingestion
params = load_params('params.yaml')
test_size = params['data_ingestion']['test_size']

# feature_engineering
max_features = params['feature_engineering']['max_features']

# model_building
model_params = params['model_building']
```

---

## 📊 DVC Live Code Block (for Experiment Tracking)

### 1. Import modules

```python
from dvclive import Live
import yaml
```

### 2. Load parameters using `load_params()` and define `params`

### 3. Add DVC Live block to `main()`

```python
with Live(save_dvc_exp=True) as live:
    live.log_metric('accuracy', accuracy_score(y_test, y_test))
    live.log_metric('precision', precision_score(y_test, y_test))
    live.log_metric('recall', recall_score(y_test, y_test))

    live.log_params(params)
```

---

🎉 **You're now ready to build, automate, and track experiments in your ML pipeline using Git + DVC + DVC Live!**
