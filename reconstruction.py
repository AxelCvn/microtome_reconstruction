

def organizePredictions(pred_file):
    list_rot = []
    for rotPair in pred_file :
        tmpList = pd.read_csv(rotPair,header=0)
        for index, row in tmpList.iterrows():
            list_rot.append(row.tolist()[0])
    final_rot = [0]
    for i in range(1,len(list_rot)):
        final_rot.append((list_rot[i]-list_rot[i-1])+final_rot[i-1]
    return final_rot

def applyPredRot(directory, final_pred):
    pre, end = os.path.split(directory)
    end = end + '_corrected'
    new_dir = os.path.join(directory,end)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    #For each image of the stack, create a png copy and save it in the new directory
    orderedDir  = sorted(os.listdir(directory))
    for i in range(0,len(orderedDir)-1) :
        imgPath = os.path.join(directory,orderedDir[i])
        imPath = 'corrected_' + orderedDir[i]
        corImgPath = os.path.join(new_dir,imPath)
        if not os.path.isdir(imgPath) and (imgPath.endswith('.png')):
            with Image.open(imgPath) as im:
                angle = final_pred[i]
                correctedIm = im.rotate(angle)
                correctedIm.save(corImgPath)
    return new_dir
