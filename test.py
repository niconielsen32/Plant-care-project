import asyncio
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from chat_service_api import Chat
from speech_service_api import SpeechService
from viam.services.vision import VisionClient

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='',
      api_key_id=''
    )
    return await RobotClient.at_address('', opts)

async def main():
    robot = await connect()
    

    roboflow_plants = VisionClient.from_robot(robot, "plant-model")
    plant = ""

    while True:
        detections = await roboflow_plants.get_detections_from_camera('webcam')
        print(detections)
        if len(detections) > 0:
            print(detections[0].class_name)
            plant = detections[0].class_name


if __name__ == '__main__':
    asyncio.run(main())