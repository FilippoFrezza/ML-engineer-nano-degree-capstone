import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def min_amount(df, min_perc=0.8):
    '''
    Functions that returns columns that have more than a given % of missing values
    '''

    return df.count()[df.count() < len(df)*min_perc].index.tolist()

# Calculate the explained variance for the top n principal components
# you may assume you have access to the global var N_COMPONENTS
def explained_variance(s, n_top_components):
    '''Calculates the approx. data variance that n_top_components captures.
       :param s: A dataframe of singular values for top components; 
           the top value is in the last row.
       :param n_top_components: An integer, the number of top components to use.
       :return: The expected data variance covered by the n_top_components.'''
    return np.square(s.sort_values(by=0, ascending=False)[:n_top_components]).sum() / np.square(s).sum()

def create_transformed_df(train_pca, counties_scaled, n_top_components):
    ''' Return a dataframe of data points with component features. 
        The dataframe should be indexed by State-County and contain component values.
        :param train_pca: A list of pca training data, returned by a PCA model.
        :param counties_scaled: A dataframe of normalized, original features.
        :param n_top_components: An integer, the number of top components to use.
        :return: A dataframe, indexed by State-County, with n_top_component values as columns.        
     '''
    # create a dataframe of component features, indexed by State-County
    # create new dataframe to add data to
    counties_transformed=pd.DataFrame()

    # for each of our new, transformed data points
    # append the component values to the dataframe
    for data in train_pca:
        # get component values for each data point
        components=data.label['projection'].float32_tensor.values
        counties_transformed=counties_transformed.append([list(components)])

    # index by county, just like counties_scaled
    counties_transformed.index=counties_scaled.index
    N_COMPONENTS= len(counties_scaled.columns.tolist()) -1
    # keep only the top n components
    start_idx = N_COMPONENTS - n_top_components
    counties_transformed = counties_transformed.iloc[:,start_idx:]
    
    # reverse columns, component order     
    return counties_transformed.iloc[:, ::-1]


def post_pca_train_test_data(complete_df, pca_data):
    '''Gets selected training and test features from given dataframes, and 
       returns tuples for training and test features and their corresponding class labels.
       :param complete_df: A dataframe with all of our processed text data, datatypes, and labels
       :param features_df: A dataframe of all computed, similarity features
       :param selected_features: An array of selected features that correspond to certain columns in `features_df`
       :return: training and test features and labels: (train_x, train_y), (test_x, test_y)'''
    
    temp_df = pd.concat([pca_data, complete_df.iloc[:,-1]], axis=1)   
    
    X_train, X_test, y_train, y_test= train_test_split(
        temp_df.iloc[:,:-1], temp_df.iloc[:,-1:], test_size=0.2,random_state=0)
    
    # get the training features
    train_x = np.array(X_train)
    # And training class labels (0 or 1)
    train_y = np.array(y_train)
    
    # get the test features and labels
    test_x = np.array(X_test)
    test_y = np.array(y_test)
    
    return (train_x, train_y), (test_x, test_y)