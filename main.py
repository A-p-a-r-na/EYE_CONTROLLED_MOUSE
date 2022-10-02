import cv2
import mediapipe as mp
import pyautogui  #to move the cursor

cam = cv2.VideoCapture(0)  # to capture video and 0 is for only 1 device camera which is the pc itself.
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h =pyautogui.size() #to get the size of the wholw screen
while True:  # while loop is used cuz video is actually continously running frame so we have to capture all the frame.
    _, frame = cam.read()  # call camera and read whatever is coming from the camera.
    frame = cv2.flip(frame, 1)  #flipping the image vertically to get the reflection of landmark on one eye to another eye so that we can move our cursor
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # detecting face in another colour.ie bgr to rgb
    output = face_mesh.process(rgb_frame)  # output after proessing the rgb frame.
    landmark_points = output.multi_face_landmarks  # these are the points on the face.
    frame_h, frame_w, _ = frame.shape  #to find the height and width of the frame
    if landmark_points:
        landmarks = landmark_points[0].landmark  # 0 means only one face that means me itself
        for id, landmark in enumerate(landmarks[474:478]):  # enumerate will give two things.They are id and landmark for all the landmark inside the landmarks, get the x and y coordinate. not all landmarks are needed so we only select 474 to 478
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))  # drawing circle around face radius of circle is 3. the rgb colour is (0, green=255,0)
            if id == 1:  #since we have 4 landmark on eye we select only one that is why id==1
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)  #In that case we will make the movement of cursor
        left = [landmarks[145], landmarks[159]]  #now we need to perform the doubleclick using cursor
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if(left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)
    cv2.imshow('Eye Controlled Mouse', frame)  # imshow means image show used to show some image.
    cv2.waitKey(1)  # wait for a key ,here it is 1--> which show the window unitl the key 1 is pressed.
