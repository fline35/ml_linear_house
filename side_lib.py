import pandas as pd
from IPython.display import display
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from matplotlib import pyplot as plt
from sklearn.tree import plot_tree
import numpy as np




#вывод основной информации о датафрейме
def data_info(df):
    display('Первые строки')
    display(df.head())
    display('Описание данных')
    display(df.describe())
    display('Базовая системная информация')
    display(df.info())


    #функция для вывода пропусков и дубликатов в количественном и процентном виде

def mis_dup_info(df):
    missing_values = df.isnull().sum() # количество пропущеннных строк
    duplicated_values = df.duplicated().sum() #Количество явных дубликатов
    total_values = df.shape[0]  # общее количество строк

    # добавление процента значений
    missing_percent = ((missing_values / total_values) * 100).round(3).astype(str) + '%'
    duplicated_percent = ((duplicated_values / total_values) * 100).round(3).astype(str) + '%'
    
    # создание датафреймов отображающих нужные данные
    missing_duplicated_df = pd.DataFrame({
        'total' : total_values,
        'missing': missing_values,
        'percent_missing': missing_percent,
        'duplicated' : duplicated_values,
        'percent_duplicated' : duplicated_percent
        
    })   
    

    return missing_duplicated_df

#функция для расчета VIF
def calculate_vif(df, target_column=None):
    #расчет VIF для каждого признака
    numeric_df = df.select_dtypes(include=['int64', 'float64']).copy()
    if target_column and target_column in numeric_df.columns:
        numeric_df.drop(columns=[target_column], inplace=True)
    vif_data = pd.DataFrame()
    vif_data["feature"] = numeric_df.columns
    vif_data["VIF"] = [variance_inflation_factor(numeric_df.values, i) for i in range(numeric_df.shape[1])]
    vif_data = vif_data.sort_values(by="VIF", ascending=False).reset_index(drop=True)
    
    return vif_data






def evaluate_pipeline_to_df(
    name, pipeline, X, y, tscv,
    plot_residuals=True,
    tree_max_depth=None,
    plot_feature_importance=True,
    show_folds=True
):
    """Считает метрики по фолдам и при необходимости строит диагностические графики.

    Параметр tree_max_depth оставлен для совместимости и сейчас не используется.
    """
    maes, rmses, r2s = [], [], []
    all_y_test, all_preds = [], []

    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        maes.append(mean_absolute_error(y_test, predictions))
        rmses.append(mean_squared_error(y_test, predictions) ** 0.5)
        r2s.append(r2_score(y_test, predictions))
        all_y_test.append(y_test)
        all_preds.append(predictions)

    df_mean = pd.DataFrame({
        'mean_mae': [np.mean(maes)],
        'r2_mean': [np.mean(r2s)],
        'rmse_mean': [np.mean(rmses)],
    }, index=[name])
    df_folds = pd.DataFrame({
        'fold': range(len(maes)),
        'mae': maes,
        'r2': r2s,
        'rmse': rmses,
    })

    display(df_mean)
    if show_folds:
        display(df_folds)

    if plot_residuals:
        actual = pd.concat(all_y_test)
        predictions = np.concatenate(all_preds)
        residuals = actual - predictions
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        axes[0].hist(residuals, bins=30, edgecolor='black')
        axes[0].set_title('Распределение остатков')
        axes[1].scatter(predictions, residuals, alpha=0.5)
        axes[1].set_title('Остатки и прогнозы')
        axes[0].set_xlabel('Остаток, $')
        axes[1].set_xlabel('Прогноз, $')
        axes[1].set_ylabel('Остаток, $')
        plt.tight_layout()
        plt.show()

    if plot_feature_importance:
        model = pipeline.named_steps.get('model')
        importances = getattr(model, 'feature_importances_', None)
        if importances is None:
            print('Для этой модели важность признаков недоступна.')
        elif len(importances) != len(X.columns):
            print('Важности признаков нельзя сопоставить с исходными столбцами.')
        else:
            importance = pd.Series(importances, index=X.columns).sort_values()
            importance.plot(kind='barh', figsize=(8, 6))
            plt.title(f'Важность признаков: {name}')
            plt.xlabel('Важность')
            plt.tight_layout()
            plt.show()

    return df_mean, df_folds

class DateGroupedTimeSeriesSplit:
    """TimeSeriesSplit по уникальным датам, чтобы один день не делился между фолдами."""
    def __init__(self, dates, n_splits=5):
        self.dates = pd.Series(pd.to_datetime(dates)).reset_index(drop=True)
        self.splitter = TimeSeriesSplit(n_splits=n_splits)

    def split(self, X, y=None, groups=None):
        unique_dates = pd.Index(self.dates.unique()).sort_values()
        for train_ids, test_ids in self.splitter.split(unique_dates):
            train_dates, test_dates = unique_dates[train_ids], unique_dates[test_ids]
            yield (
                np.flatnonzero(self.dates.isin(train_dates)),
                np.flatnonzero(self.dates.isin(test_dates)),
            )


def make_pipeline(estimator, numeric_features, bool_features, categorical_features):
    """Общий pipeline: медиана и scaler для чисел, OneHot для категорий."""
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    category_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False)),
    ])
    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipe, numeric_features),
        ("binary", "passthrough", bool_features),
        ("category", category_pipe, categorical_features),
    ]).set_output(transform="pandas")
    return Pipeline([
        ("preprocessor", preprocessor),
        ("model", estimator),
    ])


def evaluate_cv(variants, y, dates, tscv):
    """Считает метрики вариантов по одним временным фолдам."""
    fold_rows = []
    for name, (pipeline, X) in variants.items():
        for fold, (train_idx, test_idx) in enumerate(tscv.split(X), start=1):
            model = clone(pipeline).fit(X.iloc[train_idx], y.iloc[train_idx])
            predictions = model.predict(X.iloc[test_idx])
            train_dates, test_dates = dates.iloc[train_idx], dates.iloc[test_idx]
            fold_rows.append({
                "variant": name,
                "fold": fold,
                "train_period": f"{train_dates.min():%Y-%m-%d} — {train_dates.max():%Y-%m-%d}",
                "test_period": f"{test_dates.min():%Y-%m-%d} — {test_dates.max():%Y-%m-%d}",
                "mae": mean_absolute_error(y.iloc[test_idx], predictions),
                "rmse": mean_squared_error(y.iloc[test_idx], predictions) ** 0.5,
                "r2": r2_score(y.iloc[test_idx], predictions),
            })
    folds = pd.DataFrame(fold_rows)
    summary = folds.groupby("variant").agg(
        mae_mean=("mae", "mean"), mae_std=("mae", "std"),
        rmse_mean=("rmse", "mean"), rmse_std=("rmse", "std"),
        r2_mean=("r2", "mean"), r2_std=("r2", "std"),
    ).reset_index()
    return summary, folds

