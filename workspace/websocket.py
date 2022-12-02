import asyncio;
import QuestionAnswering as qa
import json
import websockets;
import psutil

def scheduling(question_scheduling_list):
    scheduling_list_size = len(question_scheduling_list)
    chatbot_id = 0
    quequed_question_cnt = question_scheduling_list[chatbot_id]
    for i in range(1, scheduling_list_size):
        if quequed_question_cnt > question_scheduling_list[i]:
            chatbot_id = i
            quequed_question_cnt = question_scheduling_list[i]
    question_scheduling_list[chatbot_id] += 1
    return chatbot_id

#model_size = (1024 ** 2) * 711 #MB
#memory = psutil.virtual_memory()

#available = memory.available * 0.15
#model_num = int(available // model_size)
chatbot_num = 5

chatbot_list = [qa.Chatbot(i) for i in range(0, chatbot_num)]
question_scheduling_list = [0] * chatbot_num
print(chatbot_num, 'chatbots activated')

def chat_thread(question_scheduling_list, data, answer_list):
    chatbot_id = scheduling(question_scheduling_list)
    chatbot = chatbot_list[chatbot_id]
    print(data)
    text = json.loads(data)
    question = text['question']
    if text.get('file') is not None:
        file_name = text['file']
        print("receive : " + question)
        print("file_name : " + file_name)
        answer = chatbot.file_mrc(question, file_name, answer_list, True)
    else:
        answer = chatbot.wiki_mrc(question, answer_list)
    question_scheduling_list[chatbot_id] -= 1


async def accept(websocket, path):
    loop = asyncio.get_running_loop()
    while True:
        data = await websocket.recv();
        answer_list = []
        answer = await loop.run_in_executor(None, chat_thread, question_scheduling_list, data, answer_list)
        await websocket.send(answer_list[0]);
        answer_list.clear()

start_server = websockets.serve(accept, "localhost", 9997);
asyncio.get_event_loop().run_until_complete(start_server);
asyncio.get_event_loop().run_forever();
