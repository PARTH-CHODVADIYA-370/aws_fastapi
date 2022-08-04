import base64
import json
import uuid
import requests

# async def Image_Converter(Hax_Value):
#     random_name = str(uuid.uuid4())
#     decodeit = open(f"Server/static/{random_name}.jpg", 'wb')
#     decodeit.write(base64.b64decode(Hax_Value))
#     decodeit.close()
#     img_path = "http://localhost:8000/images?id=Server%2Fstatic%2F" + \
#         str(random_name)+".jpg"
#     return img_path

import requests
async def Image_Converter(hax_value):
    url="https://evenmore.co.in/API/image"
    correct_payload = {"base64Image": hax_value, "imageName":str(uuid.uuid4()) }
    json_object = json.dumps(correct_payload, indent = 4) 
    data = requests.post(url, data=json_object,headers={'Content-Type':'application/json'})
    try:
        if "null" in data:
           return ""
        data=data.text
        data_list=data.split('":"')
        return data_list[-1][:len(data_list[-1])-2]
    except:
        return ""


