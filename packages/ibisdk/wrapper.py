
'''
ibisdk.py is a package that compiles all the necessary methods for IBI manipulation regarding the data from the wearable 
device. Use the included final notebook to access the methods and test them. 

Last modified: September 7th. 2018
'''

__author__ = 'Bernard Wong'


import pandas as pd 
from datetime import datetime
import numpy as np
import csv 
import matplotlib.pyplot as plt
# from pandas.plotting import register_matplotlib_converters (MIGHT BE NEEDED IN THE FUTURE)
import seaborn as sns
import warnings
import random
pd.options.mode.chained_assignment = None
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

class IBIAnalyzer():
    def ibi_dataset_reader(str_dataset):
        '''
        This function takes a string of location of ibi csv and properly formats it to be read as a dataframe.

        Parameters: 
            String, which is the location of the ibi dataset
        Returns: 
            Returns a dataframe with proper format
        '''
        df = pd.read_csv(str_dataset,sep=';')
        df['Date'] = pd.to_datetime(df['Date'],format="%d.%m.%Y")
        return df
    
    def markov_chain(df):
        '''
        A Markov chain is a mathematical system that measures the probability of transitions to different states
        based on certain probabilistic rules. This method creates a markov chain for validity; it calculates the 
        probability of the next data point being valid/invalid if the first point is valid, and calculates the 
        probability of the next data point being valid/invalid if the first point is invalid. 

        Parameters: 
            df, the IBI dataframe 
        Returns: 
            returns a dataframe representing all the information from a markov chain. The rows represent what 
            the initial validity is, and the columns represent the probability of the following data point being
            valid or invalid. 
        '''
        def validity_func(x):
            if x!= 1:
                return False
            else:
                return True
        validity_counts = pd.DataFrame({'initial':df['Validity'].apply(validity_func)})
        validity_counts['next'] = validity_counts['initial'].shift(-1)
        validity_counts = validity_counts[:-1]
        
        counts = pd.DataFrame(validity_counts['initial'].value_counts()).reset_index()
        counts.columns = ['initial','total_count']
        
        result = pd.DataFrame(validity_counts.groupby('initial')['next'].value_counts())
        result.columns = ['count']
        result = result.reset_index()
        result = result.merge(counts)
        result['proportion'] = result['count']/result['total_count']
        return result.pivot(index='initial',columns = 'next',values = 'proportion')

    def hrv_df(df):
        '''
        This function takes the IBI dataframe and transforms it into a dataframe used for various 
        HRV methods. 

        Parameters:
            df, the IBI dataframe 
        Returns: 
            returns a dataframe with 3 columns; IBI, NEXT IBI, and UTC time. This is primarily 
            used by other methods involving hrv. 
        '''
        tester = df[['IBI','UTC time']]
        tester['next IBI'] = tester['IBI'].shift(-1)
        tester = tester[:-1]
        return tester
    
    def poincare_plot(self, df):
        '''
        This is the start of a visualization method to create a poincare plot of hrv. Currently it is 
        missing the oval of best fit, as well as the x and y axes of the oval. 

        Parameters:
            self, ibisdk object
            df, ibi dataframe 
        Returns: 
            returns a matplotlib scatter plot, where x is the IBI in milliseconds and y is the IBI in 
            milliseconds following the following the IBI represented with the x coordinate 
        '''
        plot_df = self.hrv_df(df)
        return plot_df.plot(kind = 'scatter', x='IBI',y='next IBI')
    
    def rmssd(self, ibi_df):
        '''
        This method calculates the RMSSD, which is the root mean square of successive RR interval 
        differences. This is one of the measurements of HRV. 

        Parameters:
            self, ibisdk object
            df, ibi dataframe
        Returns: 
            returns a float, which is the RMSSD of the IBIs in the dataframe
        '''
        df = self.hrv_df(ibi_df)
        difference = df['IBI']-df['next IBI']
        difference_squared = difference**2
        mean_of_differences = np.mean(difference_squared)
        sqrt_item = np.sqrt(mean_of_differences)
        # np.sqrt(np.mean((tester['IBI']-tester['next IBI'])**2))
        return sqrt_item

    def sdnn(self, ibi_df):
        '''
        This method calculates the SDNN, which is the standard deviations of the IBI. This is one of 
        the measurements of HRV. 

        Parameters:
            self, ibisdk object
            df, ibi dataframe 
        Returns: 
            returns a float, which is the SDNN of the IBIs in the dataframe 
        '''
        df = self.hrv_df(ibi_df)
        return np.std(df['IBI'])

    def nn50(self, ibi_df):
        '''
        this calculates NN50, the number of NN intervals where the interval difference is more than 50 
        milliseconds. This is one of the measurements of HRV.

        Parameters:
            self, ibisdk object
            df, ibi dataframe 
        Returns:
            returns an integer, which is the NN50 of the IBIs in the dataframe 
        '''
        df = self.hrv_df(ibi_df)
        differences = np.abs(df['next IBI']-df['IBI'])
        return sum(differences > 50 )

    def pnn50(self, ibi_df):
        '''
        This calculates the pnn50, the proportion of NN intervals where the interval difference is more than
        50 milliseconds. This is one of the measurements of HRV. 

        Parameters:
            self, ibisdk object
            df, ibi dataframe
        Returns:
            returns an integer, which is the PNN50 of the IBIs in the dataframe 
        '''
        df = self.hrv_df(ibi_df)
        num = self.nn50(self,df)
        denom = len(df)+1
        return num/denom

    ### ~~~~~~~~~~~~~~~~ VISUALIZATION METHODS FOR IBI ~~~~~~~~~~~~~~~~ ### # add save as jpeg for each method 
    def ibi_vs_time_plot(df, interest_in_valid_one = True, interest_in_valid_two = True, interest_in_valid_three = True):
        '''
        A visualization method that creates a scatter plot of  IBI over UTC time (represented in epochs). The x axis is time 
        and the y axis is IBI in milliseconds. You can choose whether to plot IBIs with validity 1, 2, or 3, or any combination 
        together. 

        Parameters:
            df, the IBI dataframe
            interest_in_valid_one, boolean which represents interest in IBIs with validity 1 (most valid)
            interest_in_valid_two, boolean which represents interest in IBIs with validity 2 (valid) 
            interest_in_valid_three, boolean which represents interest in IBIs with validity 3 (slightly valid)
        Returns: 
            returns a matplotlib scatter plot with x's representing datapoints. A legend will show what each color represents
            (validities), x axis will be epoch time in UTC, and y axis will be padded IBIs in milliseconds. 
        '''
        if (not interest_in_valid_one) and (not interest_in_valid_two) and (not interest_in_valid_three):
            return
        valid_data = df[(df['Validity']==1)|(df['Validity']==2)|(df['Validity']==3)]
        valid_data_v2 = valid_data[['Validity','Padded IBI','UTC time']]
        valid_data_summary = valid_data_v2.groupby('UTC time').mean().reset_index()
        valid_data_summary['Validity'] = valid_data_summary['Validity'].round()
        valid_sum_1 = valid_data_summary[valid_data_summary['Validity']==1]
        valid_sum_2 = valid_data_summary[valid_data_summary['Validity']==2]
        valid_sum_3 = valid_data_summary[valid_data_summary['Validity']==3]
        f, ax = plt.subplots(figsize=(15,15))
        if interest_in_valid_one:
            ax.scatter('UTC time', 'Padded IBI', data = valid_sum_1,color='r',label='Validity 1',marker='x',linewidths=.1)
        if interest_in_valid_two:
            ax.scatter('UTC time', 'Padded IBI', data = valid_sum_2,color='g',label='Validity 2',marker='x',linewidths=.1)
        if interest_in_valid_three:
            ax.scatter('UTC time', 'Padded IBI', data = valid_sum_3,color='b',label='Validity 3',marker='x',linewidths=.1)
        plt.xticks(np.arange(1543351058, 1544628851, 100000.0))
        ax.set_ylim([250,2100])
        ax.set_ylabel('Padded IBI')
        ax.set_xlabel('UTC time')
        ax.set_title('Padded IBI over Time')
        leg = ax.legend()
        return ax
    
    def valid_ibi_proportion_plot(df,fitted=True, regular = True,save_as_jpg = False):
        '''
        Visualization method that creates a lineplot of the proportion of IBIs that are valid each day. The x axis 
        are dates in the dataframe, and the y axis is the proportion of IBIs valid during that date. You can choose 
        whether to only have a fitted graph (where x axis will only be from lowest to highest proportion of IBIs for 
        that specific dataframe), only have a regular graph (where x axis will be from 0 to 1), or both. 

        Parameters: 
            df, IBI dataframe 
            fitted, boolean which represents whether you want to see a plot of a fitted graph (fitted to df)
            regular, boolean which represents whether you want to see a plot of a regular graph (x axis 0 to 1)
            save_as_jpg, boolean which represents whether you want the plot to be saved as an external jpg or not
        Returns:
            returns matplotlib line plot(s), which represent the proportion of IBIs that are valid each day. X axis is
            date, y axis is proportions.
        '''
        if (not fitted) and (not regular):
            return 
        ### could potentially be separated out into a method, although no other methods use this df 
        ibi_data = df.copy()
        ibi_data['Date'] = pd.to_datetime(ibi_data['Date'],format="%d.%m.%Y")
        total_num = ibi_data.groupby('Date')[['Validity']].count().reset_index()
        total_num.columns = ['Date','Total Count']

        total_num_1 = ibi_data[ibi_data['Validity']==1].groupby('Date')[['Time']].count().reset_index()
        total_num_1.columns = ['Date','Total Count Val 1']
        total_num_1 = total_num_1.sort_values('Date')

        combined = total_num.merge(total_num_1)
        combined['Ratio'] = combined['Total Count Val 1']/combined['Total Count']
        combined['Unix'] = combined['Date'].astype(np.int64)
        ### could potentially be separated out into a method, although no other methods use this df 
        
        if fitted == regular: 
            f = plt.figure(figsize=(15,10))
            ax = f.add_subplot(211)
            ax2 = f.add_subplot(212)
            plt.subplots_adjust(hspace = 0.3)

            ax.plot(combined['Date'],combined['Ratio'],'-o')
            ax.set_title('Fitted Lineplot of the Proportion of IBI\'s that have Validity 1');
            ax.set_xlabel('Date')
            ax.set_ylabel('Proportion')

            ax2.plot(combined['Date'],combined['Ratio'],'-o')
            ax2.set_ylim(0,1)
            ax2.set_title('Lineplot of the Proportion of IBI\'s that have Validity 1');
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Proportion')
            return ax2
        else: 
            if fitted: 
                f, ax = plt.subplots(figsize=(15,5))
                ax.plot(combined['Date'],combined['Ratio'],'-o')
                ax.set_title('Fitted Lineplot of the Proportion of IBI\'s that have Validity 1');
                ax.set_xlabel('Date');
                ax.set_ylabel('Proportion')
                ax.set_xticks(ticks=combined['Date'])
                ax.tick_params(rotation = 45, size = 10)
                return ax 
            else: 
                f, ax = plt.subplots(figsize=(15,5))
                ax.plot(combined['Date'],combined['Ratio'],'-o')
                ax.set_ylim(0,1)
                ax.set_title('Lineplot of the Proportion of IBI\'s that have Validity 1');
                ax.set_xlabel('Date');
                ax.set_ylabel('Proportion');
                ax.set_xticks(ticks=combined['Date']);
                ax.tick_params(rotation = 45, size = 10)
                return ax

    def boxplot_style_one(df):
        '''
        Visualization method that creates a plot of boxplots for each day in the dataframe. The boxplots represent the 
        IBIs each day and provide valuable information about the IQR, median, and outliers. 

        Parameters:
            df, the IBI dataframe 
        Returns:
            returns a plot with boxplots that include information about the IQR, median, and outliers. The x axis is 
            date while the y axis is IBI in milliseconds.
        '''
        ### repeat, consider making method 
        total_num_1 = df[df['Validity']==1]
        data = [] 
        for x in total_num_1['Date'].unique():
            data.append(total_num_1[total_num_1['Date']==x]['Padded IBI'].tolist())
        ### repeat, consider making method 
        f, ax = plt.subplots(figsize=(20,15))
        labels = [str(x)[:10] for x in total_num_1['Date'].unique()]
        ax.boxplot(data,patch_artist=True,labels=labels)
        ax.set_title('Boxplots of Padded IBI\'s w/ Validity 1 Organized by Date')
        ax.set_xlabel('Date')
        ax.set_ylabel('IBI (milliseconds)')
        return ax
    
    def boxplot_style_two(df):
        '''
        Visualization method that creates a plot of boxplots for each day in the dataframe. The boxplot represents the
        IBIs each day and provide valuable information about the IQR and median. It also includes a line plot connecting 
        the medians of each day so that you can easily see general trends day to day.

        Parameters:
            df, the IBI dataframe 
        Returns:
            returns a plot with boxplots that include information about the IQR, median, and outliers. The x axis is 
            date while the y axis is IBI in milliseconds. The boxplots are connected 
        '''
        ### repeat, consider making method 
        total_num_1 = df[df['Validity']==1]
        data = [] 
        for x in total_num_1['Date'].unique():
            data.append(total_num_1[total_num_1['Date']==x]['Padded IBI'].tolist())
        ### repeat, consider making method 
        medians = total_num_1.groupby('Date')[['Padded IBI']].median().reset_index()
        f, ax = plt.subplots(figsize=(20,10))
        labels = [str(x)[:10] for x in total_num_1['Date'].unique()]
        ax.boxplot(data,labels=labels,showfliers=False)
        ax.plot(range(1,len(medians)+1),medians['Padded IBI'],'-o')
        ax.set_title('Boxplots of Padded IBI\'s w/ Validity 1 Organized by Date');
        ax.set_xlabel('Date');
        ax.set_ylabel('IBI (milliseconds)');
        plt.savefig('box_plot_v2.jpg')
        return ax

    def line_plot_df(df):
        '''
        Method used to clean up and organize the IBI dataframe in order to be processed in the 
        lineplot_of_valid_ibis method. It creates an additional column classifying the time that 
        IBI is being measured and modifies some of the existing columns and changes them to 
        proper formats.

        Parameters:
            df, IBI dataframe 
        Returns:
            returns a modified dataframe that is used by lineplot_of_valid_ibis
        '''
        valid_ibi = df.sort_values('UTC time')[df['Validity']==1]
        valid_ibi['UTC time'] = valid_ibi['UTC time'].astype(int)
        valid_ibi['UTC time (converted)'] = valid_ibi['UTC time'].apply(
            lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
        hours = pd.to_datetime(valid_ibi['UTC time (converted)']).apply(lambda x: x.hour)
        def morning_afternoon_evening_night(x):
            if 5<=x<=11: # 7 hours 
                return 'morning'
            elif 12<=x<=16: # 5 hours
                return 'afternoon'
            elif 17<=x<=21: # 5 hours
                return 'evening'
            else: # 7 hours
                return 'night'
        valid_ibi['time frame'] = hours.apply(morning_afternoon_evening_night)
        valid_ibi['time according to UTC time'] = pd.to_datetime(valid_ibi['UTC time (converted)']).apply(
            lambda x: str(x.time()))
        return valid_ibi
        
    def lineplot_of_valid_ibis(self, df,time = None, number = 300):
        '''
        A visualization method used to create a lineplot of the first few valid IBIs during a randomized period of time. 
        The x axis will be the random period of time represented in epoch time, and the y axis will be the IBI in milliseconds. 
        You can specify which time you want to be in (morning, evening, or night) and how many you want represented, but 
        the graph itself will randomly select a time. 

        Parameters:
            self, ibisdk object
            df, IBI dataframe 
            time, string that is either morning, afternoon, evening, or night. Represents time that data will be from, if no 
                time is specified then a random time is selected
            number, an integer that represents how many of the IBIs you want graphed. If no number is specified, default is 300
                IBI datapoints 
        Returns:
            returns a line plot representing the IBIs during the random point of time. The line plot is meant to visualize the 
            pattern of IBIs; a healthy IBI should have multiple spikes which should be easy to visualize with this chart. 
        '''
        valid_ibi = self.line_plot_df(df)
        dates = valid_ibi['Date'].unique()
        random_date = random.choice(dates)
        if time == None:
            random_time = random.choice(['morning','afternoon','evening','night'])
        else:
            random_time = time
        random_df = valid_ibi[(valid_ibi['Date'] == random_date) & (valid_ibi['time frame'] == random_time)]
        random_interest = random_df[:number]
        f = plt.figure(figsize=(20,10))
        ax = f.add_subplot(111)
        ax.plot(random_interest['time according to UTC time'],random_interest['Padded IBI'],'-o')
        ax.set_title('Lineplot of the first 100 Valid IBIs in the '+str(random_time)+' of '+str(random_date))
        ax.set_xlabel('Epoch time')
        ax.set_xticklabels(labels = random_interest['time according to UTC time'], rotation = 90)
        ax.set_ylabel('IBI')
        return ax
    