# ------------------------------
# 1. Pipeline catégoriel 
# ------------------------------

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin

cat_features = ['NetworktypesubscriptioninMonth1', 
                'NetworktypesubscriptioninMonth2', 
                'MostLovedCompetitornetworkininMonth1', 
                'MostLovedCompetitornetworkininMonth2']

class CustomCategoricalImputer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.most_frequent_1 = X[cat_features[0]].mode()[0]
        self.most_frequent_2 = X[cat_features[1]].mode()[0]
        self.most_frequent_comp_1 = X[cat_features[2]].mode()[0]
        self.most_frequent_comp_2 = X[cat_features[3]].mode()[0]
        return self

    def transform(self, X):
        X = X.copy()
        for col in cat_features[2:]:
            X[col].replace('0', 'Aucun', inplace=True)
            X[col].fillna('Aucun', inplace=True)

        mask1 = X[cat_features[0]].isna() & X[cat_features[1]].notna()
        mask2 = X[cat_features[1]].isna() & X[cat_features[0]].notna()
        X.loc[mask1, cat_features[0]] = X.loc[mask1, cat_features[1]]
        X.loc[mask2, cat_features[1]] = X.loc[mask2, cat_features[0]]

        X[cat_features[0]].fillna(self.most_frequent_1, inplace=True)
        X[cat_features[1]].fillna(self.most_frequent_2, inplace=True)
        X[cat_features[2]].fillna(self.most_frequent_comp_1, inplace=True)
        X[cat_features[3]].fillna(self.most_frequent_comp_2, inplace=True)
        return X

class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.freq_maps = {col: X[col].value_counts(normalize=True).to_dict() for col in cat_features}
        return self

    def transform(self, X):
        X = X.copy()
        for col in cat_features:
            X[col] = X[col].map(self.freq_maps[col])
        return X
    

# ------------------------------
# 2. Pipeline quantitatif
# ------------------------------

class CleanColumnNames(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X.columns = X.columns.str.replace(" ", "")
        return X

class FixADF1623(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = X.copy()
        mask = X["CustomerID"] == "ADF1623"
        for col in ["network_age", "Customertenureinmonth"]:
            if col in X.columns:
                X.loc[mask, col] = X.loc[mask, col].abs()
        return X

class RemoveNegNetworkAgeExceptADF1623(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[(X["CustomerID"] == "ADF1623") | (X["network_age"] >= 0)].copy()

class CreateRatios(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = X.copy()
        base = "TotalSpendinMonths1and2of2017"
        variables = [
            "TotalSMSSpend", 
            "TotalDataSpend", 
            "TotalUniqueCalls", 
            "TotalOnnetspend", 
            "TotalOffnetspend"
        ]
        variables_suppr=['CustomerID','network_age']
        for var in variables:
            if var in X.columns:
                X[f"{var}_ratio"] = X[var] / X[base].replace(0, np.nan)
        X.drop(columns=variables + [base]+variables_suppr, inplace=True, errors='ignore')
        return X

class ScaleQuantVars(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.scaler = MinMaxScaler()
    def fit(self, X, y=None):
        self.columns = X.select_dtypes(include=[np.number]).columns.difference(["ChurnStatus"])
        self.scaler.fit(X[self.columns])
        return self
    def transform(self, X):
        X = X.copy()
        X[self.columns] = self.scaler.transform(X[self.columns])
        return X

# ------------------------------
# 3. Full Preprocessing Pipeline
# ------------------------------

class FullPreprocessingPipeline(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.cat_pipeline = Pipeline([
            ('imputer', CustomCategoricalImputer()),
            ('freq_encoder', FrequencyEncoder())
        ])
        self.quant_pipeline = Pipeline([
            ("clean_columns", CleanColumnNames()),
            ("fix_adf1623", FixADF1623()),
            ("remove_neg_network_age", RemoveNegNetworkAgeExceptADF1623()),
            ("create_ratios", CreateRatios()),
            ("scale_vars", ScaleQuantVars())
        ])

    def fit(self, X, y=None):
        # Appliquer pipeline quanti pour nettoyage colonnes + suppression lignes
        X_clean = self.quant_pipeline.fit_transform(X.copy())
        self.cat_pipeline.fit(X_clean[cat_features])
        return self
    

    def transform(self, X):
        X = self.quant_pipeline.transform(X.copy())
        X_cat = self.cat_pipeline.transform(X[cat_features])
        X[cat_features] = X_cat
        return X

# ------------------------------
# Utilisation
# ------------------------------

pipeline = FullPreprocessingPipeline()
# df_final = pipeline.fit_transform(df1)
# df_final.head()