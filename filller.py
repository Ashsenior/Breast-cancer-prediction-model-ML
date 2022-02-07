'''
    Functions inside the header file to use >>>

    ready_data() function for cleaning and filling data from start to end
    ready_data(csv_file_name,num_method="median",time_series=False) returns X,Y

    get_time_series() function to get time series dataframe and convert it into numerical form
    get_time_series(csv_file)

    scale() scale function scales your data and returns dataframe with all scaled columns
    scale(df)

    remove_least_correlated_columns() function removes all least correlated columns with the label with a factor
    remove_least_correlated_columns(df,label,factor=3)

'''
import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler

def ready_data(csv_file_path,label,num_method="median",time_series=False):
    # Loading the csv file 
    df = pd.read_csv(csv_file_path,low_memory=False)
    # If time series then get date column and parse dates as datetime64
    if time_series:
        datec = get_date_column(csv_file_path)
        df = pd.read_csv(csv_file_path,low_memory=False,parse_date=[datec])
        df.sort_values(by=[datec],inplace=True,ascending=True)
    # Converting Objects into pandas Category 
    for column ,content in df.items():
        if pd.api.types.is_string_dtype(content):
            df[column] = content.astype("category").cat.as_ordered()
    # Filling the missing values and droping rows with empty label
    for column,content in df.items():
        if pd.api.types.is_categorical_dtype(content):
            df[column] = pd.Categorical(content).codes+1
        elif pd.api.types.is_datetime64_dtype(content):
            df[column] = content.dropna(axis=0,inplace=True)
        elif pd.api.types.is_numeric_dtype(content):
            if pd.isnull(content).sum():
                df[column+'_is_missing'] = pd.isnull(content)
                print(f"Column {column}_is_missing was added to your DataFrame ")
                if num_method=='median':
                    df[column] = content.fillna(content.median())
                else :
                    df[column] = content.fillna(content.mean())
    # Converting DateTime64 into numerical values 
    if time_series:
        df.Year = df[datec].dt.year
        df.Month = df[datec].dt.month
        df.Day = df[datec].dt.day
        df.DayOfWeek = df[datec].dt.dayofweek
        df.DayOfYear = df[datec].dt.dayofyear
        df.drop(datec,axis=1,inplace=True)
        print("Columns Year, Month, Day, DayOfWeek, DayOFYear were added to your DataFrame ")
    # Splitting Dataframe into label and features 
    Y = df[label]
    X = df.drop(label,axis=1)
    scaled_df = scale(X)
    return scaled_df,Y

def get_time_series(csv_file_path):
    # Get datetime column from the dataframe 
    datec = get_date_column(csv_file_path)
    # Load dataframe from csv and parse datetime column as DateTime64
    df = pd.read_csv(csv_file_path,low_memory=False,parse_date=[datec])
    # Sort dataframe acording to date
    df.sort_values(by=[datec],inplace=True,ascending=True)
    # Drop rows with null datetime column
    for label,content in df.items():
        if pd.api.type.is_datetime64_dtype(content):
            df[label] = content.dropna(axis=0,inplace=True)
    # Convert date time into numerical data 
    df.Year = df[datec].dt.year
    df.Month = df[datec].dt.month
    df.day = df[datec].dt.day
    df.DayOfWeek = df[datec].dt.dayofweek
    df.DayOfYear = df[datec].dt.dayofyear
    df.drop(datec,axis=1,inplace=True)
    print("Columns Year, Month, Day, DayOfWeek, DayOFYear were added to your DataFrame ")
    return df

def scale(df):
    # Scales the dataframe with StandardScaler
    scaler = StandardScaler()
    scaled_df = pd.DataFrame(scaler.fit_transform(df),columns=df.columns)
    return scaled_df

def remove_least_correlated_columns(df,label,factor=3):
    least_corr = []
    count=0
    # Defining the negative and positive limit for deletion of Least correlated columns
    neg_limit = df.corr()[label][df.corr()[label]<0].mean()/factor
    pos_limit = df.corr()[label][df.corr()[label]>0].mean()/factor
    # Checks for the column within the limits 
    for i in range(len(df.corr()[label])):
        val=df.corr()[label][i]
        if neg_limit<val<pos_limit:
            least_corr.append(df.corr().index[i])
            print(f" Column **{df.corr().index[i]}** was removed with correlation {val} with {label}")
            count+=1;
    if count==0:
        print(" No column was removed from DataFrame")
    # Removing the least correlated columns
    df = df.drop(least_corr,axis=1)
    return df

def get_date_column(csv_file_path):
    # Loads the dataframe 
    df = pd.read_csv(csv_file_path,low_memory=False)
    # If the column name contains "date" then return the column 
    for label,content in df.items():
        if pd.api.types.is_string_dtype(content):
            if "date" in label.lower():
                datec = column
    return datec