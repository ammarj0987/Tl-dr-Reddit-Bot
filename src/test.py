from main import getResponse

print("READING TEXT from text.txt file")
f = open("text.txt", "r")
exampleText = f.read()
print("\nCHOOSE A MODEL:\n1. openAI \n2. huggingface")
model = ""
inp = int(input())
if inp == 1:
    model = "openAI"
if inp == 2:
    model = "huggingface"
print("SUMMARIZING TEXT...")
result = getResponse(exampleText, model)
print(result)