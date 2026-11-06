# 🏠 Прогнозирование стоимости недвижимости

Предсказание цены домов на основе характеристик объекта и района. Проект выполнен как end-to-end ML-пайплайн: EDA → preprocessing → baseline → improvements.

> Часть ноутбуков (improvement_cv.ipynb, hyperparam_tuning.ipynb) взяты в учебных целях у [andyfirez](https://github.com/andyfirez). Остальное — моё.

## Данные

- **Источник:** df_train.csv (13 603 записи)
- **Период:** май 2014 — май 2015
- **Целевая переменная:** price (стоимость продажи)
- **Признаки:** 13 — площадь, кол-во спален/санузлов, качество строительства, район, наличие подвала/ремонта/вида и др.

## Структура проекта

```
├── side_lib.py              # Вспомогательные функции (info, VIF, оценка моделей)
├── visual.py                # Визуализации (гистограммы, boxplot, scatter, категории)
├── eda.ipynb                # Разведочный анализ данных
├── baseline.ipynb           # Базовые модели без обработки признаков
├── improvements.ipynb       # Улучшения: feature engineering, preprocessing, лог-трансформация
├── df_train.csv             # Данные
└── report.html              # Auto-generated EDA-отчёт (Sweetviz)
```

## Что сделано

### EDA
- Анализ пропусков и дубликатов (0 пропусков, 2 дубликата)
- Распределения количественных и категориальных признаков
- Phik-корреляция для смешанных типов данных
- VIF-анализ мультиколлинеарности
- Анализ скошенности price (skew=0.80) → логарифмирование

### Baseline
- 4 модели: LinearRegression, DecisionTree, RandomForest, LightGBM
- TimeSeriesSplit (5 фолдов) — корректная кросс-валидация для временных данных
- Диагностика: residual plots, feature importance, абляция признаков

### Improvements
- ColumnTransformer: StandardScaler + OneHotEncoder + passthrough
- Feature engineering: house_size_score (комбинация размера), год продажи
- Лог-преобразование target для линейных моделей
- Сравнение всех моделей с улучшенным preprocessing

## Результаты

| Модель | MAE | RMSE | R² |
|---|---|---|---|
| LinearRegression | 78 319 | 104 610 | 0.74 |
| DecisionTree | 105 548 | 144 187 | 0.51 |
| RandomForest | 78 087 | 106 533 | 0.73 |
| **LightGBM** | **74 499** | **101 764** | **0.76** |

**Лучшая модель:** LightGBM — MAE ≈ 74.5k, R² = 0.76

**Ключевые признаки:** quartile_zone (район) и living_in_m2 (площадь) — их удаление сильнее всего снижает качество.

## Инструменты

Python, pandas, numpy, scikit-learn, LightGBM, matplotlib, seaborn, phik, statsmodels, sweetviz, missingno

## Как запустить

```bash
pip install pandas numpy scikit-learn lightgbm matplotlib seaborn phik statsmodels sweetviz missingno
jupyter notebook eda.ipynb
```
