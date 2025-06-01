from random import sample

def get_counter_heroes(hero1, hero2, hero3):
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from ast import literal_eval
    from itertools import combinations

    # Load and clean data
    df = pd.read_csv('results.csv')
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

    # Get hero list
    all_heroes = sorted(set(hero for row in pd.concat([df_all['left_heroes'], df_all['right_heroes']]) for hero in row))

    # One-hot encoding
    def encode_match(row):
        encoding = dict.fromkeys(['L_' + h for h in all_heroes] + ['R_' + h for h in all_heroes], 0)
        for h in row['left_heroes']:
            encoding['L_' + h] = 1
        for h in row['right_heroes']:
            encoding['R_' + h] = 1
        return pd.Series(encoding)

    X = df_all.apply(encode_match, axis=1)
    y = df_all['match_result']

    # Train model
    X_train, _, y_train, _ = train_test_split(X, y, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Predict counter combos
    enemy_heroes = [hero1, hero2, hero3]
    our_hero_pool = [h for h in all_heroes if h not in enemy_heroes]
    all_combos = list(combinations(our_hero_pool, 3))

    # Batasi kombinasi maksimal 3000 random sampel
    sample_combos = sample(all_combos, min(3000, len(all_combos)))

    input_data = []
    combos = []

    for combo in sample_combos:
        input_vec = dict.fromkeys(X.columns, 0)
        for h in enemy_heroes:
            col = 'R_' + h
            if col in input_vec:
                input_vec[col] = 1
        for h in combo:
            input_vec['L_' + h] = 1
        input_data.append(input_vec)
        combos.append(combo)

    input_df = pd.DataFrame(input_data)
    probs = model.predict_proba(input_df)[:, 1]
    recommendations = list(zip(combos, probs))
    top_recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

    # Hitung rata-rata skor tiap hero
    hero_scores = {}
    for combo, prob in top_recommendations:
        for hero in combo:
            if hero not in hero_scores:
                hero_scores[hero] = []
            hero_scores[hero].append(prob)

    hero_avg = [(hero, np.mean(scores) * 100) for hero, scores in hero_scores.items()]
    hero_avg = sorted(hero_avg, key=lambda x: x[1], reverse=True)

    return hero_avg[:3]
