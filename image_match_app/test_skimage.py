import skimage
import skimage.io
import skimage.color
import skimage.transform
import matplotlib.pyplot as plt

def inspect(img_path):
    image = skimage.io.imread(img_path)
    fig = plt.figure(figsize=(1, 4))

    def mark(title):
        plt.axis('off')
        plt.title(title)

    plt.subplot(141)
    plt.imshow(image)
    mark('origin')

    lab = skimage.color.rgb2lab(image)
    # lab = skimage.color.rgb2xyz(image)
    # lab = image

    plt.subplot(142)
    plt.imshow(lab[:,:,0], cmap=plt.cm.gray)
    mark('L')

    plt.subplot(143)
    plt.imshow(lab[:,:,1], cmap=plt.cm.gray)
    mark('a')

    plt.subplot(144)
    plt.imshow(lab[:,:,2], cmap=plt.cm.gray)
    mark('b')
    
    plt.show()

imgPath = '/home/ray/dimage/final-project/imagematch/CBIRdataset/images/%d.jpg'

for i in xrange(121, 125):
    inspect(imgPath % i)



