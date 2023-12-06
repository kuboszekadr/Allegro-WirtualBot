import json

with open('./service/Allegro-WirtualBot-dev/disputes.json', 'r') as f:
    disputes = json.load(f)
disputes = disputes.get('disputes')
return disputes[0].get('id')
