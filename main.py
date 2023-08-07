import cv2
# Start of execution program
#get image
img = cv2.imread('input.jpg', cv2.IMREAD_COLOR)
# cv2.imshow('img', img)
# *******************************************************
# Make image greyscale
grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# cv2.imshow('greyscale', grey)
# *******************************************************
# Binarise greyscale pixels
(_, thresh) = cv2.threshold(grey, 230, 255, 1)
# cv2.imshow('thresholded', thresh)
# *******************************************************
#Get shape contours
(contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# *******************************************************
for contour in contours:
    if cv2.contourArea(contour) > 130:
        x, y, w, h = cv2.boundingRect(contour)
        perimeter = cv2.arcLength(contour, True)
        e = 0.009 * perimeter
        approxContour = cv2.approxPolyDP(contour, epsilon= e, closed= True)
        cv2.drawContours(grey, [contour], contourIdx= -1, color=(255, 255, 255), thickness=9)
        newImage = grey[y:y+h, x:x+w]

        (newContour, newHierarchy) = cv2.findContours(newImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(newContour) > 7:
            cv2.putText(img, "Face", (x+15, y+15), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,0,255), thickness=1)




            (_, thresh) = cv2.threshold(newImage, 230, 255, 1)
            (innerContours,innerHierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            yCoordinate = []
            for inContour in innerContours:
                perimeter1 = cv2.arcLength(inContour, True)
                e1 = 0.009 * perimeter1
                approxContour = cv2.approxPolyDP(inContour, epsilon= e1, closed= True)
                _,y1, _, _ = cv2.boundingRect(inContour)
                yCoordinate.append(y1)
            yCoordinate.sort(reverse=False)
            for inContour in innerContours:
                # recognized on name internal parts of the face
                x2, y2, w2, h2 = cv2.boundingRect(inContour)
                shapeName =""
                for yIndex in range(len(yCoordinate)):
                    if y2 == yCoordinate[yIndex] or y2 == yCoordinate[yIndex+1]:
                        shapeName = "Eye"
                        break
                    elif y2 == yCoordinate[yIndex+2]:
                        shapeName = "Nose"
                        break
                    else:
                        shapeName = "Mouth"
                        break
                cv2.putText(img, shapeName, (x2+x, y2+y), fontFace= cv2.FONT_HERSHEY_PLAIN, fontScale= 1, color= (0, 0, 255), thickness= 1)
        else:
            # ****************************************************
            # recognized on shape name
            shapeName=""
            if len(approxContour) == 2:
                shapeName= 'Line'
            elif len(approxContour) == 3:
                shapeName= 'Triangle'
            elif len(approxContour) == 4:
                shapeName= 'Rectangle'
            elif 5 <= len(approxContour) <= 10:

                shapeName= 'Curve'
            else:
                shapeName= 'Circle'
            cv2.putText(img, shapeName, (x+15,y+35), fontFace= cv2.FONT_HERSHEY_PLAIN, fontScale= 1, color= (0, 0, 255), thickness= 1)

cv2.imshow('name image', img)
cv2.waitKey()