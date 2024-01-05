import cv2
import numpy as np
import utils

def detection(image, que, ch, ans):
    widthImage = 800
    heightImage =  1200
    questions = que
    choices = ch
    answer = ans
    image = cv2.imread(image)
    image = cv2.resize(image, (widthImage, heightImage))
    imageContours = image.copy()
    imageBiggestContours = image.copy()
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5),1)
    imgCanny = cv2.Canny(imgBlur,10,50)

    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imageContours, contours, -1, (0, 255, 0),4)
    rectangleContours = utils.rectContour(contours)
    biggestContour = utils.getCornerPoints(rectangleContours[0])
    gradesContour = utils.getCornerPoints(rectangleContours[1])

    if biggestContour.size != 0:
        cv2.drawContours(imageBiggestContours, biggestContour,-1,(0,255,0),30)
        cv2.drawContours(imageBiggestContours, gradesContour,-1,(255,0,0),30)
        biggestContour = utils.reorder(biggestContour)
        gradesContour = utils.reorder(gradesContour)
        point1 = np.float32(biggestContour)
        point2 = np.float32([[0,0],[widthImage,0],[0, heightImage],[widthImage, heightImage]])
        matrix = cv2.getPerspectiveTransform(point1,point2)
        imageWarpColored = cv2.warpPerspective(image, matrix, (widthImage, heightImage))
        
        
        pointG1 = np.float32(gradesContour)
        pointG2 = np.float32([[0,0],[widthImage,0],[0, heightImage],[widthImage, heightImage]])
        matrixG = cv2.getPerspectiveTransform(pointG1,pointG2)
        imageGradeWarpColored = cv2.warpPerspective(image, matrixG, (widthImage, heightImage))
        
        imageWarpGrey = cv2.cvtColor(imageWarpColored,cv2.COLOR_BGR2GRAY)
        imageThreshold = cv2.threshold(imageWarpGrey, 150,255,cv2.THRESH_BINARY_INV)[1]
        
        imageGradeWarpGrey = cv2.cvtColor(imageGradeWarpColored,cv2.COLOR_BGR2GRAY)
        imageGradeThreshold = cv2.threshold(imageGradeWarpGrey, 150,255,cv2.THRESH_BINARY_INV)[1]
        
        boxes = utils.splitBoxes(imageThreshold, questions, choices)
        boxesGrades = utils.splitBoxes(imageGradeThreshold, 5, 5)

        pixelVals = np.zeros((questions,choices))
        
        columnsCount = 0
        rowsCount = 0
        
        for image in boxes:
            totalPx = cv2.countNonZero(image)
            pixelVals[rowsCount][columnsCount] = totalPx
            columnsCount += 1
            if (columnsCount == choices): rowsCount += 1; columnsCount = 0
        
        myIndex = []
        for x in range(0, questions):
            array = pixelVals[x]
            myIndexVal =  np.where(array == np.amax(array))
            myIndex.append(myIndexVal[0][0])
        # print(myIndex)
        grading = []
        for x in range(0, questions):
            if answer[x] == myIndex[x]:
                grading.append(1)
            else:
                grading.append(0)
        # print(grading)
        score = sum(grading)
        
    ###########################################################################
        
        pixelValues = np.zeros((5,5))
        
        columnsGCount = 0
        rowsGCount = 0
        
        for i in boxesGrades:
            totalPixels = cv2.countNonZero(i)
            pixelValues[rowsGCount][columnsGCount] = totalPixels
            columnsGCount += 1
            if (columnsGCount == 5): rowsGCount += 1; columnsGCount = 0
        
        myGIndex = []
        for x in range(0, 5):
            arrayG = pixelValues[x]
            myGIndexVal =  np.where(arrayG == np.amax(arrayG))
            myGIndex.append(myGIndexVal[0][0]+1)
        # print(myGIndex)
        rollNo = ''.join(map(str, myGIndex))
        print("Roll No. ",rollNo," Results: ",score)
        imageArray = ([imageContours,imageBiggestContours, imageThreshold, imageGradeThreshold])
        imageStacked = utils.stackImages(imageArray,0.5)


        cv2.imshow("Stack", imageStacked)
        cv2.waitKey(1)
        return score, rollNo

