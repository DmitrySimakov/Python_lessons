import csv
import string
import datetime
import os
from collections import Counter, defaultdict
csv.field_size_limit(100000000)
#vacs = list(csv.DictReader(open("C://vacancy.csv", "r", encoding='UTF8')))
file_pth = os.path.join('vacancy.csv')

vacs = list(csv.DictReader(open(file_pth, encoding='UTF-8', newline='')))
count_dict = defaultdict(int)

# Сколько вакансий с позициями на которых вы работаете?
for vac in vacs:
    vacs_strtitle = str(vac.get('vactitle'))
    vacs_des = str(vac.get('vacdescription'))
    condition = [
        'ассистент клиентского менеджера' in vacs_strtitle.lower(),
        'ассистент КМ' in vacs_strtitle.lower(),
        'акм' in vacs_strtitle.lower()
    ]
    if any(condition):
        count_dict['count_work_vac']+= 1

# Сколько вакансий для аналатика данных?
    condition_da = [
        'аналитик данных' in vacs_strtitle.lower(),
        'data analyst' in vacs_strtitle.lower(),
        'da' in vacs_strtitle.lower()
    ]
    if any(condition_da):
        count_dict['count_da_vac'] += 1

# Сколько вакансий для аналитика данных с использованием Python?
        condition_py = [
            'python' in vacs_strtitle.lower(),
            'питон' in vacs_strtitle.lower(),
        ]
        if any(condition_py):
            count_dict['count_da_vac_py'] += 1

# Сколько вакансий, которые вам нравятся?
    condition_like = [
        'москва' in vacs_des.lower(),
        'г.москва' in vacs_des.lower(),
        'москва,' in vacs_des.lower(),
        'г.москва,' in vacs_des.lower(),
        ]
    if any(condition_like):
        count_dict['vac_like'] += 1

# Насколько свежие эти вакансии?
        vac_date = datetime.datetime.strptime(vac['vacdate'], '%Y-%m-%d')
        delta_days = (datetime.datetime.today() - vac_date).days
        if delta_days <=30:
            count_dict['count_vac_fresh_month'] += 1
        elif 30 < delta_days <= 30 * 3:
            count_dict['count_vac_fresh_kvartal'] += 1
        elif 30 * 3 < delta_days <= 30 * 6:
            count_dict['count_vac_fresh_halfyear'] += 1
        else:
            count_dict['count_vac_fresh_older_halfyear'] += 1
big_str = f"""
Сколько вакансий, которые вам нравятся? - {count_dict.get("vac_like")}. Из них
\t вакансий младше месяца - {count_dict.get("count_vac_fresh_month")}
\t Вакансий младше квартала - {count_dict.get("count_vac_fresh_kvartal")}
\t вакансий младше полугода - {count_dict.get("count_vac_fresh_halfyear")}
\t вакансий старше полугода - {count_dict.get("count_vac_older_halfyear")}
Сколько вакансий с позициями на которых вы работаете? - {count_dict.get("count_work_vac")}
Сколько вакансий для аналитика данных? - {count_dict.get("count_da_vac")}
Сколько вакансий для аналитика данных с использованием Python? - {count_dict.get("count_work_vac")}
"""
print(big_str)