import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(data, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    and backward propagation for the gradients for all parameters.
    """
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs + Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    z1 = np.matmul(data, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.matmul(a1, W2) + b2
    a2 = softmax(z2)

    cost = -np.sum(labels * np.log(a2))

    grad_z2 = a2 - labels
    grad_a1 = np.matmul(grad_z2, np.transpose(W2))
    grad_z1 = grad_a1 * sigmoid_grad(a1)
    #grad_x = np.matmul(grad_z1, np.transpose(W1))

    grad_w1 = np.matmul(np.transpose(data), grad_z1)
    grad_b1 = np.sum(grad_z1, axis=0)

    grad_w2 = np.matmul(np.transpose(a1), grad_z2)
    grad_b2 = np.sum(grad_z2, axis=0)

    grad = np.concatenate((grad_w1.flatten(), grad_b1.flatten(),
                           grad_w2.flatten(), grad_b2.flatten()))

    return cost, grad

def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i,random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params: forward_backward_prop(data, labels, params,
        dimensions), params)

def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    raise NotImplementedError
    ### END YOUR CODE

if __name__ == "__main__":
    sanity_check()
    #your_sanity_checks()
