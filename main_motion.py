# importing OpenCV 
import cv2
import os
from num_detection import final_num_det

# Capturing video 
video = cv2.VideoCapture('sentry3.mkv') 

fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1440, 810)) 

static_back = None
k=0
m=0
temp_1=0
temp_2=0

# Infinite while loop to treat stack of image as video 
while(video.isOpened()): 

	# Reading frame(image) from video 
	check, frame = video.read() 
	
	# Converting color image to gray_scale image 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

	# Converting gray scale image to GaussianBlur 
	# so that change can be find easily 
	gray = cv2.GaussianBlur(gray, (21, 21), 0) 
	
	# In first iteration we assign the value 
	# of static_back to our first frame 
	if static_back is None: 
		static_back = gray 
		continue

	# Difference between static background 
	# and current frame(which is GaussianBlur) 
	diff_frame = cv2.absdiff(static_back, gray) 
	
	# If change in between static background and 
	# current frame is greater than 30 it will show white color(255) 
	thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 
	
	# Finding contour of moving object 
	_,cnts,_ = cv2.findContours(thresh_frame.copy(), 
					cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
	x=1
	y=1
	i=0
	
	for contour in cnts: 
		if cv2.contourArea(contour) < 3000: 
			continue 
		
		if i==1:
			(x, y, w, h) = cv2.boundingRect(contour)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 3) 
			crop_y = frame[y:y+h, x:x+w]
			cv2.imwrite('test_main.jpg', crop_y)
			num = final_num_det()
			if num != 0:
				cv2.putText(frame,'BOT '+str(num), (x-5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
			else:  
				cv2.putText(frame,'BOT '+str(temp_1), (x-5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
			if num != 0:
				temp_1=num
				print(temp_1)
			path_y = 'y_robot_images'
			#cv2.imwrite(os.path.join(path_y, 'y'+str(k)+'.jpg'), y)
			i=0
			k+=1
			continue
		(x1, y1, w1, h1) = cv2.boundingRect(contour)
		cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 0), 3) 
		crop_x = frame[y1:y1+h1, x1:x1+w1]
		cv2.imwrite('test_main.jpg', crop_x)
		num = final_num_det()
		if num != 0:
			cv2.putText(frame,'BOT '+str(num), (x1-5,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
		else:  
			cv2.putText(frame,'BOT '+str(temp_2), (x1-5,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,cv2.LINE_AA)
		if num != 0:
			temp_2=num
			print(temp_2)
		path_x = 'x_robot_images'
		#cv2.imwrite(os.path.join(path_x,'x'+str(m)+'.jpg'), x)
		m+=1
		i+=1

	# Displaying color frame with contour of motion of object 
	cv2.imshow("frame", frame)
	out.write(frame)

	key = cv2.waitKey(15) 

out.release()
video.release() 

# Destroying all the windows 
cv2.destroyAllWindows() 

