from colorama import Fore, Back, Style


class Menu:
    '''Menu class
    Provides base methods for menu-driven classes.
    '''

    INVALID = '\nInvalid input.'

    def __init__(self):
        '''Constructor - Assigns class properties.'''
        self.Fore = Fore
        self.Back = Back
        self.Style = Style

    class Decor:
        '''Class object to hold underline and reverse ASCII values.'''
        UNDERLINE = '\u001b[4m'
        REVERSE = '\u001b[7m'

    def greeting(self):
        '''Display the welcome message.'''
        print(f'{self.Fore.YELLOW}{self.Back.CYAN}{self.Style.BRIGHT}' +
              f'|*********************************|\n' +
              f'| WELCOME TO THE TOP NEWS SEARCH! |\n' +
              f'|_________________________________|')
        print(self.Style.RESET_ALL)

    def show_details(self, article):
        '''Display the formatted details of a given article.

        Args:
            article: Article JSON object.
        '''
        print(
            f"{self.Decor.UNDERLINE}SOURCE{self.Style.RESET_ALL}: {article['source']['name']}")
        print(
            f"{self.Decor.UNDERLINE}TITLE{self.Style.RESET_ALL}: {article['title']}")
        print(
            f"{self.Decor.UNDERLINE}DESCRIPTION{self.Style.RESET_ALL}: {article['description']}")
        print(
            f"{self.Decor.UNDERLINE}URL{self.Style.RESET_ALL}: {article['url']}")
        print(
            f"{self.Decor.UNDERLINE}DATE{self.Style.RESET_ALL}: {article['publishedAt']}")
        print(
            f"{self.Decor.UNDERLINE}CONTENT{self.Style.RESET_ALL}: {article['content']}")

    def create_menu(self, title, menu):
        '''Display formatted output of a given menu.

        Args:
            title: Title of the menu.
            menu: Contents of the menu.

        Returns:
            int: The return value. Number of the chosen action if success. Recurse the method if error.
        '''
        print()
        print(f'{self.Fore.YELLOW}{self.Back.CYAN}{self.Style.BRIGHT}' +
              ':---------- ' + title + ' ----------:')
        print(Style.RESET_ALL)
        print(f'{self.Decor.REVERSE}{menu}{Style.RESET_ALL}')
        action = self.yellow_input('Choose option')
        print(Style.RESET_ALL)
        try:
            return int(action)
        except:
            self.error(self.INVALID)
            return self.create_menu(title, menu)

    def success(self, msg):
        '''Display a given message with success formatting.

        Args:
            msg: Message to format.
        '''
        print()
        print(f'{Fore.WHITE}{Back.GREEN}{Style.BRIGHT}{msg}')
        print(Style.RESET_ALL)

    def error(self, msg):
        '''Display a given message with error formatting.

        Args:
            msg: Message to format.
        '''
        print()
        print(f'{Fore.WHITE}{Back.RED}{Style.BRIGHT}{msg}')
        print(Style.RESET_ALL)

    def yellow_input(self, msg):
        '''Add yellow formatting to the given input.

        Args:
            msg: Input to format.

        Returns:
            string: The return value. Input with yellow formatting.
        '''
        return input(f'{Fore.YELLOW}{Style.BRIGHT}{msg}: ')
