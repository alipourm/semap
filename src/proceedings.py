import requests as req
from bs4 import BeautifulSoup
import re
import json
import os
import io


class Proceedings:
    """Abstraction of an ACM DL conference proceedings page"""
    ACM_BASE_URL = 'http://dl.acm.org/'

    def __init__(self, cite_id=None):
        """
        Gets ACM DL cite id and initializes the object.
        :param cite_id:
        :return:
        """
        if cite_id is not None:
            self.url = Proceedings.ACM_BASE_URL + cite_id
            self.main_page = self.get_acm_main_page()
            self.title = self.get_title()
            self.toc = self.get_toc()
            self.papers = self.get_papers()

    def refresh(self):
        self.title = self.get_title()
        self.toc = self.get_toc()
        self.papers = self.get_papers()

    def get_acm_main_page(self):
        response = req.get(self.url)
        content = response.content
        return content

    def get_title(self):
        """ Returns proceeding title """
        soup = BeautifulSoup(self.main_page)
        title_tag = soup.find(lambda tag: tag.has_attr('name') and tag['name'] == 'citation_conference_title')
        print 'title_tag:', title_tag
        return title_tag['content']


    def get_toc(self):
        """
        Get table of contents of the proceedings.
        """
        soup = BeautifulSoup(self.main_page)
        scripts = soup.find_all('script')
        scripts_text = map(lambda s: s.string, scripts)
        toc = filter(lambda s: s is not None and 'Table of Contents' in s, scripts_text)[0]
        link = re.findall(r'tab_about.cfm?.*toc.*ftoken=\d+', toc)[0]
        toc = req.get(Proceedings.ACM_BASE_URL + link).content
        return toc

    def get_prev(self):
        """
        Returns the url of previous proceedings.
        None if there is no.
        """
        soup = BeautifulSoup(self.toc)
        a = soup.find_all(lambda tag: tag.has_attr('title') and 'previous' in tag['title'])
        if len(a) > 0:
            return a[0]['href']
        else:
            return None

    def dump(self, file_name=None):
        if file_name is None:
            curated_name = self.title.replace(os.sep, '').replace(' ', '_')
            file_name = curated_name + '.json'
        data = {'url': self.url,
                'main_page': self.main_page,
                'title': self.title,
                'toc': self.toc,
                'papers': self.papers,
                'dois': self.get_papers_doi()
                }
        json.dump(data, open(file_name, 'w'), indent=2)

    def load(self, file_name):
        """
        loads from a file
        :param file_name:
        :return:
        """
        
        data = json.load(open(file_name))
        self.main_page = data['main_page']
        self.title = data['title']
        self.toc = data['toc']
        self.url = data['url']
        
    def get_papers_doi(self):
        """ Returns the DOI of papers
        :return:
        """
        soup = BeautifulSoup(self.toc)
        papers_tags = soup.find_all(lambda t: t.has_attr('title') and t['title'] == 'DOI')
        paper_url = map(lambda t: t['href'], papers_tags)
        return paper_url

    def get_title_auth(self, l, result=[]):

        if len(l) <= 1:
            return result
        title = l[0].string
        authors = []
        i = 1
        while i < len(l) and 'author' in l[i]['href']:
            authors.append(l[i].string)
            i += 1
        result.append({'authors': authors, 'title': title, 'venue': self.title})
        return self.get_title_auth(l[i:], result)

    def get_papers(self):
        soup = BeautifulSoup(self.toc)
        papers_tables = soup.find('table')
        soup = BeautifulSoup(str(papers_tables))
        a_tags = soup.find_all(lambda t: t.has_attr('href'))
        hrefs = filter(lambda t: 'citation' in t['href'] or 'author' in t['href'], a_tags)
        return self.get_title_auth(hrefs, result=[])

    def get_title_auth_href(self, l, result=[], authors_map = {}):
        if len(l) <= 1:
            return result, authors_map
        title = l[0].string
        authors = []
        i = 1
        while i < len(l) and 'author' in l[i]['href']:
            href = ""
            authors.append(l[i].string)
            i += 1
        result.append({'authors': authors, 'title': title, 'venue': self.title})
        return self.get_title_auth(l[i:], result)
