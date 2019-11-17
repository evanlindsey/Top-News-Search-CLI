import json
import os
import urllib.request


class News:
    '''News class
    Provides access to News API via REST calls.
    '''

    news_url = 'http://newsapi.org/v2/'
    api_key = os.environ['API_KEY']
    sources_ep = 'sources'
    headlines_ep = 'top-headlines'
    api_param = 'apiKey'
    sources_param = 'sources'
    term_param = 'q'
    page_param = 'pageSize'

    @classmethod
    def request_json(cls, url, key):
        '''Request JSON from the given URL with a formatted query string.

        Args:
            url: Target URL with formatted query string.
            key: Key for the target value within the returned JSON object.

        Returns:
            string: The return value. Value from the returned JSON object based on the given key.
        '''
        req = urllib.request.urlopen(url)
        data = req.read()
        obj = json.loads(data.decode('utf-8'))
        return obj[key]

    @classmethod
    def get_sources(cls):
        '''Request all available sources from News API.

        Returns:
            dictionary: The return value. Keys are names of sources. Values are IDs of sources.
        '''
        url = f'{cls.news_url}{cls.sources_ep}?{cls.api_param}={cls.api_key}'
        sources = cls.request_json(url, 'sources')
        return dict(enumerate(sources))

    @classmethod
    def search_term(cls, term, sources):
        '''Search the given news sources for articles containing the given term.

        Args:
            term: Target term to search for within articles.
            sources: Comma separated list of news source IDs.

        Returns:
            dictionary: The return value. Keys are titles of articles. Values are objects containing contents of articles.
        '''
        if sources != '':
            sources = ','.join([x for x in sources])
            sources = f'{cls.sources_param}={sources}&'
        url = f'{cls.news_url}{cls.headlines_ep}?{sources}{cls.term_param}={term}&{cls.page_param}=100&{cls.api_param}={cls.api_key}'
        articles = cls.request_json(url, 'articles')
        return dict(enumerate(articles))
