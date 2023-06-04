import pandas as pd


def read_data_from_doc(src):
    if '.csv' in src:
        data = pd.read_csv(src)['Ваши данные:']
    elif 'xlsx' in src:
        data = pd.read_excel(src)['Ваши данные:']
    else:
        raise Exception

    house_type_encoding = {
        None: None,
        'Кирпичный': 0,
        'Блочный': 1,
        'Монолитный': 2,
        'Монолитно кирпичный': 3,
        'Сталинский': 4,
        'Панельный': 5
    }
    parking_encoding = {
        None: None,
        'Подземная': 0,
        'Открытая': 1,
        'Наземная': 2,
        'Многоуровневая': 3
    }

    data = {
        'Кухня': data.iloc[0],
        'Год постройки': data.iloc[1],
        'Санузел': data.iloc[2],
        'Тип дома': house_type_encoding[data.iloc[3]],
        'Парковка': parking_encoding[data.iloc[4]],
        'Высота потолков': data.iloc[5],
        'Этаж': data.iloc[6],
        'Площадь': data.iloc[7],
        'Новойстройка': data.iloc[8],
        'Пентхаус': data.iloc[9],
        'Апартаменты': data.iloc[10],
        'Вид на улицу': data.iloc[11],
        'Жилплощадь': data.iloc[12],
        'Балкон': data.iloc[13],
        'Время до метро': data.iloc[14],
        'Всего этажей': data.iloc[15]
    }

    return data
