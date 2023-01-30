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
    city_choices = ["chicago", "new york city", "washington"]
    while True:
        city= input('Chose one city from {} :? '.format(city_choices)).lower()
        if city in city_choices:  
            break
        else:
            print('Your city choice - {} - was not a correct one, please try again'.format(city))
                     

    # get user input for month (all, january, february, ... , june)
    month_choices = ["all", "january", "february", "march", "april", "may", "june"]
    while True:
        month = input('Chose a month from these options {} : ? '.format(month_choices)).lower()
        if month in month_choices:  
            break
        else:
            print('Your month choice - {} - was not a correct one, please try again'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_choices = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while True:
        day = input('Chose a day from these choices {} : ? '.format(day_choices)).lower()
        if day in day_choices:  
            break
        else:
            print('Your day choice - {} - was not a correct one, please try again'.format(day))

    print('-'*40)
    return city, month, day
 
def show_raw_data(raw):
"""
    Asks user to specify if they want to see raw data or not.
    Added controls on proper use of yes and no
"""
    row = 0
    print(raw[row:row+5])
    row += 5
    while True:
        view_more=input('Do you wish to view more raw data? (yes/no)').lower()
        if view_more not in ['yes','no']:
            print("\nInvalid input. Please enter yes or no.\n")
            continue
        if view_more == 'yes' and row+5<raw.shape[0]:
            print(raw[row:row+5])
            row += 5
            continue
        if view_more == 'no':
            break
        else:
            break
   

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
    df=pd.read_csv(CITY_DATA[city])
    #print(df.head(5))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    print('\nYour reports for city:{}, month:{}, day:{} report are\n'.format(city, month, day))
    #RAW DATA MISSING PART CODE#
    while True:
        raw_data=input('\nDo you want to see some raw data before we start applying the filters? (yes/no)').lower()
        if raw_data=='yes':
           show_raw_data(df)
           break
        if raw_data=='no':
           break        
    #OLD CODE PRE-RAWDATA#
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        #print(df.head(2), 'if month')
    #print('month ', month)
    if day != 'all':
       #print(df['day_of_week'], day.title())
       df = df[df['day_of_week'] == day.title()]
       #print(df.head(2), 'if day')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]
    print('Most popular month is: {}'.format(months[popular_month-1]))
    

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day is: {}'.format(popular_day))
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start statio
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station is: {}'.format(popular_start_station))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station is: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_trip=df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most popular combination is: {}'.format(popular_trip))
    
    # display total time report execution
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=sum(df['Trip Duration'])
    total_travel=timedelta(seconds=total_travel_time)
    print('Total travel time = {}'.format(total_travel))

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    mean_travel=timedelta(seconds=mean_travel_time)
    print('Average travel time = {}'.format(mean_travel))
    
    # display total time report execution
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types_count=df['User Type'].value_counts()
    print('Count of user types: {}'.format(user_types_count))
    try:
        # Display counts of gender
        gender_types_count=df['Gender'].value_counts()
        print('Count of Genders: {}'.format(gender_types_count))

        # Display earliest, most recent, and most common year of birth
        earliest=df['Birth Year'].min()
        most_recent=df['Birth Year'].max()
        most_common=df['Birth Year'].mode()
        print('The Earliest date of birth is {}, the latest is {} and the most common is {}'.format(earliest,most_recent,most_common))
    except KeyError:
        print('Washington has no data for Gender and Birth')
        
    # display total time report execution    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    x = True
    while x == True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart not in ['yes','no']:
                print("\nInvalid input. Please enter yes or no.\n")
                continue
            if restart == 'yes': 
                break
            if restart == 'no':
                print('Thanks for all!')
                x = False
                break
        
              
if __name__ == "__main__":
	main()