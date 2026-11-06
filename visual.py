import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display 

   


#информация и графики количественных данных
def kol_info(x, x_title='', y_title='', title='', color='#3498DB', bins='auto', figsize=(11,6), alpha=0.7):
    display(x.describe())
    
    fig, ax = plt.subplots(2, 1, figsize=(figsize[0], figsize[1]*1.5), gridspec_kw={'height_ratios':[3,1]})
    
    #гистограмма
    sns.histplot(x, bins=bins, kde=True, color=color, alpha=alpha, ax=ax[0])
    ax[0].set_title(f'Histogram of {title}')
    ax[0].set_xlabel(x_title)
    ax[0].set_ylabel(y_title)
    
    #boxplot
    sns.boxplot(x=x, color=color, orient='h', ax=ax[1])
    ax[1].set_title(f'Boxplot of {title}')
    
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
        plt.xlabel(value_col)
        plt.ylabel(y_title)
        plt.title(title)
            
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
def date_info(df, date_col, period='M', bins=100, figsize=(11,6), title='Distribution of Dates'):
    #гистограмма по исходным датам
    df[date_col].hist(bins=bins, figsize=figsize)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Frequency')
    plt.show()
    
    #создание периода
    period_col = f'{date_col}_{period}'
    df[period_col] = df[date_col].dt.to_period(period)
    
    #гистограмма по периодам
    df[period_col].value_counts().sort_index().plot(figsize=figsize)
    plt.title(f'{title} by period ({period})')
    plt.xlabel('Date')
    plt.ylabel('Frequency')
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


    sns.scatterplot(
        x=x, y=y, data=df,
        hue=hue1, palette=palette, alpha=alpha,
        ax=ax[0,0]
    )

    ax[0,0].set_title(f'{y_col} vs {x_col} by {hue1}')
    ax[0,0].set_xlabel(x_col)
    ax[0,0].set_ylabel(y_col)

    sns.scatterplot(
        x=x, y=y, data=df,
        hue=hue2, palette=palette, alpha=alpha,
        ax=ax[0,1]
    )

    ax[0,1].set_title(f'{y_col} vs {x_col} by {hue2}')
    ax[0,1].set_xlabel(x_col)
    ax[0,1].set_ylabel(y_col)

    sns.scatterplot(
        x=y, y=hue1, data=df,
        palette=palette, alpha=alpha,
        ax=ax[1,0]
    )

    ax[1,0].set_title(f'{hue1} vs {y_col}')
    ax[1,0].set_xlabel(y_col)
    ax[1,0].set_ylabel(hue1)

    sns.scatterplot(
        x=y, y=hue2, data=df,
        palette=palette, alpha=alpha,
        ax=ax[1,1]
    )

    ax[1,1].set_title(f'{hue2} vs {y_col}')
    ax[1,1].set_xlabel(y_col)
    ax[1,1].set_ylabel(hue2)

    plt.tight_layout()
    plt.show()

