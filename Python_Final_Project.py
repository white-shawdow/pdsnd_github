from asyncio.base_futures import _FINISHED
from asyncio.windows_events import NULL
from cgi import test
from dis import findlinestarts
from email import header
from operator import index, truediv
from re import I
import pandas as pd
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }
Months = ['january','february','march','april','may','june']
Days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('\nHello! Let\'s explore some US bikeshare data!\nYou will need to select a city, month, and day to analyze \n\n')
    print('Cities to choose from: New York City, Chicago, or Washington\nMonth can be "all" or any month between January and June...Same rules goes for days\n')
    
    #Gathers user input (city, month, and day)
    while True:
        try:
            city, month, day = input('Enter City, Month, Day with a comma in-between! ').strip().lower().split(',')
            city= city.strip().lower()
            month= month.strip().lower()
            day= day.strip().lower()
            print('-'*40)
            break
        except:
            print('\nMake sure to include city, month, and day!\n')    
   
    #Test user input and requests changes if necessary  
    while True:   
        if CITY_DATA.get(city,'error') != 'error':
            if month == 'all' or month in Months:
                if day == 'all' or day in Days:
                    break
                else:
                    day = input('\nChoose specific day or "all": ').strip().lower()
                    print('Updated selection: ','')
                    print(city, month, day)
                    print('-'*40)
            else:
                month = input('\nChoose specific month or "all": ').strip().lower()
                print('Updated selection: ','')
                print(city, month, day)
                print('-'*40)
        else:
            city = input('\nChoose New York City, Chicago, or Washington:').strip().lower()
            print('Updated selection: ','')
            print(city, month, day)
            print('-'*40)

    return city,month,day                

def Load_Data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # loads data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracts month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    
    # filters by month
    if month != 'all':
        #index of the months list used to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filters by month to create the new dataframe
        df = df[df['month'] == month]

    # filters by day of week if applicable
    if day != 'all':
        # filters by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # displays the most common month
    mode_month = Months[df['month'].mode()[0]-1]
    
    # displays the most common day of week
    most_common_day = df['day_of_week'].mode()[0]

    # displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    
    print('The most common month is: {0}\nThe most common day is: {1}\nThe most common start hour is: {2}'.format(mode_month,most_common_day,most_common_hour).title())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station
    Start_Station = df['Start Station'].mode()[0]

    # displays most commonly used end station
    End_Station  = df['End Station'].mode()[0]

    # displays most frequent combination of start station and end station trip
    df['Start & End Station'] = df['Start Station'] + ' and ' + df['End Station'] 
    Most_Frequent_Combo = df['Start & End Station'].mode()[0]
    
    print('The most common start station is: {0}\nThe most common end station is: {1}\nThe most common combo is: {2}'.format(Start_Station,End_Station,Most_Frequent_Combo))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Finds total travel time and mean travel time
    start = pd.to_datetime(df['End Time'])
    finish = pd.to_datetime(df['Start Time'])
    
    Total_Sum = (start-finish).sum().round('D').days
    Mean_Trip = (start-finish).mean().round('5min')


    print('The total duration of all trips was: {0} days\nThe average trip lasted: {1} minutes'.format(Total_Sum,Mean_Trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type.to_string(),'\n')
    
    # Displays counts of gender
    gender_test = 'Gender' in df.columns
    if gender_test is True:
        gender = df['Gender'].value_counts()
        print(gender.to_string(),'\n')
    else:
        print('No data on user gender available.\n')
        
    # Displays earliest, most recent, and most common year of birth and converts Birth Year column to int
    Birth_test = 'Birth Year' in df.columns
    
    if Birth_test is True:
        df['Birth Year'] = df['Birth Year'].astype(pd.Int64Dtype())
        
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('The earliest birth was in year: {0} \nThe most recent birth was in year: {1}\nThe most common birth was in the year: {2}'.format(earliest_birth,most_recent_birth,most_common_birth))
    else:
        print('No data on birth year available.')
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data from city file 5 rows at a time."""
    
    #Loop allows user to view raw data or exit file
    response = input('Would you like to see the Raw data? Enter yes or no. \n').lower().strip()
    i = 5
    while True:            
        if response == 'no':
            break
        elif response == 'yes':
            print(df.iloc[i-5:i])
            response = input("Would you like to see more? Enter yes or no ").lower().strip() 
            i += 5
        else:
            response = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower().strip()
            
def main():
    while True:
        city, month, day = get_filters()
        df = Load_Data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.')

        #Loop asks user if they would like to repeat exercise or exit. 
        while True:            
            if restart.lower().strip() == 'yes':
                break
            elif restart.lower().strip() == 'no':
                print('\nGoodbye!')
                exit()
            else:
                restart = input('You must choose yes or no. \n').lower().strip()               

if __name__ == "__main__":
	main()