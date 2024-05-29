def df_to_list(df):
    list_from_df = []
    for index, row in df.iterrows():
        line = f"{row['Имя человека']} (Время отправления: {row['Время отправления']}) : {row['Место отправления']} - {row['Место прибытия']}"
        list_from_df.append(line)
    return list_from_df
