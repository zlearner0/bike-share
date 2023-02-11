import time
from datetime import timedelta
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

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Choose the city you are interested in; chicago, new york city or washington: ')
        cities=['chicago','new york city','washington']
        city=city.strip().lower()
        if city not in cities:
            print('please enter city from the given cities only')
        else:
            break 

    # get user input for month (all, january, february, ... , june)
    while True: 
        month = input('Enter all or first 3 letters of a specific month from jan to june i.e. jan: ')
        months = ['jan','feb','mar','apr','may','jun']
        month = month.strip().lower()
        if month == 'all':
            break
        elif month not in months:
            print('please enter month word as 3 letters like feb or apr and months range from jan to june')
        else:
            month = months.index(month)+1
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:         
        day = input('Enter all or first 3 letters of a specific day i.e. mon: ')
        days = ['mon','tue','wed','thu','fri','sat','sun']
        day = day.strip().lower()
        if day == 'all':
            break
        elif day not in days:
            print('please enter day word as 3 letters like thu or tue')
        else:
            day = days.index(day)+1
            break
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

    df = df.drop(df.columns[[0]],axis = 1)   # delete first column as it is useless

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['hour'] = df['Start Time'].dt.hour

    df['month'] = df['Start Time'].dt.month

    df['day_no'] = df['Start Time'].dt.day_of_week

    if month != 'all':
        
        df = df[df['month'] == month]
    
    if day != 'all':
        
        df = df[df['day_no'] == day]

    
    if df.empty:
        print('No trips for this duration, please try another time frame')
        get_filters()


    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    months = ['January','February','March','April','May','June']
    common_month = months[common_month -1]
    print('the most common month is {}.'.format(common_month))

    # display the most common day of week
    common_day = df['day_no'].mode()[0]
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    common_day = days[common_day-1]
    print('the most common day of week is {}.'.format(common_day))

    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is {}.'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}.'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    frequent_trip = df.groupby(['Start Station','End Station']).size().reset_index(name='Trips No.').max()
    print('The most frequent start/end trip:\n{}.'.format(frequent_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    total_travel_time= timedelta(seconds=total_travel_time)
    print('Total travel time is {}.'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    mean_travel_time= timedelta(seconds=mean_travel_time)
    print('Mean travel time is {}.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users_type_counts = df['User Type'].value_counts()
    print('Counts of users types are:\n{}.'.format(users_type_counts))

    if 'Gender' in df.columns:
     # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender are:\n{}.'.format(gender_counts))

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('The most earliest birth year is {}.'.format(int(earliest_birth_year)))

        recent_birth_year = df['Birth Year'].max()
        print('The most recent birth year is {}.'.format(int(recent_birth_year)))

        common_year_of_birth= df['Birth Year'].mode()[0]
        print('The most common year of birth is {}.'.format(int(common_year_of_birth)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def row_data(df):
    '''presents the raw data in 5 rows group each time upon request'''
    # here we present for the user the raw data of the trips if the user likes to
    n = 5
    while True:
        row_data_requrest = input('Do you like to see more of trips row data for US bikeshare? please type in yes or no?  ')
        if row_data_requrest.lower() == 'yes' and n <= len(df.index)-5:
            print(df.iloc[n-5:n])
            n += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        row_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


