import cv2
import os
import enum


def changeState(ch, state):
    if (state == PIC.GREY_NOTFLIPPED and ch == ord('g')) or (state == PIC.COLORED_NOTFLIPPED and ch == ord('g')) \
            or (state == PIC.GREY_FLIPPED and ch == ord('f')):
        return PIC.GREY_NOTFLIPPED

    if (state == PIC.GREY_FLIPPED and ch == ord('g')) or (state == PIC.COLORED_FLIPPED and ch == ord('g')) \
            or (state == PIC.GREY_NOTFLIPPED and ch == ord('f')):
        return PIC.GREY_FLIPPED

    if (state == PIC.COLORED_NOTFLIPPED and ch == ord('f')) or (state == PIC.GREY_FLIPPED and ch == ord('c')) \
            or (state == PIC.COLORED_FLIPPED and ch == ord('c')):
        return PIC.COLORED_FLIPPED

    if (state == PIC.COLORED_FLIPPED and ch == ord('f')) or (state == PIC.GREY_NOTFLIPPED and ch == ord('c')) \
            or (state == PIC.COLORED_NOTFLIPPED and ch == ord('c')):
        return PIC.COLORED_NOTFLIPPED
    return state


# creating enumerations using class
class PIC(enum.Enum):
    COLORED_NOTFLIPPED = 1
    COLORED_FLIPPED = 2
    GREY_NOTFLIPPED = 3
    GREY_FLIPPED = 4


if __name__ == '__main__':

    if not (os.path.isdir('outputImages')):  # if directory with the name 'outputImages' doesn't exist
        os.mkdir('outputImages')  # create directory

    # create a VideoCapture object and pass in the device index (0 or -1 since it's only one camera) or video file name
    cap = cv2.VideoCapture(0)

    i = 0
    picState = PIC.COLORED_NOTFLIPPED
    while cap.isOpened():
        ret, frame = cap.read()  # capture frame by frame, returns true if frame is read correctly

        if not ret:
            break
        else:
            key = cv2.waitKey(1) & 0xFF
            # if key is not equal to default value(255), change key state
            if key != 255:
                picState = changeState(key, picState)
                print(picState)

            # if 'g' was pressed, change color to grey
            if picState == PIC.GREY_NOTFLIPPED:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert colored frame to grayscale

            # if 'g' was pressed followed be 'f', change color to grey then flip
            elif picState == PIC.GREY_FLIPPED:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert colored frame to grayscale
                frame = cv2.flip(frame, 0)

            # if 'f' was pressed, flip frame
            elif picState == PIC.COLORED_FLIPPED:
                frame = cv2.flip(frame, 0)

            # pause the video when p is pressed by waiting indefinitely for o (play or resume) to be pressed
            if key == ord('p'):
                while True:
                    key2 = cv2.waitKey(0) & 0XFF
                    cv2.imshow('frame', frame)

                    if key2 == ord('o'):
                        break

            # save current video frame, then increment i to avoid it from being overridden
            elif key == ord('s'):
                cv2.imwrite('outputImages/img' + str(i) + '.jpg', frame)
                i += 1

            # start recording video
            elif key == ord('m'):
                # define the codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter("Record.avi", fourcc, 20.0, (640, 480))

                # output the video frame
                out.write(frame)

            # stop recording video
            elif key == ord('n'):
                out.release()

            # quit
            elif key == ord('q'):
                break

            cv2.imshow('frame', frame)  # display the resulting frame

    cap.release()  # after breaking out of the loop(pressing 'q'), release the capture
    cv2.destroyAllWindows()  # destroy all windows
