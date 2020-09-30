import cv2
import os
import enum


# creating enumerations using class
class PIC(enum.Enum):
    COLORED_NOTFLIPPED = 1
    COLORED_FLIPPED = 2
    GREY_NOTFLIPPED = 3
    GREY_FLIPPED = 4


picState = PIC.COLORED_NOTFLIPPED

if not (os.path.isdir('outputImages')):  # if directory with the name 'outputImages' doesn't exist
    os.mkdir('outputImages')  # create directory

# create a VideoCapture object and pass in the device index (0 or -1 since it's only one camera) or video file name
cap = cv2.VideoCapture(0)

# define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # output video
prevkeypressed = '0'
i = 0
mylist = []
while cap.isOpened():
    ret, frame = cap.read()  # capture frame by frame, returns true if frame is read correctly

    if not ret:
        break
    else:
        key = cv2.waitKey(1) & 0xFF
        if prevkeypressed == 'g':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        elif prevkeypressed == 'g' and isflipped == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.flip(frame, 0)

        elif prevkeypressed == 'f':
            frame = cv2.flip(frame, 0)

        elif prevkeypressed == 'f' and isgray == 1:
            frame = cv2.flip(frame, 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if key == ord('g'):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert colored frame to grayscale
            picState = PIC.GREY_NOTFLIPPED

        elif key == ord('f'):
            frame = cv2.flip(frame, 0)
            prevkeypressed = 'f'
            isflipped = 1
            mylist.append(prevkeypressed)
            print(prevkeypressed)

        elif key == ord('p'):
            while True:
                key2 = cv2.waitKey(0) & 0XFF
                cv2.imshow('frame', frame)

                if key2 == ord('o'):
                    break

        elif key == ord('s'):
            cv2.imwrite('outputImages/img' + str(i) + '.jpg', frame)
            i += 1

        elif key == ord('c'):
            prevkeypressed = 'c'
            isgray = 0
            mylist.append(prevkeypressed)
            print(prevkeypressed)

        elif key == ord('m'):
            # define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter("Record.avi", fourcc, 20.0, (640, 480))
            # output the video frame
            out.write(frame)

        elif key == ord('n'):
            out.release()

        elif key == ord('q'):
            break

        print(mylist)
        cv2.imshow('frame', frame)  # display the resulting (grayscale) frame

cap.release()  # after breaking out of the loop(pressing 'q'), release the capture
cv2.destroyAllWindows()  # destroy all windows
