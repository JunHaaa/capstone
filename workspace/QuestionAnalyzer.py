import json
import urllib3
import http


class QuestionAnalyzer():

	def __init__(self, openapi_key = '-'):
		self.openapi_key = openapi_key

	def do_lang (self, openapi_key, text) :
		openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"

		requestJson = {"argument": { "text": text, "analysis_code": "morp" } }

		http = urllib3.PoolManager()
		response = http.request( "POST", openApiURL, headers={"Content-Type": "application/json; charset=UTF-8",  "Authorization": self.openapi_key}, body=json.dumps(requestJson) )

		return response.data.decode()

	def getKeyword(self, question):
		question = question.replace(' ', '_')
		question_lang = self.do_lang(self.openapi_key, question)

		q_json = json.loads(question_lang)['return_object']
		prev_nng = False
		NNG_list = []
		for sentence in q_json['sentence']:
			for morp in sentence['morp']:
				if morp['type'] == 'NNG':
					if prev_nng is True:
						NNG_list[-1] = NNG_list[-1] + morp['lemma']
					else:
						NNG_list.append(morp['lemma'])
						prev_nng = True
				else:
					prev_nng = False
		return NNG_list
