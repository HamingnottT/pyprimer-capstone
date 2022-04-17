import os

# for quickly pushing to github

print("\n ~ A quicker way to update github from bash terminal ~\n")

print("Please enter the comment below and this program will handle the rest:")
comment = input("git commit -m ")

os.system("cd ..")
# os.system("dir")
os.system(f"git add . && git commit -m {comment} && git push && git pull")