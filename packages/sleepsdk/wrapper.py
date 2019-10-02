'''
sleepsdk.py is a package that compiles all the necessary methods for sleep manipulation regarding the data from the wearable 
device. Use the included final notebook to access the methods and test them. 

Last modified: September 7th. 2018
'''

__author__ = 'Bernard Wong'

import pandas as pd 
from datetime import datetime
import numpy as np
import csv 
import matplotlib.pyplot as plt
import seaborn as sns


class SleepAnalyzer():    

    def sleep_dataset_reader(str_dataset):
        ''' 
        This function takes a string of location of sleep csv and properly formats it to be read as a dataframe.

        Parameters: 
            String, which is the location of the sleep dataset
        Returns: 
            Returns a dataframe with proper format; dataframe does not extend past header columns
        '''
        # CURRENTLY MAKES MODIFICATIONS LINE BY LINE; RUN TIME CAN BE AVOIDED BY MODIFYING AS A DATAFRAME INSTEAD
        SLEEP_COL_START = 39 
        test = open(str_dataset,'r')
        lines = test.readlines()
        length_lines = [len(x.strip().split(';')) for x in lines]
        columns = max(length_lines) 
        list_rows = [] 
        list_sleep_phases = [] 
        for i in lines: 
            list_rows.append(i.strip().split(';'))
            list_sleep_phases.append(i.strip().split(';')[SLEEP_COL_START:]) 
        list_rows[0].extend(range(len(list_rows[0])-SLEEP_COL_START,columns-SLEEP_COL_START))
        list_rows[0] = list(map(str, list_rows[0]))
        for row in list_rows:
            row.extend(np.nan for x in range(columns-len(row))) # extends rows; for some, 'sleep cycle max' is less than 899
        headers = list_rows.pop(0)
        df = pd.DataFrame(list_rows,columns = headers,dtype='float')
        df.replace(r'^\s*$', np.nan, regex=True, inplace = True) # replaces all the empty spaces with NaN 
        df['list_numbers'] = list_sleep_phases[1:]
        return df
    
    def minimal_dataset_for_methods(df): # DATASET CLEANER
        '''
        This function does a general clean of the sleep dataframe for other methods(changes variables to proper types, drops
        unimportant columns)

        Parameter: 
            dataset, the sleep dataframe 
        Returns: 
            Returns a cleaner dataframe that has proper dtypes and less unnecessary columns 
        '''
        df = df.copy()
        df['Date'] =  pd.to_datetime(df['Date'], format='%d.%m.%Y') 
        # originally string, might be unnecessary? maybe convert to date; weekday vs weekend?
        df['Bedtime start Unix'] = pd.to_datetime(df['Bedtime start Unix'],unit='s') # originally string
        df['Bedtime end Unix'] = pd.to_datetime(df['Bedtime end Unix'],unit='s') # originally string 
        df = df.drop(['Bedtime start','Bedtime end'],axis=1) # unnecessary, since we already have bedtime unix's
        df = df[df['Debug info'] != 'Bedtime detection failed'] 
        # removes bedtime detection failed, rows lack info; line could be used to grab failing measurements in the future 
        str_list = list(filter(None, list(df.columns))) 
        # some columns have empty header and are empty, this gets rid of these columns 
        return df[str_list]

    def no_sleepcycles_df(self,df):
        ''' 
        Method used to split dataframe into initial interest columns first. Focuses on only the first few 
        columns, ignoring the sleep phases columns. 

        Parameter: 
            self, sleepsdk object
            df, sleep dataframe 
        Returns: 
            returns dataframe with columns of interest, everything should be converted to numbers 
        
        THINGS TO CONSIDER: Maybe don't drop bed time/wake time. Could be something important (sleeping late at night
        vs sleeping earlier, etc.)
        '''
        df = self.minimal_dataset_for_methods(df)
        area_interest = df.iloc[:,6:35].dropna(how='all', axis=1).drop('SleepMidPoint',axis=1)
        return area_interest.apply(pd.to_numeric)
    
    def naps_and_sleep(self,df):
        ''' 
        Method used to split dataframe into two dataframes; one focused on naps (sleep minutes less than 30 
        minutes) and one focused on concrete sleep (sleep minutes equal to or more than 30 minutes)

        Parameter: 
            sleep dataframe
        Returns: 
            returns two dataframes, first one being naps (naps dataframe), second one being sleep (sleep dataframe)
        
        POTENTIAL SOURCE: https://www.sleep.org/articles/how-long-to-nap/
        '''
        try:
            df = self.minimal_dataset_for_methods(df)
            naps = df[df['Sleep minutes']<30]
            sleep = df[df['Sleep minutes']>=30]
            return naps,sleep
            
        except:
            print('Error: MAKE SURE YOU HAVEN\'T RUN THIS DF THROUGH no_sleep_cycles_df')
    
    ### ~~~~~~~~~~~~~~~~ VISUALIZATION METHODS FOR SLEEP ~~~~~~~~~~~~~~~~ ### # add save as jpeg for each method 

    def corr_heatmap(self,df):
        '''
        Method that creates a correlational heatmap of correlation between variables in the dataframe. MAKE SURE TO PASS IN 
        A DATA FRAME THAT HAS NO SLEEP CYCLES (use no_sleep_cycles_df())

        Parameter: 
            sleep dataframe, formatted with no_sleep_cycles_df
        Returns: 
            seaborn plot, heatmap representing correlation between variables in dataframe 
        '''
        try: 
            df = self.no_sleepcycles_df(self,df)
            corr = df.corr()
            ax = sns.heatmap(
                corr, 
                vmin=-1, vmax=1, center=0,
                cmap=sns.diverging_palette(20, 220, n=200),
            )
            return ax
        except:
            print('ERROR WITH DATAFRAME FORMAT')
            
    def sleepduration_vs_sleepscore_plot(naps,sleep,interest_in_naps=False,interest_in_sleep=False):
        '''
        Visualization method used to plot sleep duration vs sleep score. Can select whether you want naps in the graph, sleep 
        in the graph, or both. It will produce a scatterplot with a legend denoting whether a data point is a nap or sleep 
        measurement. 

        Parameters: 
            naps, df from naps_and_sleep() method that contains sleep that lasted less than 30 minutes
            sleep, df from naps_and_sleep() method that contains sleep that lasted 30 minutes or more 
            interest_in_naps, boolean which states whether you wanted nap to be plotted or not 
            interested_in_sleep, boolean which states whetehr you want sleep to be plotted or not 
        Returns: 
            returns a matplotlib scatterplot with either the nap data, sleep data, or both. x axis will be sleep duration in 
            minutes and y axis will be sleep score 
        '''
        if (not interest_in_naps) and (not interest_in_sleep):
            return
        f, ax = plt.subplots()
        if (not interest_in_naps and not interest_in_sleep):
            ax.scatter('Sleep minutes', 'Sleep Score', data = df, color='g',label='All Sleep Measurements')
        if interest_in_sleep:
            ax.scatter('Sleep minutes', 'Sleep Score', data = sleep, color='r',label='Sleep')
            if not interest_in_naps:
                ax.plot(np.unique(sleep['Sleep minutes']), np.poly1d(np.polyfit(sleep['Sleep minutes'], sleep[
                    'Sleep Score'], 1))(np.unique(sleep['Sleep minutes'])),color='r')
        if interest_in_naps:
            ax.scatter('Sleep minutes', 'Sleep Score', data = naps, color='b',label='Naps')
            if not interest_in_sleep:
                ax.plot(np.unique(naps['Sleep minutes']), np.poly1d(np.polyfit(naps['Sleep minutes'], naps[
                    'Sleep Score'], 1))(np.unique(naps['Sleep minutes'])),color='b')
        ax.set_ylabel('Sleep Score')
        ax.set_xlabel('Sleep Duration (minutes)')
        ax.set_title('Sleep Duration vs. Sleep Score')
        leg = ax.legend()
        return ax

    def bedtimestart_vs_sleepscore_plot(naps,sleep,interest_in_naps=False,interest_in_sleep=False):
        '''
        Visualization method used to plot bedtime start and sleep score. Can select whether you want naps in the graph, sleep 
        in the graph, or both. It will produce a scatterplot with a legend denoting whether a data point is a nap or sleep 
        measurement. It will also draw a line of best fit so that you can better visualize patterns. 

        Parameters: 
            naps, df from naps_and_sleep() method that contains sleep that lasted less than 30 minutes
            sleep, df from naps_and_sleep() method that contains sleep that lasted 30 minutes or more 
            interest_in_naps, boolean which states whether you wanted nap to be plotted or not 
            interested_in_sleep, boolean which states whetehr you want sleep to be plotted or not 
        Returns: 
            returns a matplotlib scatterplot with either the nap data, sleep data, or both. x axis will be bedtime in EPOCH time 
            and y axis will be sleep score 
        
        # DOUBLE CHECK TIME MEASUREMENT
        '''
        f, ax = plt.subplots()
        if (not interest_in_naps and not interest_in_sleep):
            ax.scatter(df['Bedtime start Unix'].astype(int), 'Sleep Score', data = df,color='g',label='All Sleep Measurements')
        if interest_in_sleep:
            ax.scatter(sleep['Bedtime start Unix'].astype(int).sort_values(), 'Sleep Score', data = sleep,color='r',label='Sleep')
            ax.plot(sleep['Bedtime start Unix'].astype(int), np.poly1d(np.polyfit(sleep['Bedtime start Unix'].astype(
                int), sleep['Sleep Score'], 1))(np.unique(sleep['Bedtime start Unix'].astype(int))),color='r')
        if interest_in_naps:
            ax.scatter(naps['Bedtime start Unix'].astype(int).sort_values(), 'Sleep Score', data = naps,color='b',label='Naps')
            ax.plot(naps['Bedtime start Unix'].astype(int), np.poly1d(np.polyfit(naps['Bedtime start Unix'].astype(int), naps[
                'Sleep Score'], 1))(np.unique(naps['Bedtime start Unix'].astype(int))),color='b')
        ax.set_ylabel('Sleep Score')
        ax.set_xlabel('Time')
        ax.set_title('Bedtime Start vs. Sleep Score')
        leg = ax.legend()
        return ax

    def sleepphases_vs_sleepscore_plot(self, df):
        '''
        Visualization method used to plot number of minutes in each sleep phase and sleep score. Will have 3 different data
        colors which represent the three phases of sleep (REM, light, and deep). Plot will also contain 3 lines of best fit, 
        so that you can better visualize trends between amount of sleep in each sleep phase and its effect on sleep score. 

        Parameters:
            self, sleepsdk object
            df, sleep dataframe 
        Returns: 
            matplotlib scatterplot, where x axis is duration in sleep phase in minutes and y is sleep score. Plot will have a 
            legend with 3 different sleep phases, and graph will have 3 colors and a line of best fit for each sleep phase. 
        '''
        df_1 = self.minimal_dataset_for_methods(df)
        f, ax = plt.subplots()
        ax.scatter('REM minutes', 'Sleep Score', data = df_1,color='r',label='REM Phase')
        ax.plot(df_1['REM minutes'], np.poly1d(np.polyfit(df_1['REM minutes'], df_1[
            'Sleep Score'], 1))(df_1['REM minutes']),color='r')
        ax.scatter('Light minutes', 'Sleep Score', data = df_1, color='g',label='Light Phase')
        ax.plot(df_1['Light minutes'], np.poly1d(np.polyfit(df_1['Light minutes'], df_1[
            'Sleep Score'], 1))(df_1['Light minutes']),color='g')
        ax.scatter('Deep minutes', 'Sleep Score', data = df_1, color='b',label='Deep Phase')
        ax.plot(df_1['Deep minutes'], np.poly1d(np.polyfit(df_1['Deep minutes'], df_1[
            'Sleep Score'], 1))(df_1['Deep minutes']),color='b')
        ax.set_ylabel('Sleep Score')
        ax.set_xlabel('Duration (minutes)')
        ax.set_title('Duration of Sleep Phases vs. Sleep Score')
        leg = ax.legend()
        return ax

    def durationofsleep_vs_day_plot(df):
        '''
        Visualization method used to plot the duration of sleep (split up between REM, deep, light, and total) per day. 
        Plot will have a legend with 3 different sleep phases and total sleep, and graph will have 4 colors per day. 

        Parameters: 
            df, sleep dataframe 
        Returns:
            returns a matplotlib lineplot, where x are the dates and y is duration in minutes. Plot will have 4 measurements
            per day; total sleep, REM sleep, deep sleep, and light sleep. 
        '''
        pd.options.mode.chained_assignment = None
        interested = df[['Date','Sleep minutes','REM minutes','Light minutes','Deep minutes']]
        interested['Date'] = pd.to_datetime(interested['Date'],format="%d.%m.%Y")
        totals = interested.groupby('Date').sum().reset_index().sort_values('Date').iloc[1:]
        f, ax = plt.subplots(figsize=(20,10))
        ax.plot(totals['Date'],totals['Sleep minutes'],'-o',label='Total Sleep')
        ax.plot(totals['Date'],totals['REM minutes'],'-o',label='REM Sleep')
        ax.plot(totals['Date'],totals['Deep minutes'],'-o',label='Deep Sleep')
        ax.plot(totals['Date'],totals['Light minutes'],'-o',label='Light Sleep')
        ax.set_xticks(ticks=totals['Date'])
        ax.set_title('Duration of Sleep per Day')
        ax.set_ylabel('Duration (Minutes)')
        ax.set_xlabel('Date')
        leg = ax.legend()
        return ax
    
    def durationofsleep_vs_day_separated_plot(df):
        '''
        Visualization method used to plot the duration of sleep (split up between REM, deep, light, and total) per day. 
        Plot will have 4 different graphs, essentially fitting a graph on each of the 4 categories of sleep. First plot 
        will be total duration of sleep per day, second plot will be total duration of rem sleep per day, third plot 
        will be total duration of deep sleep per day, and fourth plot will be total duration of light sleep per day 

        Parameters: 
            df, sleep dataframe 
        Returns:
            returns a matplotlib lineplot, where x are the dates and y is duration in minutes. There will be 4 plots 
            in the plot, each one representing measurements for total sleep, REM sleep, deep sleep, and light sleep
            respectively. 
        '''
        f = plt.figure(figsize=(20,10))
        ax1 = f.add_subplot(411)
        ax2 = f.add_subplot(412)
        ax3 = f.add_subplot(413)
        ax4 = f.add_subplot(414)

        pd.options.mode.chained_assignment = None
        interested = df[['Date','Sleep minutes','REM minutes','Light minutes','Deep minutes']]
        interested['Date'] = pd.to_datetime(interested['Date'],format="%d.%m.%Y")
        totals = interested.groupby('Date').sum().reset_index().sort_values('Date').iloc[1:]
        ax1.plot(totals['Date'],totals['Sleep minutes'],'-o',label='Total Sleep')
        ax1.set_xticks(ticks=totals['Date'])
        ax1.set_title('Duration of Sleep per Day (Total)')
        ax1.set_ylabel('Duration (Minutes)')
        ax1.set_xlabel('Date')

        ax2.plot(totals['Date'],totals['REM minutes'],'-o',label='REM Sleep')
        ax2.set_title('Duration of Sleep per Day (REM)')
        ax2.set_xticks(ticks=totals['Date'])
        ax2.set_ylabel('Duration (Minutes)')
        ax2.set_xlabel('Date')

        ax3.plot(totals['Date'],totals['Deep minutes'],'-o',label='Deep Sleep')
        ax3.set_xticks(ticks=totals['Date'])
        ax3.set_title('Duration of Sleep per Day (Deep)')
        ax3.set_ylabel('Duration (Minutes)')
        ax3.set_xlabel('Date')

        ax4.plot(totals['Date'],totals['Light minutes'],'-o',label='Light Sleep')
        ax4.set_xticks(ticks=totals['Date'])
        ax4.set_title('Duration of Sleep per Day (Light)')
        ax4.set_ylabel('Duration (Minutes)')
        ax4.set_xlabel('Date')

        plt.subplots_adjust(hspace = 0.5)
        