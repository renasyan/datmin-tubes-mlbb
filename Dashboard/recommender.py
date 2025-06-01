from random import sample
from itertools import combinations
from ast import literal_eval
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
import streamlit as st

# Global variables to cache model metrics
model_accuracy = None
model_roc_auc = None
model_cv_score = None
conf_matrix = None
trained_model = None
all_heroes = None
X_columns = None

def train_model():
    global model_accuracy, model_roc_auc, model_cv_score, conf_matrix, trained_model, all_heroes, X_columns

    df = pd.read_csv('results.csv')

    # Clean data
    df = df.drop(columns=[
        "Unnamed: 0", "file", "player", "ss_type", "opening_failure", "battle_id",
        "right_medals", "left_medals", "left_scores", "right_scores"
    ], errors='ignore')
    df['match_result'] = df['match_result'].map({'Victory': 1, 'Defeat': 0})
    df['left_heroes'] = df['left_heroes'].apply(literal_eval)
    df['right_heroes'] = df['right_heroes'].apply(literal_eval)

    # Remove outliers
    numerical_cols = df.select_dtypes(include=['number'])
    outlier_index = []
    for column in numerical_cols:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df.index[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]
        outlier_index.extend(outliers)
    df = df.drop(index=sorted(set(outlier_index)))

    # Data augmentation
    df_flip = df.copy()
    df_flip['left_heroes'], df_flip['right_heroes'] = df['right_heroes'], df['left_heroes']
    df_flip['match_result'] = 1 - df['match_result']
    df_all = pd.concat([df, df_flip], ignore_index=True)

    # One-hot encoding
    all_heroes = sorted(set(hero for row in pd.concat([df_all['left_heroes'], df_all['right_heroes']]) for hero in row))
    def encode(row):
        encoding = dict.fromkeys(['L_' + h for h in all_heroes] + ['R_' + h for h in all_heroes], 0)
        for h in row['left_heroes']:
            encoding['L_' + h] = 1
        for h in row['right_heroes']:
            encoding['R_' + h] = 1
        return pd.Series(encoding)

    X = df_all.apply(encode, axis=1)
    y = df_all['match_result']
    X_columns = X.columns

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Save model & metrics
    trained_model = model
    model_accuracy = accuracy_score(y_test, model.predict(X_test)) * 100
    model_roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]) * 100
    model_cv_score = cross_val_score(model, X, y, cv=5, scoring='accuracy').mean() * 100
    conf_matrix = confusion_matrix(y_test, model.predict(X_test))

def get_counter_heroes(hero1, hero2, hero3):
    global trained_model, all_heroes, X_columns
    if trained_model is None:
        train_model()

    enemy_heroes = [hero1, hero2, hero3]
    our_hero_pool = [h for h in all_heroes if h not in enemy_heroes]
    all_combos = list(combinations(our_hero_pool, 3))
    sample_combos = sample(all_combos, min(3000, len(all_combos)))

    input_data = []
    combos = []

    for combo in sample_combos:
        input_vec = dict.fromkeys(X_columns, 0)
        for h in enemy_heroes:
            col = 'R_' + h
            if col in input_vec:
                input_vec[col] = 1
        for h in combo:
            input_vec['L_' + h] = 1
        input_data.append(input_vec)
        combos.append(combo)

    input_df = pd.DataFrame(input_data)
    probs = trained_model.predict_proba(input_df)[:, 1]
    recommendations = list(zip(combos, probs))
    top_recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

    hero_scores = {}
    for combo, prob in top_recommendations:
        for hero in combo:
            hero_scores.setdefault(hero, []).append(prob)

    hero_avg = [(hero, np.mean(scores) * 100) for hero, scores in hero_scores.items()]
    return sorted(hero_avg, key=lambda x: x[1], reverse=True)[:3]

def get_model_metrics():
    if any(metric is None for metric in (model_accuracy, model_roc_auc, model_cv_score, conf_matrix)):
        train_model()
    return model_accuracy, model_roc_auc, model_cv_score, conf_matrix
