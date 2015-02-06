def activity_columns(data, activity_code):
    """For the activity code given, return all columns that fall
    under that activity."""
    col_prefix = "t{}".format(activity_code)
    return [column for column in data.columns if re.match(col_prefix, column)]

def average_minutes(data, activity_code):
    cols = activity_columns(data, activity_code)
    activity_data = data[cols]
    activity_sums = activity_data.sum(axis=1)
    data = data[['TUFINLWGT']]
    data['minutes'] = activity_sums
    data = data.rename(columns={"TUFINLWGT": "weight"})
    data['weighted_minutes'] = data.weight * data.minutes
    return data.weighted_minutes.sum() / data.weight.sum()

def activity_name_lookup(a_list):
    return [((activity_code_dict_t[int(code)][0], num)) for code, num in a_list]

def percentage_more(original, challenger):
    return (original - challenger) / challenger

def comparing_user_sets(original, challenger, activity_code):
    original_activity = average_minutes(summary[original], activity_code) / 60
    challenger_activity = average_minutes(summary[challenger], activity_code) / 60
    return percentage_more(original_activity, challenger_activity)

def list_of_comparisons(orig, chall, activity_code_list):
    output_list = []
    for code in activity_code_list:
        result_percent = comparing_user_sets(orig, chall, code)
        output_list.append((code, result_percent))
    return output_list

def values_only(a_list):
    return [num for code, num in a_list]

def value_names(a_list):
    return [name for name, num in a_list]

def remove_outlier(a_list):
    high_percentile = np.percentile(values_only(child_vs_no_child_results), 95)
    return [(counter, value) for counter, value in child_vs_no_child_results if abs(value) < iqr]

def plot_horiz_bar(a_list):
    a_list = remove_outlier(a_list)
    x_labels = value_names(activity_name_lookup(a_list))
    x_values = values_only(activity_name_lookup(a_list))
    width = .5
    height = np.arange(len(x_labels))

    ply.yticks(height+width/2., x_labels)
    ply.barh(height, x_values, width, color = sbn.color_palette())
    return ply.show()

def plot_user_group_breakdown(user_list_a, user_list_b, data_point):
    a_list = summary[user_list_a][data_point].value_counts()
    b_list = summary[user_list_b][data_point].value_counts()

    a_list_weight = a_list / a_list.sum()
    b_list_weight = b_list / b_list.sum()

    fig, ax = plt.subplots()
    rects1 = ax.bar(np.arange(len(a_list_weight)),
                    a_list_weight.sort_index(), .35, color='r')
    rects2 = ax.bar(np.arange(len(b_list_weight))+.35,
                    b_list_weight.sort_index(), .35, color='b')
    ax.legend( (rects1, rects2), ('user_list_a', 'user_list_b') )
    ply.xticks(np.arange(len(a_list_weight))+.35/2,
               a_list_weight.sort_index().index )
    return ply.show()
