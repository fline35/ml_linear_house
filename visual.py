import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display 

   


#информация и графики количественных данных
def kol_info(x, x_title='', y_title='', title='', color='#3498DB', bins='auto', figsize=(11,6), alpha=0.7):
    display(x.describe())
    
    fig, ax = plt.subplots(2, 1, figsize=(figsize[0], figsize[1]*1.5), gridspec_kw={'height_ratios':[3,1]})
    
    #гистограмма
    sns.histplot(x, bins=bins, kde=True, color=color, alpha=alpha, ax=ax[0])
    ax[0].set_title(title)
    ax[0].set_xlabel(x_title)
    ax[0].set_ylabel(y_title)
    
    #boxplot
    sns.boxplot(x=x, color=color, orient='h', ax=ax[1])
    ax[1].set_title(f'Диаграмма размаха: {title}')
    
    plt.tight_layout()
    plt.show()


#информация и графики категориальных данных
def cat_info(
        df,
        target,
        value_col=None,
        x_title='',
        y_title='',
        title='',
        color='#3498DB',
        figsize=(11,4),
        alpha=1,
        index_sort=False
        ):
    
    #подсчет значений по категориям
    x_val = df[target].value_counts(ascending=True)
    #средняя цена по категориям


    #сортировка по индексу
    if index_sort:
        x_val = x_val.sort_index()

    
    #горизонтальная диаграмма
    ax = x_val.plot(
        kind='barh',
        figsize=figsize,
        color=color,
        alpha=alpha
    )
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    
    #добавление значения рядом со столбцовм
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f'{width}',
                (width, p.get_y() + p.get_height() / 2.),
                ha='left', va='center',
                xytext=(5, 0),
                textcoords='offset points')
    plt.show()
    
    #круговая диаграмма
    x_val.plot(
        kind='pie',
        title=title,
        autopct= "%.0f%%",
        figsize=figsize
        )
    
    plt.show()
    
    #средняя цена по категориям

    if value_col is not None:
        display('Средняя цена по категориям:')
        mean_by_category = df.groupby(target)[value_col].mean().sort_values().round(1)

        mbc_plot = mean_by_category.plot(
            kind='barh',
            figsize=figsize,
            color=color,
            alpha=alpha
        )
        plt.xlabel({'price': 'Цена'}.get(value_col, value_col))
        plt.ylabel(y_title)
        plt.title('Средняя цена по категориям')
            
        #добавление значения рядом со столбцовм
        for p in mbc_plot.patches:
            width = p.get_width()
            mbc_plot.annotate(f'{width}',
                    (width, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center',
                    xytext=(5, 0),
                    textcoords='offset points')
        plt.show()



    
    

    
    


#информация и графики по дате
def date_info(df, date_col, period='M', bins=100, figsize=(11,6), title='Продажи'):
    #гистограмма по исходным датам
    df[date_col].hist(bins=bins, figsize=figsize)
    plt.title(title)
    plt.xlabel('Дата')
    plt.ylabel('Количество')
    plt.show()
    
    #создание периода
    period_col = f'{date_col}_{period}'
    df[period_col] = df[date_col].dt.to_period(period)
    
    #гистограмма по периодам
    df[period_col].value_counts().sort_index().plot(figsize=figsize)
    plt.title(f'{title} по периодам ({period})')
    plt.xlabel('Дата')
    plt.ylabel('Количество')
    plt.show()
    
#функция для построения двух scatter plot рядом горизонтально
def four_scatter_horizontal(
    df,
    x_col,
    y_col,
    hue1,
    hue2,
    figsize=(20, 16),
    palette='viridis',
    alpha=0.7,
    sample_size=3000,
    is_sample=False
    ):

    if is_sample == True:
        df = df.sample(n=sample_size, random_state=42)
    x = df[x_col]
    y = df[y_col]

    fig, ax = plt.subplots(2, 2, figsize=figsize)
    feature_labels = {
        'price': 'Цена',
        'living_in_m2': 'Жилая площадь, м²',
        'grade': 'Качество дома',
        'quartile_zone': 'Квартильная зона',
    }
    x_label = feature_labels.get(x_col, x_col.replace('_', ' '))
    y_label = feature_labels.get(y_col, y_col.replace('_', ' '))
    hue1_label = feature_labels.get(hue1, hue1.replace('_', ' '))
    hue2_label = feature_labels.get(hue2, hue2.replace('_', ' '))

    sns.scatterplot(
        x=x, y=y, data=df,
        hue=hue1, palette=palette, alpha=alpha,
        ax=ax[0,0]
    )

    ax[0,0].set_title(f'{y_label} и {x_label} по группе «{hue1_label}»')
    ax[0,0].set_xlabel(x_label)
    ax[0,0].set_ylabel(y_label)

    sns.scatterplot(
        x=x, y=y, data=df,
        hue=hue2, palette=palette, alpha=alpha,
        ax=ax[0,1]
    )

    ax[0,1].set_title(f'{y_label} и {x_label} по группе «{hue2_label}»')
    ax[0,1].set_xlabel(x_label)
    ax[0,1].set_ylabel(y_label)

    sns.scatterplot(
        x=y, y=hue1, data=df,
        alpha=alpha,
        ax=ax[1,0]
    )

    ax[1,0].set_title(f'Связь «{hue1_label}» с «{y_label}»')
    ax[1,0].set_xlabel(y_label)
    ax[1,0].set_ylabel(hue1_label)

    sns.scatterplot(
        x=y, y=hue2, data=df,
        alpha=alpha,
        ax=ax[1,1]
    )

    ax[1,1].set_title(f'Связь «{hue2_label}» с «{y_label}»')
    ax[1,1].set_xlabel(y_label)
    ax[1,1].set_ylabel(hue2_label)

    plt.tight_layout()
    plt.show()



def plot_price_distribution(price, bins=40, figsize=(12, 4)):
    """Показывает распределение цены в исходной шкале и после log1p."""
    values = pd.Series(price).dropna().astype(float)
    if (values < 0).any():
        raise ValueError("price must be non-negative for log1p plotting")

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    axes[0].hist(values, bins=bins, color="#3977a8", alpha=0.85)
    axes[0].set(title="Цена: исходная шкала", xlabel="Цена", ylabel="Количество")
    axes[1].hist(np.log1p(values), bins=bins, color="#d17b36", alpha=0.85)
    axes[1].set(title="Цена: log1p", xlabel="log1p(price)", ylabel="Количество")
    fig.tight_layout()
    plt.show()
    return fig, axes


def plot_actual_vs_predicted(actual, predictions, figsize=None):
    """Сравнивает фактические значения с одним или несколькими прогнозами."""
    actual = np.asarray(actual, dtype=float)
    if not predictions:
        raise ValueError("Pass at least one named prediction array")
    if any(len(values) != len(actual) for values in predictions.values()):
        raise ValueError("Actual and prediction arrays must have equal lengths")

    count = len(predictions)
    figsize = figsize or (6 * count, 5)
    fig, axes = plt.subplots(1, count, figsize=figsize, squeeze=False)
    low, high = float(actual.min()), float(actual.max())
    for ax, (name, values) in zip(axes.ravel(), predictions.items()):
        values = np.asarray(values, dtype=float)
        ax.scatter(actual, values, alpha=0.25, s=12, color="#3977a8")
        ax.plot([low, high], [low, high], linestyle="--", color="#c64b4b")
        ax.set(title=name, xlabel="Фактическая цена", ylabel="Прогноз")
    fig.tight_layout()
    plt.show()
    return fig, axes


def plot_r2_by_fold(fold_results, figsize=(9, 5)):
    """Строит R² по фолдам для нескольких вариантов модели."""
    if not fold_results:
        raise ValueError("Pass at least one named fold-results table")

    fig, ax = plt.subplots(figsize=figsize)
    for name, frame in fold_results.items():
        if not {"fold", "r2"}.issubset(frame.columns):
            raise ValueError(f"{name!r} must contain fold and r2 columns")
        ax.plot(frame["fold"], frame["r2"], marker="o", label=name)
    ax.set(title="R² по временным фолдам", xlabel="Фолд", ylabel="R²")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    plt.show()
    return fig, ax


def plot_feature_importance(pipeline, top_n=15, figsize=(9, 6), title="Важность признаков модели"):
    """Plot fitted tree-model importances using transformed feature names."""
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    if not hasattr(model, "feature_importances_"):
        raise TypeError("The fitted model must expose feature_importances_.")

    names = preprocessor.get_feature_names_out()
    values = np.asarray(model.feature_importances_, dtype=float)
    if len(names) != len(values):
        raise ValueError("Transformed feature names and importances do not match")
    order = np.argsort(values)[-top_n:]

    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(np.asarray(names)[order], values[order], color="#3977a8")
    ax.set(title=title, xlabel="Важность", ylabel="Признак")
    fig.tight_layout()
    plt.show()
    return fig, ax
