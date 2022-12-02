import wikipediaapi
import os
import re

class Document():
    def __init__(self, page, save_path = './documents'):
        self.page = page
        self.title = page.title
        self.summary = page.summary
        self.sections = page.sections
        self.save_dir_path = os.path.join(save_path, self.title)
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        if not os.path.isdir(self.save_dir_path):
            os.mkdir(self.save_dir_path)
            summary_file = open(os.path.join(self.save_dir_path, self.title), 'w')
            summary_file.write(self.summary)
            summary_file.close()

    def save_document(self, sections, level = 0):
        for section in sections:
            if section.text is not None and section.title is not None:
                section_text = section.text.replace('\n', '')

                title = re.sub('[!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\']', '', section.title)
                save_path = os.path.join(self.save_dir_path, title)
                if len(section_text):
                    section_file = open(save_path, 'w', -1, 'utf-8')
                    section_file.write(section_text)
                    print('save file : ', save_path)
                    section_file.close()
            self.save_document(section.sections, level + 1)

class DocumentSearch():
    def __init__(self):
        self.searching = wikipediaapi.Wikipedia(language='ko')
        self.save_path = './documents'
    def search_keyword(self, keyword):
        page = self.searching.page(keyword)
        document = Document(page)
        return document
