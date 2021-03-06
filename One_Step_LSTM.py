import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# pip install -U numpy==1.18.5

def create_dataset(dataset, look_back=1):
  dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)


# Add noise to the training set to test the model performance 
 
def add_noise(trainset, max=0.1):
  noise_X = trainset
  noise = np.random.normal(0, max, trainset.shape)
  noise_X = noise_X + noise
  noise_X = noise_X.astype('float32')
  return noise_X
  
# Function used to perform LSTM on dataset and 
# superimpose the prediction on the original dataset to see the goodness of prediction 

def perform_LSTM(feature_name, layer=4):
  dataset = pd.DataFrame(Full[feature_name]).values
  dataset = dataset.astype('float32')
  
  # Normalize the data 
  scaler = MinMaxScaler(feature_range = (0,1))
  dataset = scaler.fit_transform(dataset)
  
  # Split data into training and testing set
  train_size = int(len(dataset) * 0.7)
  test_size = len(dataset) - train_size
  train, test = dataset[0:train_size, :], dataset[train_size:, :]
  
  look_back = 1
  trainX, trainY = create_dataset(train, look_back)
  testX, testY = create_dataset(test, look_back)
  
  # train_noise_X = add_noise(trainX)
  # train_noise_Y = add_noise(trainY)

  trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
  testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
  
  # create and fit the LSTM network
  model = Sequential()
  model.add(LSTM(4, input_shape=(1, look_back)))
  model.add(Dense(1))
  model.compile(loss='mean_squared_error', optimizer='adam')
  model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)

  # make predictions
  trainPredict = model.predict(trainX)
  testPredict = model.predict(testX)

  # invert predictions
  trainPredict = scaler.inverse_transform(trainPredict)
  trainY = scaler.inverse_transform([trainY])
  testPredict = scaler.inverse_transform(testPredict)
  testY = scaler.inverse_transform([testY])
  
  print("Training set RMSE: ", np.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
  print("Testing set RMSE: ", np.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
  
  # shift train predictions for plotting
  trainPredictPlot = np.empty_like(dataset)
  trainPredictPlot[:, :] = np.nan
  trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
  # shift test predictions for plotting
  testPredictPlot = np.empty_like(dataset)
  testPredictPlot[:, :] = np.nan
  testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
  # plot baseline and predictions
  plt.plot(scaler.inverse_transform(dataset))
  plt.plot(trainPredictPlot)
  plt.plot(testPredictPlot)
  plt.show()
  
