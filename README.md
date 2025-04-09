🚀 End-to-End ML Pipeline with Git, DVC, and Experiments
This guide walks you through setting up a full machine learning pipeline using Git, DVC, and DVC Live for experiment tracking.

📁 Initial Git Setup
Create a GitHub repository and clone it locally:

bash
Copy
Edit
git clone <repo-url>
cd <project-directory>
Add your src/ folder with all your pipeline components (run each script individually to test them).

Add the following folders to your .gitignore file:

text
Copy
Edit
data/
models/
reports/
Stage and push the initial files:

bash
Copy
Edit
git add .
git commit -m "Initial pipeline setup"
git push
⚙️ Setting Up DVC Pipeline (Without params.yaml)
Create a dvc.yaml file manually or by running individual stages using dvc stage add.

Initialize DVC and test the pipeline:

bash
Copy
Edit
dvc init
dvc repro
dvc dag  # to visualize the pipeline
Push DVC setup to Git:

bash
Copy
Edit
git add .
git commit -m "Add DVC pipeline"
git push
⚙️ Setting Up DVC Pipeline (With params.yaml)
Create a params.yaml file for pipeline configuration values.

Add the parameter loading function in your scripts (see code block below in params.yaml setup section).

Run the pipeline:

bash
Copy
Edit
dvc repro
Push all updates:

bash
Copy
Edit
git add .
git commit -m "Integrate params.yaml into DVC pipeline"
git push
🧪 Running Experiments with DVC
Install DVC Live:

bash
Copy
Edit
pip install dvclive
Add the DVC Live experiment logging code (provided below).

Run an experiment:

bash
Copy
Edit
dvc exp run
View your experiments:

bash
Copy
Edit
dvc exp show
Or use the DVC Extension in VSCode for a UI.

Manage experiments:

bash
Copy
Edit
dvc exp remove <exp-name>     # optional
dvc exp apply <exp-name>      # apply a previous experiment
Change values in params.yaml and re-run:

bash
Copy
Edit
dvc exp run
Commit your experiment tracking:

bash
Copy
Edit
git add .
git commit -m "Track DVC experiments"
git push
📄 params.yaml Setup
1. Import yaml
python
Copy
Edit
import yaml
2. Define a function to load parameters
python
Copy
Edit
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
3. Use the params inside main() as needed
python
Copy
Edit
# data_ingestion
params = load_params('params.yaml')
test_size = params['data_ingestion']['test_size']

# feature_engineering
max_features = params['feature_engineering']['max_features']

# model_building
model_params = params['model_building']
📊 DVC Live Code Block (for Experiment Tracking)
1. Import modules
python
Copy
Edit
from dvclive import Live
import yaml
2. Load parameters using load_params() and define params
3. Add DVC Live block to main()
python
Copy
Edit
with Live(save_dvc_exp=True) as live:
    live.log_metric('accuracy', accuracy_score(y_test, y_test))
    live.log_metric('precision', precision_score(y_test, y_test))
    live.log_metric('recall', recall_score(y_test, y_test))

    live.log_params(params)
🎉 You're now ready to build, automate, and track experiments in your ML pipeline using Git + DVC + DVC Live!