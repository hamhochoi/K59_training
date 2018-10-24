# import Api

# thing_global_id = 'cb2c8df3-74ff-4095-97a6-488fd418e5cd/binary_sensor.motion_detection'
# item_global_id = 'cb2c8df3-74ff-4095-97a6-488fd418e5cd/binary_sensor.motion_detection/binary_sensor.motion_detection'
# platform_id = 'cb2c8df3-74ff-4095-97a6-488fd418e5cd'
# print(Api.api_get_thing_state_by_id(thing_global_id))
# print(Api.api_get_things_state())
# print(Api.api_get_item_state_by_id(thing_global_id, item_global_id))
# print(Api.api_get_things_state_in_platform(platform_id))
# print(Api.api_get_thing_info_in_platform(platform_id))
# print(Api.api_get_things_info())



# import paho.mqtt.client as mqtt
# import json
# broker_address = "iot.eclipse.org"
# clientMQTT = mqtt.Client("test")  # create new instance
# clientMQTT.connect(broker_address)  # connect to broker
# global_id = 'f2b99574-8585-4cac-935f-d53ada871086/binary_sensor.motion_detection'
# message = {
#     'caller': 'collector',
#     'thing_global_id': global_id
# }
#
# clientMQTT.publish('dbwriter/request/api_get_thing_by_global_id', json.dumps(message))
# clientMQTT.publish('dbwriter/request/api_get_thing_by_global_id', json.dumps(message))
# clientMQTT.publish('dbwriter/request/api_get_thing_by_global_id', json.dumps(message))


import tensorflow as tf
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

n_features = 2

X, Y = make_classification(n_samples=140, n_features=n_features, n_informative=1, 
                           n_redundant=0, n_clusters_per_class=1)
Y = np.array([Y, -(Y-1)]).T  # The model currently needs one column for each class
X, X_test, Y, Y_test = train_test_split(X, Y)


index0 = []
index1 = []

for i in range(len(Y)):
	if (Y[i][0] == 0):
		index0.append(i)
	else:
		index1.append(i)


X0 = X[index0]
X1 = X[index1]
Y0 = Y[index0]
Y1 = Y[index1]

X0 = np.asarray(X0)
X1 = np.asarray(X1)
Y0 = np.asarray(Y0)
Y1 = np.asarray(Y1)

print ("X0: ", X0)
print ("X1: ", X1)
print ("Y0: ", Y0)
print ("Y1: ", Y1)

X = np.concatenate((X0, X1), axis=0)
Y = np.concatenate((Y0, Y1), axis=0)

print ("X: ", X)
print ("Y: ", Y)

learning_rate = 0.001
training_epochs = 50
batch_size = 1
display_step = 1


# Network Parameters
n_hidden_1 = 10 # 1st layer number of features
n_hidden_2 = 10 # 2nd layer number of features
n_input = n_features # Number of feature
n_classes = 2 # Number of classes to predict


# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])

# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()


with tf.Session() as sess:
    sess.run(init)
    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(len(X)/batch_size)
        X_batches = np.array_split(X, total_batch)
        Y_batches = np.array_split(Y, total_batch)
        # Loop over all batches
        for i in range(total_batch):
            batch_x, batch_y = X_batches[i], Y_batches[i]
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                          y: batch_y})
            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))


        # print (sess.run(weights['h1']))




    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({x: X_test, y: Y_test}))
    global result 
    result = tf.argmax(pred, 1).eval({x: X_test, y: Y_test})