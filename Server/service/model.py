import base64
import os

from AIModel.Open_Close_Eye_Model import detect


def decode_and_process_pictures(username, pictures_base64):
    # create a directory with pictures
    user_directory = f'./user_data/{username}'
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    for idx, picture_base64 in enumerate(pictures_base64):
        try:
            # Decode the Base64-encoded picture
            picture_binary = base64.b64decode(picture_base64)

            # Define the file path
            file_path = os.path.join(user_directory, f'picture_{idx + 1}.jpg')

            # Save the picture to the file
            with open(file_path, 'wb') as file:
                file.write(picture_binary)
        except Exception as e:
            print(f"Error decoding or saving picture: {e}")
    # send the path to pictures to model for analyze
    return detect(user_directory)
