import numpy as np
from sklearn.manifold import TSNE
from skimage.transform import resize
from PIL import Image
from matplotlib import pyplot as plt


def gray_to_color(img):
    if len(img.shape) == 2:
        img = np.dstack((img, img, img))
    return img


def min_resize(img, size):
    """
    Resize an image so that it is size along the minimum spatial dimension.
    """
    print("we are here!!")
    print(img.shape)
    w, h = map(float, img.shape[:2])
    if min([w, h]) != size:
        if w <= h:
            img = resize(img, (int(round((h/w)*size)), int(size)))
        else:
            img = resize(img, (int(size), int(round((w/h)*size))))
    return img


def image_scatter(features, images, img_res, res=4000, cval=1.):
    """
    Embeds images via tsne into a scatter plot.
    Parameters
    ---------
    features: numpy array
        Features to visualize
    images: list or numpy array
        Corresponding images to features. Expects float images from (0,1).
    img_res: float or int
        Resolution to embed images at
    res: float or int
        Size of embedding image in pixels
    cval: float or numpy array
        Background color value
    Returns
    ------
    canvas: numpy array
        Image of visualization
    """
    features = np.copy(features).astype('float64')
    images = [gray_to_color(image) for image in images]
    print("problem is here")
    dummy = [image.shape for image in images]
    print(dummy)
	
	
	
    #images = [min_resize(image, img_res) for image in images]
    max_width = max([image.shape[0] for image in images])
    max_height = max([image.shape[1] for image in images])
    
    print('Beginning T-SNE')
    model = TSNE(n_components=2, random_state=0)
    #f2d = bh_sne(features)
    f2d = model.fit_transform(features)
    print('Finished T-SNE')
    
    xx = f2d[:, 0]
    yy = f2d[:, 1]
    x_min, x_max = xx.min(), xx.max()
    y_min, y_max = yy.min(), yy.max()
    # Fix the ratios
    sx = (x_max-x_min)
    sy = (y_max-y_min)
    if sx > sy:
        res_x = sx/float(sy)*res
        res_y = res
    else:
        res_x = res
        res_y = sy/float(sx)*res

    canvas = np.ones((res_x+max_width, res_y+max_height, 3))*cval
    x_coords = np.linspace(x_min, x_max, res_x)
    y_coords = np.linspace(y_min, y_max, res_y)
    for x, y, image in zip(xx, yy, images):
        w, h = image.shape[:2]
        x_idx = np.argmin((x - x_coords)**2)
        y_idx = np.argmin((y - y_coords)**2)
        canvas[x_idx:x_idx+w, y_idx:y_idx+h] = image
    return canvas


# Main Code

image1 = Image.open('D:/stephen-krewson/Documents/illustra-ligner/extracted-images/1779_Page_05_ex_0.jpg')
image1 = np.array(image1)
print(image1.shape[1])
# image1data = np.asarray(image1array).astype('float64')
# image1data = image1data.reshape((image1data.shape[0], -1))
image2 = Image.open('D:/stephen-krewson/Documents/illustra-ligner/extracted-images/1779_Page_05_ex_0.jpg')
image2 = np.array(image2)
print(image2.shape[:2])
# image2array = np.array(image2)
# image2data = np.asarray(image2array).astype('float64')
# image2data = image2data.reshape((image2data.shape[0], -1))
imagesall = np.hstack([image1,image2])


# In[41]:

data1=np.load('D:/stephen-krewson/Documents/illustra-ligner/extracted-sims/1779_Page_05_ex_0.jpg.npy')
data2=np.load('D:/stephen-krewson/Documents/illustra-ligner/extracted-sims/1779_Page_05_ex_0.jpg.npy')
dataall = np.array([])
dataall = np.vstack(data1)
dataall= np.vstack(data2)

print("blarg")
print(data1.shape)
print(data1)
print(dataall.shape)
print(dataall)


# In[42]:

canvas=image_scatter(dataall, imagesall, img_res=500, res=4000, cval=1.)


# In[ ]:

plt.imshow(canvas, interpolation='nearest')
plt.show()