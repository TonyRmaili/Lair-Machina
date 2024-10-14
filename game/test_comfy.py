from comfy_prompt import thread_test_run,async_test_run
import asyncio

description = "An edgy mage with a blue hat"
name = 'Traveler'


asyncio.run(async_test_run(description, name))