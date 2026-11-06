import pandas as pd
from IPython.display import display
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
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
    '''
    Оценка модели с помощью временной кросс-валидации и вывод результатов в датафреймы.
    Параметры:
    - name: Название модели (строка).
    - pipeline: sklearn Pipeline с моделью.
    - X: Признаки (DataFrame).
    - y: Целевая переменная (Series).
    - tscv: Объект временной кросс-валидации (
    - plot_residuals: Флаг для построения графиков остатков (по умолчанию True).
   убрать!!!- plot_tree_graph: Флаг для визуализации дерева решений (по умолчанию False).
    - tree_max_depth: Максимальная глубина дерева для визуализации (по умолчанию None).
    - plot_feature_importance: Флаг для построения графика важности признаков (по умолчанию True).
    Возвращает:
    - df_mean: DataFrame с усредненными метриками.
    - df_folds: DataFrame с метриками по каждому фолду.
    - show_folds: Флаг для отображения метрик по фолдам (по умолчанию True).
    '''

    #метрики для каждого фолда
    maes, rmses, r2s = [], [], []
    all_y_test = []
    all_preds = []

    #временная кросс-валидация
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        #обучение и предсказание
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)

        #вычисление метрик и их сохранение
        maes.append(mean_absolute_error(y_test, preds))
        rmses.append(mean_squared_error(y_test, preds) ** 0.5)
        r2s.append(r2_score(y_test, preds))

        all_y_test.append(y_test)
        all_preds.append(preds)


    #метрики в датафреймы
    df_mean = pd.DataFrame({
        'mean_mae': [np.mean(maes)],
        'r2_mean': [np.mean(r2s)],
        'rmse_mean': [np.mean(rmses)]
    }, index=[name])

    df_folds = pd.DataFrame({
        'fold': range(len(maes)),
        'mae': maes,
        'r2': r2s,
        'rmse': rmses
    })

    display(df_mean)
    if show_folds:
        display(df_folds)

    #residuals plot
    if plot_residuals:
        all_y_test_concat = pd.concat(all_y_test)
        all_preds_concat = np.concatenate(all_preds)
        residuals = all_y_test_concat - all_preds_concat

        fig, axes = plt.subplots(1, 2, figsize=(14,5))

        axes[0].hist(residuals, bins=30, edgecolor="black")
        axes[0].set_title("Residuals Distribution")

        axes[1].scatter(all_preds_concat, residuals, alpha=0.5)
        axes[1].set_title("Residuals vs Predictions")

        plt.tight_layout()
        plt.show()
    


    #feature importance
    if plot_feature_importance:
        try:
            model = pipeline.named_steps['model']

            importances = model.feature_importances_
            fi = pd.Series(importances, index=X.columns).sort_values()

            plt.figure(figsize=(8,6))
            fi.plot(kind="barh")
            plt.title(f"Feature Importance: {name}")
            plt.xlabel("Importance")
            plt.tight_layout()
            plt.show()

        except:
            print("Feature importance недоступна для этой модели")

    return df_mean, df_folds


