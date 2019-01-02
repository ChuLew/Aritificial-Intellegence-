import inspect
import sys
import numpy as np
'''
Raise a "not defined" exception as a reminder
'''
advanced= False
def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)


'''
Extract 'basic' features, i.e., whether a pixel is background or
forground (part of the digit)
'''
def extract_basic_features(digit_data, width, height):
    features=[]
    # Your code starts here
    for x in range (height):
        data = []
        for y in range (width):
            if digit_data[x][y] == 0:
                data.append(0)
            else:
                data.append(1)
        features.append(data)
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    #_raise_not_defined()
    return features

'''
Extract advanced features that you will come up with
'''
adv_feat = []
final=True
def extract_advanced_features(digit_data, width, height):
    global advanced
    global final
    features=[]
    advanced= True
    features= extract_basic_features(digit_data,width,height)
    final= False
    count = 0
    for i in range (1,height-1):
        for j in range(width-1):
            count = 0
            if features[i-1][j]==1:
                count +=1
            if features[i+1][j]==1:
                count +=1
            if features[i][j+1]==1:
                count+=1
            if features[i][j-1]==1:
                count+=1
            if count >= 3:
                features[i][j]=1


    # Your code starts here
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    return features

'''
Extract the final features that you would like to use
'''
def extract_final_features(digit_data, width, height):
    global final
    features=[]
    # Your code starts here
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    features= extract_advanced_features(digit_data,width,height)
    final=True
    return features

'''
Compute the parameters including the prior and and all the P(x_i|y). Note
that the features to be used must be computed using the passed in method
feature_extractor, which takes in a single digit data along with the width
and height of the image. For example, the method extract_basic_features
defined above is a function than be passed in as a feature_extractor
implementation.

The percentage parameter controls what percentage of the example data
should be used for training.
'''
prior = [None]* 10 # global that holds prior probability
cy = [None] * 10 #global that holds 3d array of conditional probability
edgeCy = [None]*10
def compute_statistics(data, label, width, height, feature_extractor, percentage=100.0):
    global cy
    global prior
    global edgeCy
    global final
    prior = [0.0] * 10 # initialize prior array to 10 0's
    edgeCy = np.zeros((height,width,10))
    #cy = [[[0.0] * height]*width]*10
    cy = np.zeros((height,width,10)) #initialize numpy 3d array of 0's
    num_image = int(len(data) * percentage/100) #take image#*percentage for amount of testing images
    for x in range(num_image):
        prior[label[x]] += 1.0 #increments freqency of each number
        image = data[x] #takes a 2d array and assigns it to image
        features = feature_extractor(image,width,height) #converts image into booleans (1,0)'s
        #print features
        for i in range(height):
            for j in range(width):
                cy[i,j,label[x]] += features[i][j] #for conditional probabiblity increments frequency each pixel is 1 for test_images .
                if advanced:
                    if image[i][j] == 2:
                        edgeCy[i,j,label[x]] += 1


    frequency = prior[:] #will need frequency later for smoothing
    #print frequency
    prior = [x/ len(data) for x in prior]#converts prior array into percentage
    for i in range(10):
        for j in range(height):
            for k in range(width):
                cy[j,k,i] = ((cy[j,k,i]+.000001)/(frequency[i]+.000001)) # increment by k=10 for laplace smoothing
                edgeCy[j,k,i] = ((edgeCy[j,k,i]+.000001)/(frequency[i]+.000001))
                #print cy[j,k,i]

    #print cy
    #_raise_not_defined()

'''
For the given features for a single digit image, compute the class
'''
def compute_class(features):
    predicted = -1
    global cy
    global final
    # Your code starts here
    list = []
    #print final
    for x in range (10):
        count = 0
        for i in range(len(features)):
            for j in range(len(features[0])):
                if final and features[i][j] == 1:
                    count += np.log(cy[i,j,x])
                if advanced:
                    if features[i][j] == 0:
                        count += np.log(1-cy[i,j,x])
                    if features[i][j] == 2:
                        count += np.log(edgeCy[i,j,x])

        list.append(count + np.log(prior[x]))
    predicted = list.index(max(list))
    # You should remove _raise_not_defined() after you complete your 100code
    # Your code ends here
    #print predicted
    return predicted

'''
Compute joint probaility for all the classes and make predictions for a list
of data
'''
def classify(data, width, height, feature_extractor):
    global advanced
    predicted=[]

    # Your code starts here
    for x in range(len(data)):
        image = data[x] #takes a 2d array and assigns it to image
        if advanced:
            features = image
        else:
            features = feature_extractor(image,width,height) #converts image into booleans (1,0)'s
        predicted.append(compute_class(features))
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here


    return predicted
