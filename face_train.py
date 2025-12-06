import cv2
import face_recognition
import os
import pickle

dataset_path = "dataset"
encodings_file = "encodings.pickle"

known_encodings = []
known_names = []
for person_name in os.listdir(dataset_path):

	person_folder = os.path.join(dataset_path,person_name)
	
	if not os.path.isdir(person_folder):
		continue
		
	print(f"[INFO] Processing {person_name}...")
	
	for image_name in os.listdir(person_folder):
		image_path = os.path.join(person_folder, image_name)
		
		image = cv2.imread(image_path)
		rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		
		boxes = face_recognition.face_locations(rgb,model="hog") #hog can be replaced with cnn
		
		encodings = face_recognition.face_encodings(rgb, boxes)
		
		for encoding in encodings:
			known_encodings.append(encoding)
			known_names.append(person_name)
	
	
print("[INFO] Saving encodings...")
data = {"encodings": known_encodings, "names": known_names}

with open(encodings_file, "wb") as f:
    pickle.dump(data, f)
    
#add function to limit entry of one face one time only 

print("[INFO] Training completed! Encodings saved to", encodings_file)
