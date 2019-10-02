import pandas as pd 

class MotionAnalyzer():
    '''
    This function takes a string which is the location of the motion csv and properly formats it to be read as a dataframe. Motion csv should have 
    Unix time, Date, Time, Motion seconds, NTC temp, Ring state, Motions low, Motions high, Regularity, Average Y, and Average Z as columns. 

    Parameters: String, which is the location of the motion csv 
    Returns: Returns a dataframe with proper format 
    '''
    def motion_dataset_reader(str_dataset):
        return pd.read_csv(str_dataset,sep=';')
        
    '''
    NO METHODS HAVE BEEN CREATED FOR MOTION ANALYTICS. IN THE FUTURE, MOTION CAN BE GRAPHED OUT OR COMPARED TO SLEEP TO HELP MEASURE PATTERNS THAT OCCUR 
    DURING SLEEP 
    '''