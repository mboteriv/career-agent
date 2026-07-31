from pprint import pprint

from career_agent.clients.lever_client import LeverClient

client = LeverClient()

payload = client.get_jobs("robinhood")

print(type(payload))
print(len(payload))
print(payload[0].keys())