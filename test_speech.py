import asyncio
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from chat_service_api import Chat
from speech_service_api import SpeechService


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

    while True:
        commands = await speech.get_commands(1)
        if len(commands) > 0:
            command = commands[0]
            print(command)
            response = await llm.chat(command)
            print(response)
            await speech.say(response, True)

        # Don't forget to close the machine when you're done!
        await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
