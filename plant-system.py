import asyncio
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from chat_service_api import Chat
from speech_service_api import SpeechService
from viam.services.vision import VisionClient
import re
import time

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='',
      api_key_id=''
    )
    return await RobotClient.at_address('', opts)

async def main():
    robot = await connect()
    
    llm = Chat.from_robot(robot, name="llm")
    speech = SpeechService.from_robot(robot, name="speech")
    roboflow_plants = VisionClient.from_robot(robot, "plant-model")
    plant = ""

    while True:
        detections = await roboflow_plants.get_detections_from_camera('webcam')
        if len(detections) > 0:
            print(detections[0].class_name)
            plant = detections[0].class_name

            time.sleep(5)

    
            command = "what family does this plant belong to?"
            if plant != "":
                command = re.sub(r'(this|that|the) plant',  "a " + plant, command)
            print(command)

            response = await llm.chat(command)
            print(response)
            await speech.say(response, True)

            # Don't forget to close the machine when you're done!
            await robot.close()

if __name__ == '__main__':
    asyncio.run(main())