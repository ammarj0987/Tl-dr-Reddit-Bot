from main import getResponse

print("READING TEXT from text.txt file")
f = open("text.txt", "r")
text = f.read()
print("\nCHOOSE A MODEL:\n1. openAI \n2. huggingface")
model = ""
if int(input()) == 1:
    model = "openAI"
elif int(input()) == 2:
    model = "huggingface"
print("SUMMARIZING TEXT...")
result = getResponse(text, model)
print(result)