from sklearn.ensemble import RandomForestClassifier
from PIL import Image
import numpy as np
from skimage import io, color, img_as_ubyte
# from DBConnection import Db
from skimage.feature import greycomatrix, greycoprops
from sklearn.metrics.cluster import entropy


def test_image(image):
    rgbImg = io.imread(image)
    grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

    distances = [1, 2, 3]
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    properties = ['energy', 'homogeneity', 'dissimilarity', 'correlation', 'contrast']

    glcm = greycomatrix(grayImg,
                        distances=distances,
                        angles=angles,
                        symmetric=True,
                        normed=True)

    feats = np.hstack([greycoprops(glcm, 'energy').ravel() for prop in properties])
    feats1 = np.hstack([greycoprops(glcm, 'homogeneity').ravel() for prop in properties])
    feats2 = np.hstack([greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
    feats3 = np.hstack([greycoprops(glcm, 'correlation').ravel() for prop in properties])
    feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel() for prop in properties])
    print(feats)
    k = np.mean(feats)
    l = np.mean(feats1)
    m = np.mean(feats2)
    n = np.mean(feats3)
    o = np.mean(feats4)
    ar = []
    ar.append(k)
    ar.append(l)
    ar.append(m)
    ar.append(n)
    ar.append(o)
    arr = []
    test_val = np.array(ar)
    arr.append(test_val)

    import pandas as pd
    a = pd.read_csv(
        r"C:\Users\hp\Dropbox\PC\Desktop\alzher\static\features.csv")
    attributes = a.values[1:, 0:5]
    labels = a.values[1:, 5]

    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(attributes, labels)
    pred = rf.predict(arr)
    if pred[0] == "MildDemented" or pred[0] == "ModerateDemented" or pred[0] == "VeryMildDemented":
        print("Result : Yes")
        print("Stage: ", pred[0])
        return pred[0]
    elif pred[0] == "NonDemented":
        print("Result : No")
        print("Stage: ", pred[0])
        return pred[0]
    else:
        print("Invalid")
        return "Invalid"
