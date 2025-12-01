import joblib
import json
import pandas as pd
import os
import numpy as np
from typing import Dict, Any

from app.core.interfaces import IModelService
from app.core.entities import LoanApplication, PredictionResults

#implement
class CatBoostAdapter(IModelService):
    def __init__(self, artifacts_dir:str):
        #constructor method sayesinde nesenin attribute yani özelliklerini oluşturuyoruz
        # aşagidakileri yazmamizin sebebi su modeli falan bir kez yuklemek
        #bir tane catboostadapter nesnesi oluşsun ve predict methoduyla defalaraca aynı model üstünden sorgu yapılsın
        #adapter = catbootstadapter adapter.predict gibi düşün ve içine süekli parametre yazdığını
        self.artifacts_dir = artifacts_dir
        print(f"model dosyaları yükleniyor {artifacts_dir}")
    
        # 1. Modeli Yükle
        model_path = os.path.join(artifacts_dir, "final_catboost_model.pkl")
        self.model = joblib.load(model_path)
        
        # 2. Config Yükle Eşik değeri burada
        config_path = os.path.join(artifacts_dir, "config.json")
        with open(config_path, "r") as f:
            self.config = json.load(f)
            self.threshold = self.config.get("threshold", 0.5) # Bulamazsa 0.5 kullan
            
        # 3. Feature Listesini Yükle Reindex için şart
        features_path = os.path.join(artifacts_dir, "features.json")
        with open(features_path, "r") as f:
            self.feature_names = json.load(f)
            
        # 4. Mapping Kurallarını Yükle
        mappings_path = os.path.join(artifacts_dir, "mappings.json")
        with open(mappings_path, "r") as f:
            self.mappings = json.load(f)

    def _preprocess(self, application: LoanApplication) -> pd.DataFrame:
        """
        Gelen tekil başvuru verisini, modelin anlayacağı DataFrame formatına çevirir.
        Kaggle'daki işlemlerin aynısı burada uygulanır.
        """
        # Entity sınıfını sözlüğe, sonra DataFrame'e çevir
        # dataclasses.asdict() kullanılabilir ama manuel mapping daha güvenlidir
        data = {
            "annual_income": [application.annual_income],
            "debt_to_income_ratio": [application.debt_to_income_ratio],
            "credit_score": [application.credit_score],
            "loan_amount": [application.loan_amount],
            "interest_rate": [application.interest_rate],
            "gender": [application.gender],
            "marital_status": [application.marital_status],
            "employment_status": [application.employment_status],
            "loan_purpose": [application.loan_purpose],
            "education_level": [application.education_level],
            "grade_subgrade": [application.grade_subgrade]
        }

        
        df=pd.DataFrame(data)
        
        df["education_level"]=df["education_level"].map(self.mappings["education_map"])
        df["grade_subgrade"]=df["grade_subgrade"].map(self.mappings["grade_map"])
        obj_cols =df.select_dtypes(include=['object']).columns.to_list()

        df=pd.get_dummies(
            df,
            columns=obj_cols,
            dtype=int,
            drop_first=False
        )
        
        df=df.reindex(columns=self.feature_names,fill_value=0)
        return df
    def predict(self, application:LoanApplication)->PredictionResults:
        processed_df= self._preprocess(application)
        prob=self.model.predict_proba(processed_df)[0][1]
        if prob>self.threshold:
            decision="ONAY"
        else:
            decision="RED"
        return PredictionResults(
            probability=prob,
            decision=decision,
            threshold_used=self.threshold 
        )

        
    
