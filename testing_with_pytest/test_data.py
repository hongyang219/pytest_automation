from collections import defaultdict

tasks = ("Task_"+str(i) for i in range(1,4))

def task_ids():
    return ("T"+t[-1] for t in tasks)

test_user_info = {
    "id": '666',
    "name": "user_A",
    "password":"welcome",
    "role": "admin"
}