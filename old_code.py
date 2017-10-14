# app.py

# Sets up data for csv-file, using pandas
# data = functions.setup_matrix(columns, x_axis_data, y_axis_data)

# columns = ["Time", "Weekday", "Events"]

# Saves data to .csv
# functions.save_csv("hotspot.csv", data, columns)

# Creates a DataFrame to use, x_axis_data = correct order of x-axis-column
# df = functions.create_dataframe("hotspot.csv", x_axis_data, columns)

def save_csv(filename, data, columns):
    """
    Saves DataFrame as CSV
    """
    df_save = pandas.DataFrame(data, columns=columns)
    df_save.to_csv(filename)



def setup_matrix(columns, x_data, y_data):
    """
    Returns the data
    """
    data = {}
    data[columns[0]] = []
    data[columns[1]] = []
    data[columns[2]] = []
    for y in y_data:
        for x in x_data:
            data[columns[0]].append(y)
            data[columns[1]].append(x)
            data[columns[2]].append(random.randint(0, 100))

    return data



def create_dataframe(filename, sort_on, columns):
    """
    Creates a DataFrame file from csv
    """
    csv_file = pandas.read_csv(filename)
    df = csv_file.pivot_table(index=columns[0], columns=columns[1], values=columns[2], fill_value=0)
    df = df.reindex_axis(sort_on, axis=1) # Sort columns and their data

    return df
