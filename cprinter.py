import sys
#colors for the text
colors = {'black': '30;',
    'red': '31;',
    'green': '32;',
    'yellow': '33;',
    'blue': '34;',
    'purple': '35;',
    'cyan': '36;',
    'white': '37;',
    '30;': 'black',
    '31;': 'red',
    '32;': 'green',
    '33;': 'yellow',
    '34;': 'blue',
    '35;': 'purple',
    '36;': 'cyan',
    '37;': 'white'
}
#colors for the background
back_colors = {'black': '40m',
    'red': '41m',
    'green': '42m',
    'yellow': '43m',
    'blue': '44m',
    'purple': '45m',
    'cyan': '46m',
    'white': '47m',
    '40m': 'black',
    '41m': 'red',
    '42m': 'green',
    '43m': 'yellow',
    '44m': 'blue',
    '45m': 'purple',
    '46m': 'cyan',
    '47m': 'white'
}
#text option codes
text_options = {
    'bold': '1;',
    'italic': '3;',
    'underline': '4;',
    'blink': '5;'
}
        

def cprint(*args, **kwargs):
    '''
    Stand alone function for printing in color
    '''
    colo = '' if kwargs.get('color') == None else colors[kwargs['color']]
    bkgnd = '40m' if kwargs.get('background') == None else back_colors[kwargs['background']]

    bold = '' if not kwargs.get('bold', False) else '1;'
    underline = '' if not kwargs.get('underline', False) else '4;'
    italic = '' if not kwargs.get('italic', False) else '3;'
    blink = '' if not kwargs.get('blink', False) else '5;'
    no_effect = not bold == underline == italic == blink 
    style ='0;' if no_effect else ''.join((bold, underline, italic, blink))

    stream = kwargs.get('stream', sys.stdout)   
    end = kwargs.get('end', '\n')
    sep = kwargs.get('sep', '')

    print(f'\033[{style}{colo}{bkgnd}{sep.join(args)}\033[0;37;40m', file = stream, end = end)
    
    
class cprinter:
    '''
    print stream object with color options
    '''
    
    def __init__(self, **kwargs):
        #color of the text
        self._color = '' if kwargs.get('color') == None else colors[kwargs['color']]
        #color of the bacground
        self._background = '40m' if kwargs.get('background') == None else back_colors[kwargs['background']]

        #text options dictionary
        self._text_opts = {}
        self._text_opts['bold'] = kwargs.get('bold', False)
        self._text_opts['underline'] = kwargs.get('underline', False) 
        self._text_opts['italic'] = kwargs.get('italic', False) 
        self._text_opts['blink'] = kwargs.get('blink', False) 
        #style string

        self._style = None
        self._update_style()

        self._stream = kwargs.get('stream', sys.stdout)
        self.end = kwargs.get('end', '\n')
        self.sep = kwargs.get('sep', '')
    

    def _update_style(self):
        '''
        update the style escape string for printing
        '''
        #if no special text options are chosen
        if not any(self._text_opts.values()):
            self._style = '0;'
        else:
            self._style = ''.join([text_options[k] for k,v in self._text_opts.items() if v])       

        self._style = ''.join((self._style, self._color, self._background))
        

    def print(self, *args, **kwargs):
        '''
        print with all currently set options
        '''
        stream = kwargs.get('stream', self.stream)
        end = kwargs.get('end', self.end)
        sep = kwargs.get('sep', self.sep)

        print(f'\033[{self._style}{sep.join(args)}\033[0;40m', file = stream, end = end)

    def __lshift__(self, arg):
        '''
        for those you who really like C++ but really don't want to code in it
        by default this doesn't print out the end string to make it more consistent with
        C++ style output.
        '''
        print(f'\033[{self._style}{str(arg)}\033[0;40m', file = self.stream, end = '')
        return self
    
    
    @property
    def color(self):
        return colors[self._color]

    @color.setter
    def color(self, color):
        self._color = colors[color]
        self._update_style()

    @property
    def background(self):
        return back_colors[self._background]

    @background.setter
    def background(self, background):
        self._background = back_colors[background]
        self._update_style()

    @property
    def bold(self):
        return self._text_opts['bold']
    
    @bold.setter
    def bold(self, val):
        if type(val) != bool:
            raise Exception("text style must be a boolean")

        self._text_opts['bold'] = val
        self._update_style()

    @property
    def italic(self):
        return self._text_opts['italic']
    
    @italic.setter
    def italic(self, val):
        if type(val) != bool:
            raise Exception("text style must be a boolean")

        self._text_opts['italic'] = val
        self._update_style()

    @property
    def underline(self):
        return self._text_opts['underline']
    
    @underline.setter
    def underline(self, val):
        if type(val) != bool:
            raise Exception("text style must be a boolean")

        self._text_opts['underline'] = val
        self._update_style()

    @property
    def blink(self):
        return self._text_opts['blink']
    
    @blink.setter
    def blink(self, val):
        if type(val) != bool:
            raise Exception("text style must be a boolean")

        self._text_opts['blink'] = val
        self._update_style()

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, new_stream):
        #close the stream if it is not stderr or stdout
        if not self._stream == sys.stdout or self._stream == sys.stderr:
            self._stream.close()
        self._stream = new_stream
    
