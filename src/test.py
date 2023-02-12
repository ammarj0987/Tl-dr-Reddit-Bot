from main import getResponse

"""
This is a testing file that reads from a text file and summarizes it using either model.
"""

inp = 1
while (inp == 1):
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
    print("1: Try again \n2. Quit")
    inp = int(input())
