import pickle

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials
import time, uuid


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# Replace with valid values
ENDPOINT = ""
training_key = ""
prediction_key = ""
prediction_resource_id = ""

# Create training and prediction clients
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Create a new project
publish_iteration_name = "classifyModel"
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
project_name = uuid.uuid4()
project = trainer.create_project(project_name)

# Add tags to project
normal = trainer.create_tag(project.id, "normal")
defect = trainer.create_tag(project.id, "defect")

# Load fetched data
with open('normal_data_file', 'rb') as fp:
    normal_arr = pickle.load(fp, encoding="utf-8")

with open('defect_data_file', 'rb') as fp:
    defect_arr = pickle.load(fp, encoding="utf-8")

train_list = []

temp = []
for image in normal_arr:
    if bytes.fromhex(image[2]) not in temp:
        temp.append(bytes.fromhex(image[2]))
        train_list.append(
            ImageFileCreateEntry(name="normal" + image[1], contents=(bytes.fromhex(image[2])), tag_ids=[normal.id]))
for image in defect_arr:
    if bytes.fromhex(image[2]) not in temp:
        temp.append(bytes.fromhex(image[2]))
        train_list.append(
            ImageFileCreateEntry(name="defect" + image[1], contents=(bytes.fromhex(image[2])), tag_ids=[defect.id]))

# Upload images to project
batchedImages = chunks(train_list, 64)
for batchOfImages in batchedImages:
    batches = ImageFileCreateBatch(images=batchOfImages)
    upload_result = trainer.create_images_from_files(project.id, batches)

if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print(image)
        print("Image status: ", image.status)

# Train the data
iteration = trainer.train_project(project.id)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    print("Waiting 5 seconds...")
    time.sleep(5)

# Publish the iteration
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print("Done!")

# # Predict the data
# predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
#
# for item in train_list[-10]:
#     results = predictor.classify_image(project.id, publish_iteration_name, bytes.fromhex(item[2]))
#     for prediction in results.predictions:
#         print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))
