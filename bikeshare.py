import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        try:
            print('Please enter the city you would like to investigate: ')
            city = str(input('Choose between Chicago, New York City, and Washington.\n')).lower()
            if city == 'chicago' or city == 'new york city' or city == 'washington':
                print('Selecting data for {}'.format(city.title()))
                break
            else:
                print('{} is not a valid input!'.format(city))
        except KeyboardInterrupt:
            print('No input taken. Exiting program...')
            break
        finally:
            print('\n')
    
    print('-'*40)
            
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
    while True:
        try:
            print('Which month would you like to investigate?')
            month = str(input('Type Jan, Feb, Mar, Apr, May or Jun to select a month \nor type "all" to select all months. \n')).lower()
            if month in months:
                month = months.index(month) + 1
                break
            elif month == 'all':
                break
            else:
                print('\n{} is not a valid input! Please try again.'.format(month))
                continue
        except KeyboardInterrupt:
            print('No input taken. Exiting program...')
            break
        finally:
            print('\n')
        
    print('-'*40)
    
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    while True:
        try:
            print('Which day would you like to investigate?')
            day = str(input('Type Mon, Tue, Wed, Thu, Fri, Sat or Sun to select a day \nor type "all" to select all days. \n')).lower()
            if day in days:
                day = days.index(day)
                break
            elif day == 'all':
                break
            else:
                print('\n{} is not a valid input! Please try again.'.format(day))
                continue
        except KeyboardInterrupt:
            print('No input taken. Exiting program...')
            break
        finally:
            print('\n')
            
    print('Selected filters: city = {}, month = {}, day = {}'.format(city, month, day))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
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
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week']= df['Start Time'].dt.day_name()
    
    if month != 'all':
        df = df[df['month'] == month]
        
    if day != 'all':
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day = days[day]
        df = df[df['day_of_week'] == day]
        
    df = df.rename(columns={'Unnamed: 0': 'ID'})
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel, using the previously defined filters."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if month == 'all':
        mcomm_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        print('The most common month is: {}'.format(months[mcomm_month - 1]))
   
    if day == 'all':
        print('The most common day is: {}'.format(df['day_of_week'].mode()[0]))

    df['start_hour'] = df['Start Time'].dt.hour
    print('The most common start hour is: {}'.format(df['start_hour'].mode()[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular start station, end station and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('The most commonly used start station is: {}'.format(df['Start Station'].mode()[0]))
    print('The most commonly used end station is: {}'.format(df['End Station'].mode()[0]))

    df['Trip'] = df['Start Station'] + ' --> ' + df['End Station']
    print('The most common trip is: {}'.format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum() / 60 / 60 / 24
    total_travel_time = round(total_travel_time, 2)
    print('The total time traveled in the selected period is {} days.'.format(total_travel_time))

    average_travel_time = df['Trip Duration'].mean() / 60
    average_travel_time = round(average_travel_time, 2)
    print('The average time traveled in the selected period is {} minutes.'.format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    df['User Type'].fillna('None Specified', inplace=True)
    print('Breakdown of user numbers by type:\n')
    user_count = pd.Series(df.groupby(['User Type'])['ID'].count())
    print(user_count)

    if city != 'washington':
        df['Gender'].fillna('None Specified', inplace=True)
        gender_count = pd.Series(df.groupby(['Gender'])['ID'].count())
        print('\nBreakdown of user numbers by gender:\n')
        print(gender_count)
        
        print('\nBreakdown of user age:\n')
        print('The earliest year of birth is {}.'.format(int(df['Birth Year'].min())))
        print('The most recent year of birth is {}.'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is {}.'.format(int(df['Birth Year'].mode())))
        
    else:
        print('\nNo data on user gender and birth year available for this city.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Shows 5 rows of the Pandas DataFrame 'df' at a time and prompts user to continue."""
    
    pd.set_option('display.max_columns', 200)
    i=0
    choice = input('Would you like to see 5 lines of raw data? Type yes or no.\n').lower()
    while choice == 'yes' and i + 5 < df.shape[0]:
        print(df.iloc[i : i + 5])
        i += 5
        print('-'*40)
        choice = input('\nWould you like to see 5 more rows of raw data? Please type yes or no.\n').lower()
    
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
