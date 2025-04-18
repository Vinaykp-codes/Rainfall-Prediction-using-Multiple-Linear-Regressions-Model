import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from django.conf import settings

# read the cleaned data
data = pd.read_csv(settings.DATASET_URL)
# the features or the 'x' values of the data
# these columns are used to train the model
# the last column, i.e, precipitation column
# will serve as the label
X = data.drop(['PrecipitationSumInches'], axis=1)

# the output or the label.
Y = data['PrecipitationSumInches']
# reshaping it into a 2-D vector
Y = Y.values.reshape(-1, 1)

# consider a random day in the dataset
# we shall ann a graph and observe this
# day
day_index = 798
days = [i for i in range(Y.size)]

# initialize a linear regression classifier
clf = LinearRegression()
# train the classifier with our
# input data.
clf.fit(X, Y)

# ann a graph of the precipitation levels
# versus the total number of days.
# one day, which is in red, is
# tracked here. It has a precipitation
# of approx. 2 inches.

print("the precipitation trend graph: ")
plt.scatter(days, Y, color='g')
plt.scatter(days[day_index], Y[day_index], color='r')
plt.title("Precipitation level")
plt.xlabel("Days")
plt.ylabel("Precipitation in inches")


def do_prediction(temp_high, temp_avg, temp_low, dew_point_high, dew_point_avg, dew_point_low,
                  humidity_high, humidity_avg, humidity_low, sea_level_pressure_avg_inches,
                  visibility_high, visibility_avg, visibility_low, wind_high, wind_avg, wind_gust,
                  ):
    # give a sample input to test our model
    # this is a 2-D vector that contains values
    # for each column in the dataset.
    # inp = np.array([[74], [60], [45], [67], [49], [43], [33], [45],
    #                 [57], [29.68], [10], [7], [2], [0], [20], [4], [31]])
    print('Starting .....')
    inp = np.array([
        [temp_high], [temp_avg], [temp_low], [dew_point_high], [dew_point_avg], [dew_point_low],
        [humidity_high], [humidity_avg], [humidity_low], [sea_level_pressure_avg_inches], [visibility_high],
        [visibility_avg], [visibility_low],
        [wind_high], [wind_avg], [wind_gust]
    ])

    inp = inp.reshape(1, -1)

    # print the output.
    print('***************************************************************')
    print('The precipitation in inches for the input is:', clf.predict(inp))
    return clf.predict(inp)


def mae_mse_r2_score():
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression

    data = pd.read_csv(settings.DATASET_URL)
    print(data)
    x = data.drop(columns=['PrecipitationSumInches'])
    y = data['PrecipitationSumInches']

    sc = StandardScaler()
    x_std = sc.fit_transform(x)
    x_std = pd.DataFrame(x_std, columns=x.columns)
    x_train, x_test, y_train, y_test = train_test_split(x_std, y, test_size=0.2, random_state=42)

    reg_model = LinearRegression()
    reg_model.fit(x_train, y_train)
    y_predicted = reg_model.predict(x_test)

    mae = str(mean_absolute_error(y_test, y_predicted)*100)
    mse = str(mean_squared_error(y_test, y_predicted)*100)
    r2_score_ = str(r2_score(y_test, y_predicted)*100)

    print('Mean absolute error = ', mae)
    print('Mean squared error = ', mse)
    print('R2 score = ', r2_score_)

    return [mae, mse, r2_score_]


