Multiple Disease Prediction (Diabetes, Heart, Kidney)

Overview
- End-to-end notebooks for predicting Diabetes, Heart Disease, and Chronic Kidney Disease (CKD).
- Includes data cleaning, EDA, feature engineering, model training (LR, KNN, SVM, DT, RF, GBDT, XGBoost) and evaluation.
- Slide deck for presentation: see docs/AI_Data_Science_Presentation.md

Project Structure
- dataset/ — CSV data
  - diabetes.csv, heart.csv, kidney_disease.csv
- notebooks/ — three Jupyter notebooks
  - Advance Project Diabetes Prediction Using ML.ipynb
  - Advance Project Heart Disease Prediction Using ML.ipynb
  - Advance Project Kidney Disease Prediction Using ML.ipynb
- saved_models/ — example exported models (e.g., diabetes.pkl)
- docs/AI_Data_Science_Presentation.md — concise talk track/slide deck
- requirements.txt — base deps (framework + streamlit)

Quickstart (Windows PowerShell)
1) Create and activate a virtual environment (recommended):
   powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2) Install dependencies:
   powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m pip install pandas numpy scikit-learn matplotlib seaborn plotly imbalanced-learn xgboost missingno statsmodels

3) Launch Jupyter:
   powershell
   python -m pip install jupyter
   jupyter notebook

4) Open a notebook in notebooks/ and run the first install cell if present:
   %pip install --quiet pandas numpy scikit-learn matplotlib seaborn plotly imbalanced-learn xgboost missingno statsmodels

Data Loading (paths)
- Notebooks are under notebooks/, datasets are under dataset/
- Paths are already fixed to read via Path from project root:
  from pathlib import Path
  root = Path.cwd().parent
  pd.read_csv(root / "dataset" / "diabetes.csv")
  pd.read_csv(root / "dataset" / "heart.csv")
  pd.read_csv(root / "dataset" / "kidney_disease.csv")

What’s in the Notebooks
1) Data description: df.info(), df.describe(), class distribution
2) EDA: histograms, boxplots, countplots, pairplots, KDE/violin; correlation heatmaps with df.corr(numeric_only=True)
3) Preprocessing: missing-value handling, categorical encoding (LabelEncoder/One-hot), scaling (Standard/Robust), optional outlier handling (IQR/LOF)
4) Models: Logistic Regression, KNN, SVM, Decision Tree, Random Forest, Gradient Boosting, XGBoost (+ basic GridSearch tuning)
5) Evaluation: Accuracy, Confusion Matrix, Precision/Recall/F1, ROC-AUC; ROC curves and comparison charts

Typical Results (illustrative)
- Diabetes: up to ~0.90–0.91 Accuracy with SVM/GBDT/XGB (split-dependent)
- Heart: RF ~0.82, DT tuned ~0.78, LR ~0.79 (split-dependent)
- Kidney: strong after cleaning; RF/GBDT/XGB often ≥0.96 (validate for overfitting)

Troubleshooting
- ModuleNotFoundError (e.g., xgboost, missingno): run the install cell or pip install those packages in your venv
- Seaborn API changes: use countplot with explicit keywords, e.g., sns.countplot(x='Outcome', data=df)
- NumPy 2.0: use np.nan instead of np.NaN
- Correlation with mixed dtypes: use df.corr(numeric_only=True)

Repro Tips
- Pin random_state where applicable for reproducibility
- Prefer Stratified K-Fold for robust validation on small medical datasets
- Consider SHAP/feature importance plots to explain models

License
- For academic use. Please cite appropriately if you use these notebooks.

# Multiple_Disease_Prediction