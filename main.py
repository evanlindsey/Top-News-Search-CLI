import getpass
import pickle

from db import DB
from menu import Menu
from news import News


class Main(Menu):
    '''Main class
    Provides the user interaction layer.
    Inherits from Menu class.
    '''

    user_id = -1
    source_ids = ''

    def main_menu(self):
        '''Display the main menu.'''
        if self.user_id != -1:
            options = '[1] News sources\n'\
                      '[2] Search articles\n'\
                      '[3] View saved articles\n'\
                      '[4] Logout\n'\
                      '[0] Quit\n'
        else:
            options = '[1] News sources\n'\
                      '[2] Search articles\n'\
                      '[3] Login\n'\
                      '[0] Quit\n'
        return self.create_menu('MENU', options)

    def sources_menu(self):
        '''Display the sources menu.'''
        sources = News.get_sources()
        print(f'{str(len(sources))} sources available!')
        action = None
        while action != 0:
            options = '[1] View sources\n'\
                      '[2] Choose sources\n'\
                      '[0] Go back\n'
            action = self.create_menu('SOURCES', options)
            if action == 1:
                [print(f"[{str(i + 1)}] {source['name']}")
                 for i, source in sources.items()]
                selection = 'All' if self.source_ids == '' else [
                    sources[i]['name'] for i in sources if sources[i]['id'] in self.source_ids]
                print(
                    f'\n{self.Fore.YELLOW}{self.Style.BRIGHT}Current sources: {selection}{self.Style.RESET_ALL}')
            elif action == 2:
                new_ids = ''
                while new_ids == '':
                    new_ids = self.yellow_input(
                        'Enter comma separated list of source #s (or `All`)')
                    print(self.Style.RESET_ALL)
                if new_ids.lower() == 'all':
                    self.source_ids = ''
                    self.success('Sources set!')
                else:
                    try:
                        new_ids = set(map(int, new_ids.split(',')))
                        new_ids = [sources[i - 1]['id'] for i in new_ids]
                    except:
                        self.error(self.INVALID)
                        continue
                    self.source_ids = new_ids
                    self.success('Sources set!')
            elif action == 0:
                break
            else:
                self.error(self.INVALID)

    def articles_menu(self):
        '''Display the article search menu.'''
        term = ''
        while term == '':
            term = self.yellow_input('Enter a term')
            print(self.Style.RESET_ALL)
        articles = News.search_term(term, self.source_ids)
        if len(articles) > 0:
            print(f'{str(len(articles))} results!')
            action = None
            while action != 0:
                options = '[1] View results\n'\
                          '[2] Choose article\n'\
                          '[0] Go back\n'
                action = self.create_menu('RESULTS', options)
                if action == 1:
                    [print(f"[{str(i + 1)}] {article['title']}")
                     for i, article in articles.items()]
                elif action == 2:
                    article = self.yellow_input('Enter the article #')
                    print(self.Style.RESET_ALL)
                    try:
                        article = int(article)
                        article = articles[article - 1]
                    except:
                        self.error(self.INVALID)
                        continue
                    self.show_details(article)
                    while action != 0:
                        if self.user_id != -1:
                            options = '[1] Save article\n'\
                                      '[0] Go back\n'
                        else:
                            options = '[0] Go back\n'
                        action = self.create_menu('ARTICLE', options)
                        if action == 1:
                            if self.user_id != -1:
                                res = pickle.dumps(article)
                                DB.add_article(self.user_id, res)
                                self.success('Article saved!')
                                break
                            else:
                                self.error(self.INVALID)
                        elif action == 0:
                            action = None
                            break
                        else:
                            self.error(self.INVALID)
                elif action == 0:
                    break
                else:
                    self.error(self.INVALID)
        else:
            self.error('No results.')

    def saved_menu(self):
        '''Display the saved articles menu.'''
        new = True
        action = None
        while action != 0:
            articles = DB.get_articles(self.user_id)
            ids = {i: articles[i][0] for i in articles}
            articles = {i: pickle.loads(articles[i][1]) for i in articles}
            if len(articles) > 0:
                if new:
                    print(f'{str(len(articles))} saved!')
                    new = False
                options = '[1] View saved\n'\
                          '[2] Choose article\n'\
                          '[0] Go back\n'
                action = self.create_menu('SAVED', options)
                if action == 1:
                    [print(f"[{str(i + 1)}] {article['title']}")
                     for i, article in articles.items()]
                elif action == 2:
                    article_id = 0
                    article = self.yellow_input('Enter the article #')
                    print(self.Style.RESET_ALL)
                    try:
                        num = int(article)
                        article_id = ids[num - 1]
                        article = articles[num - 1]
                    except:
                        self.error(self.INVALID)
                        continue
                    self.show_details(article)
                    while action != 0:
                        options = '[1] Remove article\n'\
                                  '[0] Go back\n'
                        action = self.create_menu('ARTICLE', options)
                        if action == 1:
                            DB.delete_article(article_id)
                            self.success('Article removed!')
                            break
                        elif action == 0:
                            action = None
                            break
                        else:
                            self.error(self.INVALID)
                elif action == 0:
                    break
                else:
                    self.error(self.INVALID)
            else:
                self.error('None saved.')
                break

    def auth_menu(self):
        '''Display the user authentication menu.'''
        if self.user_id != -1:
            self.user_id = -1
            self.success('You have logged out!')
        else:
            action = None
            while action != 0:
                options = '[1] Enter credentials\n'\
                          '[2] Create account\n'\
                          '[0] Go back\n'
                action = self.create_menu('LOGIN', options)
                if action == 1:
                    username = self.yellow_input('Enter username')
                    password = getpass.getpass('Enter password:')
                    print(self.Style.RESET_ALL)
                    self.user_id = DB.auth_user(username, password)
                    if self.user_id != -1:
                        self.success('Welcome back!')
                        break
                    else:
                        self.error('Invalid credentials.')
                elif action == 2:
                    username = self.yellow_input('Enter username')
                    password = getpass.getpass('Enter password:')
                    print(self.Style.RESET_ALL)
                    res = DB.add_user(username, password)
                    if res != False:
                        self.user_id = DB.auth_user(username, password)
                        self.success('Account created!')
                        break
                    else:
                        self.error('User already exists.')
                elif action == 0:
                    break
                else:
                    self.error(self.INVALID)

    def run(self):
        '''Entry point for the application.'''
        self.greeting()

        action = None
        while action != 0:
            if action == None:
                action = self.main_menu()

            if action == 1:
                self.sources_menu()
            elif action == 2:
                self.articles_menu()
            elif action == 3:
                if self.user_id != -1:
                    self.saved_menu()
                else:
                    action = 4
                    continue
            elif action == 4:
                self.auth_menu()
            elif action == 0:
                self.success('Goodbye!')
                break
            else:
                self.error(self.INVALID)
            action = None


if __name__ == '__main__':
    Main().run()
