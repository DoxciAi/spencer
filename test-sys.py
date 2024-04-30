import sys
import json

input = json.loads(sys.argv[1])

# messages = []
# for person in input:
#   message = {"message": f"{person['name']} is {person['age']} years old"}
#   messages.append(message)
print("THIS IS FROM PYTHON:")
print(input)
# print(json.dumps(messages))

sys.stdout.flush()