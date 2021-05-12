import requests
import json
from tqdm.auto import tqdm
from collections import defaultdict
import pickle
import pandas as pd
from collections import Counter
#1 Задание вытащить все вакансии СБЕРа с ХХ
sber = '3529'
page = 1
num_per_page = 100
perm = 1
url = f'https://api.hh.ru/vacancies?employer_id={sber}&page={page}&per_page={num_per_page}&area={perm}'
res = requests.get(url)
vacancies = res.json()
num_pages = vacancies.get('pages')
vacancy_ids = [el.get('id') for el in vacancies.get('items')]
all_vacancy_ids = []
for i in tqdm(range(vacancies.get('pages'))):
    url = f'https://api.hh.ru/vacancies?employer_id={sber}&page={i}&per_page={num_per_page}&area={perm}'
    res = requests.get(url)
    vacancies = res.json()
    vacancy_ids = [el.get('id') for el in vacancies.get('items')]
    all_vacancy_ids.extend(vacancy_ids)

#2 Вытащите все описания этих вакансий
tabdict = defaultdict(list)
for vac_id in tqdm(all_vacancy_ids):
    try:
        url = f'https://api.hh.ru/vacancies/{vac_id}'
        res = requests.get(url, timeout=10)
        vacancy = res.json()
        tabdict['id'].append(vacancy.get('id'))
        tabdict['name'].append(vacancy.get('name'))
        tabdict['description'].append(vacancy.get('description'))
        tabdict['skills'].append(vacancy.get('key_skills'))
        tabdict['published_at'].append(vacancy.get('published_at'))
    except:
        print('exeption')
        pass

#3 Создайте аналогичный vacancy DataFrame только добавьте поле skills
sk = tabdict.get('skills')
tabdict['skills'] = [','.join([y.get('name') for y in x]) for x in sk]
df = pd.DataFrame(tabdict)
print(df.head())

#4 Переведите даты публикаций в datetime
df.published_at = pd.to_datetime(df.published_at).dt.date

#5 Постройте график опубликованных вакансий по датам
df = df.set_index('published_at')
df = df.reset_index()
df.groupby('published_at')['id'].count().plot(kind='barh')

#6 Переведите даты в дни недели, и определите день недели, в который больше всего публикуют вакансий
df['weekday'] = df.published_at.apply(lambda x: x.weekday())
df.groupby('weekday')['id'].count()

#7 Найдите те вакансии с использованием python, которые вам интересны
interesting_name = 'аналитик'
interesting_desc = 'python'
term1 = df.name.str.lower().str.contains(interesting_name)
term2 = df.description.str.lower().str.contains(interesting_desc)
df[term1 & term2]

#8 Определите по полю skills какие навыки больше всего востребованы для этих вакансий, и
skills = ','.join([x for x in df[term1&term2].skills.tolist() if x ]).split(',')
skills_count = Counter(skills)
skills_count['Python'] = 0
skills_count.most_common(10)

#9 Постройте график наиболее востребованных вакансий