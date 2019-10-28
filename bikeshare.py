import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    global input_month
    global input_day
    
    month = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ['chicago', 'new york city', 'washington']
    while True:
        input_city = input("Please enter one of the following cities: chicago, new york city, washington").lower()
        if input_city not in city:
            print("Invalid input city")
            continue
        else:
            break

    # Get user input for month (all, january, february, ... , june)
    while True:
        input_month = input("Please select a month or all:").lower()
        if input_month not in month:
            print("Invalid input month")
            continue
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        input_day = input("Please select a day or all:").lower()
        if input_day not in day:
            print("Invalid input week day")
            continue
        else:
            break
    print('-'*40)
    return city, month, day

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df["Start hour"] = df["Start Time"].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common month:', common_month)

    # Display the most common day of week
    Common_day = df['day_of_week'].mode()[0]
    print('The most common day:', Common_day)

    # Display the most common start hour
    Common_hour = df['Start hour'].mode()[0]
    print('The most common start hour:'.format(Common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
      
    # Display most commonly used start station
    common_start_station = df.loc[:, "Start Station"].mode()[0]
    print('Most Common Start Station:', common_start_station)

    # Display most commonly used end station
    common_end_station = df.loc[:, "End Station"].mode()[0]
    print('Most Common End Station:', common_end_station)

    # Display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of start and end station trip:', start_end_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df["Trip Duration"] = df["End Time"] - df["Start Time"]
    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time:', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time:', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:', user_types)

    # Display counts of gender
    if "Gender" in df.columns:
        gender = df['Gender'].value_counts()
        print('Gender count:', gender)
    else:
        print("Gender information is not available")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest year of birth:', earliest_birth_year)
    else:
        print("Year of birth information is not available")
    
    if 'Birth Year' in df.columns:
        recent_birth_year = df['Birth Year'].max()
        print('most recent year of birth:', recent_birth_year)
    else:
        print("Year of birth information is not available")
    
    if 'Birth Year' in df.columns:
        common_birth_year = df['Birth Year'].mode()[0]
        print('most common year of birth', common_birth_year)
    else:
        print("Year of birth information is not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    user_input = input('\nWhat would you like to do next?\nPlease enter yes or no\n').lower()
    if user_input in ('yes', 'y'):
        i = 0
        while True:
            print(df.iloc[i:i+5])
            i += 5
            more_data = input('Would you like to see more data? Please enter yes or no: ').lower()
            if more_data not in ('yes', 'y'):
                break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
     
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
  main()