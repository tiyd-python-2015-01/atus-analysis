import pandas as pd
import re
import numpy as np
from collections import OrderedDict


def average_minutes2(data, activity_code):
    cols = activity_columns(data, activity_code)
    activity_data = data[cols]
    activity_sums = activity_data.sum(axis=1)
    data = data[['TUFINLWGT']]
    data['minutes'] = activity_sums
    data = data.rename(columns={"TUFINLWGT": "weight"})
    data['weighted_minutes'] = data.weight * data.minutes
    return data.weighted_minutes.sum() / data.weight.sum()


def activity_columns(data, activity_code):
    """For the activity code given, return all columns that fall under
    that activity."""
    col_prefix = "t{}".format(activity_code)
    return [column for column in data.columns if re.match(col_prefix, column)]


def activity_values(data, activity_code):
    """For the activity code given, return all columns that fall under that
    activity."""
    code_prefix = "{}".format(activity_code)
    return [value for value in data.TRTIER2.unique()
            if re.match(code_prefix
            , value)]

def average_happiness_act(data, activity_code):
    """Note that the code for this is going to be different then the other
    activity codes. Because TRTIER2, which only uses four letter codes. For
    example if you wanted to look at work which according to the TRTIER2
    codes is 0501. Becuase PANDAS did not recognize the code as a str at first
    instead translates to 501. This is not a large inconvience as you can just
    use 5, and it will find all the activites under the first teir 05."""
    values = activity_values(data, activity_code)
    happiness_means = []
    for value in values:
        activity_crit = (data.TRTIER2 == value)
        activity_data = data[activity_crit]
        activity_data = activity_data.rename(columns={"WUHAPPY": "happy",
                                                      'WUFNACTWTC': 'weight',
                                                      'WRTELIG': 'time'})
        activity_data['weighted_happiness'] = (activity_data.happy *
                                               activity_data.weight *
                                               activity_data.time)
        activity_data['weighted_time'] = (activity_data.weight *
                                          activity_data.time)
        happiness_means.append(activity_data.weighted_happiness.sum() /
                               activity_data.weighted_time.sum())
    happiness_mean = np.array(happiness_means).mean()
    return happiness_mean


def average_happiness(data):
    data = data.rename(columns={"WUHAPPY": "happy", 'WUFNACTWTC': 'weight'})
    data['weighted_happiness'] = data.happy * data.weight
    return (data.weighted_happiness.sum() / data.weight.sum())


def life_satisfaction(data):
    data = data.rename(columns={"WECANTRIL": 'satisfaction'})
    return data.satisfaction.mean()


def satisfaction_by_family_income(data):
    less_15000 = (data.HEFAMINC <= 5)
    less_30000 = (data.HEFAMINC > 5) & (data.HEFAMINC <= 8)
    less_50000 = (data.HEFAMINC > 8) & (data.HEFAMINC <= 11)
    less_75000 = (data.HEFAMINC > 11) & (data.HEFAMINC <= 13)
    less_100000 = (data.HEFAMINC > 13) & (data.HEFAMINC <= 14)
    less_150000 = (data.HEFAMINC > 14) & (data.HEFAMINC <= 16)
    crit_list = [less_15000, less_30000, less_50000, less_75000, less_75000,
                 less_100000, less_150000]
    satis_list = []
    for crit in crit_list:
        temp_data = data
        temp_data = data[crit]
        satis_list.append(life_satisfaction(temp_data))
    dict_list = OrderedDict([("0 - 14,999", [satis_list[0]]),
                             ("15,000 - 29,999", [satis_list[1]]),
                             ("30,000 - 49,999", [satis_list[2]]),
                             ("50,000 - 74,999", [satis_list[3]]),
                             ("75,000 - 99,999", [satis_list[4]]),
                             ("100,00+", [satis_list[5]])])
    return pd.DataFrame(dict_list).T.plot(ylim=(6, 9))


def happiness_by_family_income(data, activity_value):
    colors = ['#b0ff9e', '#82ff66', '#4cff24', '#2beb00', '#27d600', '#20ad00']
    happy_list = []
    less_15000 = (data.HEFAMINC <= 5)
    less_30000 = (data.HEFAMINC > 5) & (data.HEFAMINC <= 8)
    less_50000 = (data.HEFAMINC > 8) & (data.HEFAMINC <= 11)
    less_75000 = (data.HEFAMINC > 11) & (data.HEFAMINC <= 13)
    less_100000 = (data.HEFAMINC > 13) & (data.HEFAMINC <= 14)
    less_150000 = (data.HEFAMINC > 14) & (data.HEFAMINC <= 16)
    crit_list = [less_15000, less_30000, less_50000,
                 less_75000, less_75000, less_100000,
                 less_150000]
    for crit in crit_list:
        temp_data = data
        temp_data = data[crit]
        happy_list.append(average_happiness_act(temp_data, activity_value) -
                          average_happiness(temp_data))
    dict_list = OrderedDict([("$0 - 14,999", [happy_list[0]]),
                             ("$15,000 - 29,999", [happy_list[1]]),
                             ("$30,000 - 49,999", [happy_list[2]]),
                             ("$50,000 - 74,999", [happy_list[3]]),
                             ("$75,000 - 99,999", [happy_list[4]]),
                             ("$100,00+", [happy_list[5]])])
    limits = (min(happy_list) - .25, max(happy_list) + .25)
    colors = ['#b0ff9e', '#82ff66', '#4cff24', '#2beb00', '#27d600', '#20ad00']
    return pd.DataFrame(dict_list).T.plot(ylim=limits, kind='bar',
                                          color=colors, legend=False)


def happiness_of_generations(data, activity_code):
    first_gen_crit = (data.TEAGE <= 25)
    second_gen_crit = (data.TEAGE > 25) & (data.TEAGE <= 50)
    third_gen_crit = (data.TEAGE > 50) & (data.TEAGE <= 75)
    foruth_gen_crit = (data.TEAGE > 75)
    criteria = [first_gen_crit, second_gen_crit, third_gen_crit,
                foruth_gen_crit]
    temp_list = []
    for crit in criteria:
        temp_data = data
        temp_data = temp_data[crit]
        temp_list.append(average_happiness_act(temp_data, activity_code) -
                         average_happiness(temp_data))
    first_gen = ('First Generation', [temp_list[0]])
    second_gen = ('Second Generation', [temp_list[1]])
    third_gen = ('Third Generation', [temp_list[2]])
    fourth_gen = ('Fourth Generation', [temp_list[3]])
    temp_dict = OrderedDict([first_gen, second_gen, third_gen, fourth_gen])
    colors = ['#57bcff', '#1fa5ff', '#0084db', '#0071bd']
    limit = (min(temp_list)-.25, max(temp_list)+.25)
    return pd.DataFrame(temp_dict).T.plot(kind='bar', color=colors, ylim=limit,
                                          legend=False)


def happiness_of_employed_unemployed(df, activity_code):
    employed = df[(df.TEAGE > 18) & (df.TELFS == 1) | (df.TELFS == 2)]
    unemployed = df[(df.TEAGE > 18) & (df.TELFS == 3) | (df.TELFS == 4)]
    retired = df[(df.TELFS == 5)]
    df_list = [employed, unemployed, retired]
    temp_list = [average_happiness_act(data, activity_code) -
                 average_happiness(data) for data in df_list]
    dict_list = [('Employed Adults', [temp_list[0]]),
                 ('Unemployed Adults', [temp_list[1]]),
                 ('Not Working', [temp_list[2]])]
    temp_dict = OrderedDict(dict_list)
    colors = ['#8257c1', '#9f271e', '#0031ad']
    limit = (min(temp_list)-.25, max(temp_list)+.25)
    return pd.DataFrame(temp_dict).T.plot(kind='bar', color=colors,
                                          ylim=limit, legend=False)


def happiness_of_sexes(df, activity_code):
    males = df[(df.TESEX == 1)]
    females = df[(df.TESEX == 2)]
    df_list = [males, females]
    temp_list = [average_happiness_act(data, activity_code) -
                 average_happiness(data) for data in df_list]
    temp_dict = {'Men': [temp_list[0]], 'Women': [temp_list[1]]}
    colors = ['#83d053', '#e69e4c']
    limit = (min(temp_list)-.25, max(temp_list)+.25)
    return pd.DataFrame(temp_dict).T.plot(kind='bar', color=colors, ylim=limit,
                                          legend=False)
