from PIL import ImageFont, ImageDraw, Image
import os
import os.path
from os import path, sep
from fontTools.ttLib import TTFont
import random
import numpy as np
import cv2 as cv



#Checks .ttf file for given char, if char is not defined in cmap, returns false
def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False



def imageCropp(image, stringOfChar, NameOfImage):

    #Load image and convert it to format for OpenCV
    openCvImage = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    original = openCvImage.copy()

    #Transforming image to gray for easyer cont detection, and ajdsuting treshold
    gray = cv.cvtColor(openCvImage, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    #cont finder, creates a list of all contures it finds
    cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    boxes = []

    #Creating list with coordinate values of box that contains conts
    for c in cnts:
        (x, y, w, h) = cv.boundingRect(c)
        boxes.append([x,y, x+w,y+h])

    #numpy array 
    boxes = np.asarray(boxes)
    left, top = np.min(boxes, axis=0)[:2]
    right, bottom = np.max(boxes, axis=0)[2:]

    #Image cropp
    ROI = original[top:bottom, left:right]
    
    #Save image
    cv.imwrite("../AlpNumLettersEnv/Renders/" + stringOfChar +"/"+'CROPPED__'+NameOfImage, ROI)



def imageRenderFont():

    
    #Checking important dirs, and adding relativ path for directory
    if path.exists("../AlpNumLettersEnv/Fonts")  == False:
        print('There is no "Fonts" directory in AlpNumLettersEnv.\nCreate "Fonts" directory add ".ttf" files and try again.')
        exit()


    directory = '../AlpNumLettersEnv/Fonts/'
    

    if path.exists("../AlpNumLettersEnv/Renders/")  == False:
        os.mkdir("../AlpNumLettersEnv/Renders/")

    #Iterate over files in that directory
    for filename in os.listdir(directory):

        fileNameJoin = os.path.join(directory, filename)


        #Checking if it is a file
        if os.path.isfile(fileNameJoin):
            print(filename)
            
            
            #Adds TTF font file as current font, FONT FILES MUST CORESPOND TO ASCII
            try:

                #Adding diffrent size of the fonts, for diverse sizes
                for fontSizeIterations in range(0,10):

                    randomFontSize = random.randrange(40,60) 
                    
                    font = ImageFont.truetype(fileNameJoin, size=randomFontSize) 
                    checkFont = TTFont(fileNameJoin)
                
                    #Iterates trough ASCII printable chars, and draws a picture for every sign
                    

                    for c in range(33, 127, 1): #range is 33 to 127 for all chars
                        

                        #Char we want to draw on image, 
                        drawnChar = chr(c)
                        #Saving on conversions
                        stringOfChar = str(c)
                        #Char color
                        color = 'black'
                            

                        #Checks for the char in .ttf file, skips iteration if there is no current char. This is used as we can 
                        #create some chars from font files even tho not all of them are defined in .ttf
                        if char_in_font(drawnChar, checkFont) == False:
                            print('There is no char('+drawnChar+') defined in '+fileNameJoin)
                            continue


                        #Usual check if dir exists, if not it creates a dir with ASCII value of rendered charater
                        if path.exists("../AlpNumLettersEnv/Renders/" + stringOfChar) == False:
                            os.mkdir("../AlpNumLettersEnv/Renders/" + stringOfChar)


                        #Make an Image x*x size with transparent background, alpha is 0. Note that changes for alpha here wont affect 
                        #cropped images as they are transformed in imageCropp() function
                        image = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
                        draw = ImageDraw.Draw(image)

                        

                        #Adds the text over image, with indexed font. And saves the image under the name of font + ASCII value of char
                        draw.text((40, 30), drawnChar, font=font, fill=color)
                        
                        NameOfImage = str(str(filename[:-4]) + stringOfChar +'.png') #Needs to have '.png' to work 
                        print(NameOfImage)

                        #str(c) is for the name of the ASCII file where same chars are saved
                        #All of given variables from above have the same name as variables in imageCropp() function
                        imageCropp(image, stringOfChar, NameOfImage)
                
                        #This part of code creates iamges with no background, images are 100*100 and include
                        #Random image positioning and rotation of every image

                        # #Rotation by 10 degrees of every image and then mirroring said image and saving it as difffrent file. Not all chars are simetrical
                        # rotationAngle = 0
                        
                        # for i in range(0,35, 1):

                            
                        #     try:
                        #         #Using image that was drawn before
                        #         imageRotate = image.rotate(rotationAngle)
                        #         imageRotate.save("../AlpNumLettersEnv/Renders/" + stringOfChar +"/"+str(rotationAngle)+'_'+NameOfImage)
                        #         print('Rotate image '+ str(rotationAngle) +'_'+ NameOfImage)
                                
                        #     except:
                        #         print('Rotation error')

                        #     rotationAngle = rotationAngle + 10
                        # #Rotation reset
                        
                        
                        # #Setting diffrent starting coordinates for drawing char using random generator, and then rotating said char
                        # try:

                        #     #More iterations for diverse random positioning
                        #     for randPosIterations in range(0,1,1):
                        #         rotationAngle = 0
                        #         #Images random positioning
                        #         #Taking random starting coordinates

                        #         #If this 2 lines are anabled then the chars can be out of bound of the image border, as only a part of char would be showing
                        #         # randomX = random.randrange(40, 60)
                        #         # randomY = random.randrange(40, 60)

                        #         randomX = 40
                        #         randomY = 30

                        #         imageRanomPosition = Image.new("RGBA", (100, 100), (255, 255, 255, 0))
                        #         drawRandPos = ImageDraw.Draw(imageRanomPosition)

                        #         #Adds the text over image, with indexed font. And saves the image under the name of font + ASCII value of char
                        #         drawRandPos.text((randomX, randomY), drawnChar, font=font, fill=color)
                                
                        #         NameOfImage = str(str(filename[:-4]) + stringOfChar +'.png') 
                        #         print(str(randomX)+'-Y_'+str(randomY)+'_'+NameOfImage)


                        #         imageRanomPosition.save("../AlpNumLettersEnv/Renders/" + stringOfChar +"/"+'X_'+str(randomX)+'-Y_'+str(randomY)+'_'+NameOfImage) 
                        #         print()
                        #         for rotationIterations in range(0,35,1):
                        #             imageRotate = imageRanomPosition.rotate(rotationAngle)
                        #             imageRotate.save("../AlpNumLettersEnv/Renders/" + stringOfChar +"/"+str(rotationAngle)+'_X_'+str(randomX)+'-Y_'+str(randomY)+'_'+NameOfImage)
                        #             rotationAngle = rotationAngle + 10
                        #             print('Rotate image '+ str(rotationAngle)+'_X_'+str(randomX)+'-Y_'+str(randomY) +'_'+ NameOfImage)
                        #             print()
                               
                        # except:
                        #     print('Croping error')

                        #ˇˇˇˇˇˇ#
                        #This Part of Code is creating renders of images with white bacground, the images are not cropped
                        #They are full 100*100 and inluce random positioning and rotation of every image

                        # #RGB with white background, 
                        # #File checking
                        # if path.exists("../AlpNumLettersEnv/Renders/" + stringOfChar + "RGB") == False:
                        #     os.mkdir("../AlpNumLettersEnv/Renders/" + stringOfChar +"RGB")

                        # #Make an Image x*x size and background color,
                        # imageRGB = Image.new("RGB", (100, 100), "White")
                        # drawRGB = ImageDraw.Draw(imageRGB)

                        # #Adds the text over image, with indexed font. And saves the image under the name of font + ASCII value of char
                        # drawRGB.text((40, 30), drawnChar, font=font, fill=color)
                        
                        # NameOfImageRGB = str(str(filename[:-4]) + stringOfChar+ 'RGB' +'.png') 
                        # print(NameOfImageRGB)

                        # imageRGB.save("../AlpNumLettersEnv/Renders/" + stringOfChar +"RGB/"+ NameOfImageRGB) 
                        # print()
                    
                        # #Rotation reset
                        # #Rotatin of RGB image with white background, in 90 turns, because white background also turns around, so PIL sets some areas to black
                        # rotationAngle = 0

                        # for i in range(0,4, 1):
                            
                        #     try:
                        #         #Using RGBA image that was drawn before in RGB
                        #         imageRotateRGB = imageRGB.rotate(rotationAngle)
                        #         imageRotateRGB.save("../AlpNumLettersEnv/Renders/" + stringOfChar +"RGB/"+str(rotationAngle)+'_'+NameOfImageRGB)
                        #         print('Rotate image '+ str(rotationAngle) +'_'+ NameOfImageRGB)
                                
                        #     except:
                        #         print('Rotation error')

                        #     rotationAngle = rotationAngle + 90
                        # rotationAngle = 0
                        
                        # #Setting diffrent starting coordinates for drawing char, and then rotating said char
                        # try:
                        #     #More iterations for diverse random positioning
                        #     for positionIterations in range(0,1,1):

                        #         #Images random positioning
                        #         #Taking random starting coordinates
                        #         #If this 2 lines are anabled then the chars can be out of bound of the image border, as only a part of char would be showing
                        #         # randomX = random.randrange(40, 60)
                        #         # randomY = random.randrange(40, 60)

                        #         randomX = 40
                        #         randomY = 30

                        #         #RGB drawing for random positioning
                        #         imageRanomPositionRGB = Image.new("RGB", (100, 100), "White")
                        #         drawRandPosRGB = ImageDraw.Draw(imageRanomPositionRGB)

                        #         #Adds the text over image, with indexed font. And saves the image under the name of font + ASCII value of char
                        #         drawRandPosRGB.text((randomX, randomY), drawnChar, font=font, fill=color)
                                
                        #         NameOfImageRGB = str(str(filename[:-4]) + stringOfChar +'.png') 
                        #         print(str(randomX)+'-Y_'+str(randomY)+'_'+NameOfImageRGB)


                        #         imageRanomPositionRGB.save("../AlpNumLettersEnv/Renders/" + stringOfChar+ "RGB/" +'X_'+str(randomX)+'-Y_'+str(randomY)+'_'+NameOfImageRGB) 
                        #         print()

                        #         #Rotation of random positioning image with white background
                        #         rotationAngle = 0
                        #         for rotationIterations in range(0,4,1):
                        #             imageRotateRGB = imageRanomPositionRGB.rotate(rotationAngle)
                        #             imageRotateRGB.save("../AlpNumLettersEnv/Renders/" + stringOfChar +"RGB/"+str(rotationAngle)+'_X_'+str(randomX)+'-Y_'+str(randomY)+'_'+NameOfImageRGB)
                        #             rotationAngle = rotationAngle + 90
                        #             print('Rotate image '+ str(rotationAngle)+'_X_'+str(randomX)+'-Y_'+str(randomY) +'_'+ NameOfImageRGB)
                        #             print()
                                
                        # except:
                        #     print('Croping error')

                    
            except:
                print('\nError, cannot load ttf\n')


imageRenderFont()


