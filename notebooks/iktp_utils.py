import numpy as np
import matplotlib.pyplot as plt

def syn_image(x, values, yrange = None, shape = (32,32), value_span = (-1,1)):

    if type(yrange) == type(None):
        yrange = np.linspace(start=value_span[0], stop=value_span[-1],num=shape[0])

    current = np.zeros(shape)
    for ix in range(len(x)):
        yval = values[ix]
        xval = x[ix]
        if yval >= value_span[0] and yval <= value_span[-1]:
            yidx = len(x) -1 - np.searchsorted(yrange, yval, side="left")
            current[yidx,len(x) -1 - ix] = 1

    return current

def polynomials_as_images(size, max_degree, shape = (32,32), value_span = (-1,1), seed = 1, smear_sd = None):

    if seed:
        np.random.seed(seed)

    size = int(size)
    x = np.linspace(start=value_span[0], stop=value_span[-1],num=shape[-1])
    y = np.linspace(start=value_span[0], stop=value_span[-1],num=shape[0])

    data   = np.zeros((size,int(shape[0]),int(shape[1])),
                       dtype=np.uint8)
    labels = np.random.randint(low=1,high=max_degree+1,size=size)

    for i in range(size):
        deg = labels[i]
        c   = np.random.random_sample(deg)
        #print(c)
        #print(x)
        values   = np.polynomial.polynomial.polyval(x,c)
        if smear_sd:
            smear_by = np.random.normal(1.,smear_sd,size=values.size)
            values = values*smear_by
        current = syn_image(x,values,y,shape,value_span)

        data[i,] = current

    return data, labels

def plot_images(data, labels, n_images = 25):
    xticks = np.linspace(start=1, stop=-1,num=3)
    yticks = np.linspace(start=1, stop=-1,num=3)

    plt.figure(figsize=(10,10))
    for i in range(n_images):
        ax = plt.subplot(5,5,i+1)
        plt.grid(True)
        plt.imshow(data[i], cmap=plt.cm.binary)
        ax.set_title("pol({0})".format(labels[i]))

def plot_loss_acc(hist):
    fig = plt.figure(figsize=(15,4));

    ax = fig.add_subplot(121)
    ax.semilogy(hist.epoch,hist.history['loss'],hist.history['val_loss'])
    ax.set_xlabel('epoch')
    ax.set_ylabel('loss')
    ax.legend(['train','val/test'],loc='upper right')
    ax.grid(True)

    ax = fig.add_subplot(122)
    ax.plot(hist.epoch,hist.history['acc'],hist.history['val_acc'])
    ax.set_ylim([0.,1.])
    ax.set_xlabel('epoch')
    ax.set_ylabel('accuracy')
    ax.legend(['train','val/test'],loc='lower right')
    ax.grid(True)
