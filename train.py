import os
import csv
listOfFolders = os.listdir(r'C:\Users\hp\Dropbox\PC\Desktop\alzher\static\Dataset\\')
static_path=r"C:\Users\hp\Dropbox\PC\Desktop\alzher\static\\"
properties = ['energy', 'homogeneity', 'dissimilarity', 'correlation', 'contrast']
header_list=properties
header_list.append("label")
file=open(static_path+"features.csv", "w", newline="")
with file:
    writer=csv.writer(file)
    writer.writerow(header_list)

for foldername in listOfFolders:
    for filename in os.listdir(static_path+'Dataset\\'+foldername):
        import numpy as np
        from skimage import io, color, img_as_ubyte
        from skimage.feature import greycomatrix, greycoprops
        rgbImg = io.imread(static_path+'Dataset\\'+foldername+ "\\" + filename)
        grayImg = img_as_ubyte(color.rgb2gray(rgbImg))
        distances = [1, 2, 3]
        angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
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
        aa=[]
        k = np.mean(feats)
        l = np.mean(feats1)
        m = np.mean(feats2)
        n = np.mean(feats3)
        o = np.mean(feats4)
        aa.append(k)
        aa.append(l)
        aa.append(m)
        aa.append(n)
        aa.append(o)
        aa.append(foldername)
        file = open(static_path + "features.csv", "a", newline="")       #open csv file in append mode
        with file:
            writer = csv.writer(file)
            writer.writerow(aa)
print("Training Completed")
