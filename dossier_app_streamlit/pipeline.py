from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# ------------------------------
# Variables catégorielles
# ------------------------------
cat_features = [
    'Network type subscription in Month 1', 
    'Network type subscription in Month 2', 
    'Most Loved Competitor network in in Month 1', 
    'Most Loved Competitor network in in Month 2'
]


class ImputeByIQR(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        """
        Cette méthode calcule les bornes IQR pour chaque variable quantitative.
        """
        # Sélection des colonnes quantitatives
        self.quant_columns = X.select_dtypes(include=[np.number]).columns
        
        # Calcul des bornes IQR pour chaque variable quantitative
        self.lower_bounds = {}
        self.upper_bounds = {}
        
        for col in self.quant_columns:
            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)
            IQR = Q3 - Q1
            self.lower_bounds[col] = Q1 - 1.5 * IQR
            self.upper_bounds[col] = Q3 + 1.5 * IQR
        
        return self

    def transform(self, X):
        """
        Cette méthode remplace les valeurs manquantes par la médiane dans les bornes IQR.
        """
        X = X.copy()
        
        # Imputation des valeurs manquantes par la médiane des données dans les bornes IQR
        for col in self.quant_columns:
            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = self.lower_bounds[col]
            upper_bound = self.upper_bounds[col]
            
            # Remplacer les valeurs manquantes (NaN) par la médiane des données dans les bornes IQR
            median_value = X[col].median()
            
            # Remplacer les NaN par la médiane pour chaque variable
            X[col] = X[col].fillna(median_value)
            
            # Traiter les valeurs qui sont en dehors des bornes IQR (si elles sont aberrantes)
            X[col] = np.clip(X[col], lower_bound, upper_bound)
        
        return X

# ------------------------------
# Étape 1 : Traitement des variables catégorielles
# ------------------------------
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
# Étape 2 : Traitement des variables quantitatives
# ------------------------------
class CleanColumnNames(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X.columns = X.columns.str.replace(" ", " ")
        return X




class CreateAdditionalFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # 1. Consistent competitor
        X['Consistent_competitor'] = (
            X['Most Loved Competitor network in in Month 1'] == 
            X['Most Loved Competitor network in in Month 2']
        ).astype(int)

        # 2. Network Upgrade
        def upgrade_status(row):
            m1, m2 = row['Network type subscription in Month 1'], row['Network type subscription in Month 2']
            if m1 == '2G' and m2 == '3G':
                return 1
            elif m1 == '3G' and m2 == '2G':
                return -1
            else:
                return 0
        X['Network_Upgrade'] = X.apply(upgrade_status, axis=1)

        # 3. Offnet/Onnet ratio
        if 'Total Offnet spend' in X.columns and 'Total Onnet spend' in X.columns:
            ratio_offnet = X['Total Offnet spend'] / X['Total Onnet spend'].replace(0, np.nan)
            max_offnet = ratio_offnet[ratio_offnet.notna()].max()
            X['Offnet_Onnet_ratio'] = ratio_offnet.fillna(max_offnet)

        # 4. SMS/Data ratio
        if 'Total SMS Spend' in X.columns and 'Total Data Spend' in X.columns:
            ratio_sms_data = X['Total SMS Spend'] / X['Total Data Spend'].replace(0, np.nan)
            max_sms_data = ratio_sms_data[ratio_sms_data.notna()].max()
            X['SMS_Data_ratio'] = ratio_sms_data.fillna(max_sms_data)

        return X


class CreateRatios(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X = X.copy()
        base = "Total Spend in Months 1 and 2 of 2017"
        variables = [
            "Total SMS Spend", 
            "Total Data Spend", 
            "Total Unique Calls", 
            "Total Onnet spend", 
            "Total Offnet spend"
        ]
        variables_suppr = ['network_age']
        for var in variables:
            if var in X.columns:
                X[f"{var}_ratio"] = X[var] / X[base].replace(0, np.nan)
        X.drop(columns=variables + variables_suppr, inplace=True, errors='ignore')
        return X

class ScaleQuantVars(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.scaler = MinMaxScaler()

    def fit(self, X, y=None):
        self.columns = X.select_dtypes(include=[np.number]).columns
        self.scaler.fit(X[self.columns])
        return self

    def transform(self, X):
        X = X.copy()
        X[self.columns] = self.scaler.transform(X[self.columns])
        return X



# ------------------------------
# Étape 3 : Pipeline global
# ------------------------------
class FullPreprocessingPipeline(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.cat_pipeline = Pipeline([
            ('imputer', CustomCategoricalImputer()),
            ('freq_encoder', FrequencyEncoder())
        ])
        self.quant_pipeline = Pipeline([
            ('imputer', ImputeByIQR()),
            ("clean_columns", CleanColumnNames()),
            ("add_features", CreateAdditionalFeatures()),
            ("create_ratios", CreateRatios()),
            ("scale_vars", ScaleQuantVars())
        ])

    def fit(self, X, y=None):
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
