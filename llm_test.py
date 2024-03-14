import asyncio
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from chat_service_api import Chat

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='',
      api_key_id=''
    )
    return await RobotClient.at_address('', opts)

async def main():
    robot = await connect()
    
    llm = Chat.from_robot(robot, name="llm")
    response = await llm.chat("what are the most popular plants?")
    print(response)
    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
