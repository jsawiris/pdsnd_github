import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA=['all','january','febraury','march','april','may','june']

DAY_DATA=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

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
    cityname = ''
    while cityname.lower() not in CITY_DATA:
        cityname= input("\nWhich City you choose from the list (chicago, new york city, washington): \n")
        if cityname.lower() in CITY_DATA:
            city=CITY_DATA[cityname.lower()]

        else:
            print("Incorrect City data Provided")



    # get user input for month (all, january, february, ... , june)
    month_name=''
    while month_name.lower() not in MONTH_DATA:
        month_name=input("\nwhich month you choose (january,febraury,...,june) or type 'all' for all of the months : \n")
        if month_name.lower() in MONTH_DATA:
            month=month_name.lower()
        else:
            print("Incorrect Month data Provided")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_name=''
    while day_name.lower() not in DAY_DATA:
        day_name = input("\nWhich Day you choose (monday,tuesday,...,sunday) or type 'all' for all of the days :\n")
        if day_name.lower() in DAY_DATA:
            day=day_name.lower()
        else:
            print("Incorrect Day data Provided")


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

    df = pd.read_csv(city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month !='all':
        month = MONTH_DATA.index(month)

        df = df.loc[df['month'] == month]



    if day != 'all':
        df = df.loc[df['day_of_week'] == day.title()]



    return df


def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("\nThe common month is :\n"+str(MONTH_DATA[common_month].title()))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("\nThe Common Day of the Week is :\n"+common_day)


    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("\nThe common Hour is (24HH) :\n"+str(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #common_start_station = df['Start Station'].mode()[0]
    common_start_station = df['Start Station'].value_counts()
    print("\nThe common Start Station :\n"+str(common_start_station))



    # display most commonly used end station
    #common_end_station = df['End Station'].mode()[0]
    common_end_station = df['End Station'].value_counts()
    print("\nThe common End Station:\n"+str(common_end_station))

    # display most frequent combination of start station and end station trip
    #freq_comb = (df['Start Station']+" - "+df['End Station']).mode()[0]
    freq_comb = df.groupby(['Start Station','End Station']).size().idxmax()
    print("\nThe most frequent combination of start station and end station :\n"+str(freq_comb))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nThe total travel time (ndays HH:MI:SS):\n"+"("+str(total_travel_time)+") in Seconds.\n" +str(datetime.timedelta(seconds=int(total_travel_time))))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nThe mean Travel Time (ndays HH:MI:SS):\n"+str(datetime.timedelta(seconds=int(mean_travel_time))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("\nThe User types counts : \n"+str(user_type_count))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("\nThe Gender counts : \n"+str(gender_count))


    # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]

        print("\nThe Eraliest year of Birth is :\n"+str(int(earliest_birth)))
        print("\nThe Most Recent year of Birth is :\n"+str(int(recent_birth)))
        print("\nThe Common Year of Birth is :\n"+str(int(common_birth)))
    except KeyError:
        print("Dataset value error")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Display Data on user request
    Args:
    (DataFrame) df -Pandas DtaaFrame of the city,month,day filtered Data
    """
    view_data=input('\n would you like to view 5 rows of individual trip data?Enter yes or no\n').lower()
    start_loc=0
    while True:
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?:").lower()
        if view_data=='no':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
