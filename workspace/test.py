import os
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import QuestionAnswering as qa

bot = qa.Chatbot(0)
question_list1 = ['제1조는 무엇인가?', '제2조는 무엇인가?', '제 3조는 무엇인가?', '제 4조는 무엇인가?', '제11조는 무엇인가?', '제34조는 무엇인가?']
question_list2 = ['시험 시간은 언제인가?', '시험 범위는 어디까지인가?', '시험 문제는 몇 문제인가?']
file = '예시_pdf1_대한민국헌법.pdf'
for id, question in enumerate(question_list1):
	print('질문', str(id)+':', question);
	answer = bot.file_mrc(question, file, True)
	print()
#answer = bot.file_mrc(question_list1[1], file, True)

file = '예시_pdf3_중간고사,과제안내.pdf'
for id, question in enumerate(question_list2):
	print('질문', str(id)+':', question);
	answer = bot.file_mrc(question, file, False)
	print()


