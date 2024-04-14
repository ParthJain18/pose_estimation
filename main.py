import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def predict_cricket_shot(image_path):

	with open('body_language.pkl', 'rb') as f:
		model = pickle.load(f)

	with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

		frame = cv2.imread(image_path)

		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image.flags.writeable = False

		# Make Detections
		results = holistic.process(image)

		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
								  mp_drawing.DrawingSpec(
									  color=(245, 117, 66), thickness=2, circle_radius=4),
								  mp_drawing.DrawingSpec(
									  color=(245, 66, 230), thickness=2, circle_radius=2)
								  )
		try:
			# Extract Pose landmarks
			pose = results.pose_landmarks.landmark
			pose_row = list(np.array(
				[[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())

			# Concate rows
			row = pose_row
			X = pd.DataFrame([row])
			body_language_class = model.predict(X)[0]
			body_language_prob = model.predict_proba(X)[0]
			print(body_language_class, body_language_prob)

			# Grab ear coords
			coords = tuple(np.multiply(
				np.array(
					(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x,
					 results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y)), [640, 480]).astype(int))

			cv2.rectangle(image,
						  (coords[0], coords[1]+5),
						  (coords[0]+len(body_language_class)
						   * 20, coords[1]-30),
						  (245, 117, 16), -1)
			cv2.putText(image, body_language_class, coords,
						cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

			# Get status box
			cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

			# Display Class
			cv2.putText(image, 'CLASS', (95, 12),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.putText(image, body_language_class.split(' ')[
						0], (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

			# Display Probability
			cv2.putText(image, 'PROB', (15, 12),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2)), (
				10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		except:
			pass

		cv2.imshow("Cricket Shot detected", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		return image


if __name__ == "__main__":
	predict_cricket_shot('sample1.jpg')
