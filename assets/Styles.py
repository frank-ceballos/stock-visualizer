colors = {'background': 'rgb(3,8,18)', 'text': 'rgb(255,255,255)',
          'foreground': 'rgb(24,35,47)', 'navBackground': 'rgb(24,35,47)',
          'bullish': 'rgb(27,198,120)', 'bearish': 'rgb(219,90,65)',
          'gridlines': 'rgb(60,69,82)', 'H1BGColor': 'rgb(19,21,23)', 
          'H1FontColor': 'rgb(255,255,255)', 'axes': 'rgb(75,75,75)',
          'hoverBackground': 'rgb(0,8,41)', 'hoverBorder': 'rgb(255,255,255)',
          'graphBackgroud': 'rgb(13,20,31)',
          'shadow': 'rgba(29,174,102,0.2)'
}

styleDropdown =  {'background':colors['navBackground'], 
                  'border-color': colors['bullish'], 
                  'color': 'white', 'margin': 0, 'padding': 0}

style_card2 = {'margin-bottom': 2, 'margin-top': 2, 'margin-right': 0,
              'margin-left': 0, 'padding-left':0, 'overflow': 'inherit', 'height': 750}

style_info = {'margin-bottom': 2, 'margin-top': 2, 'margin-right': 6,
              'margin-left': 2, 'padding-left':2}

ticker_picker_card = {'margin-bottom': 1, 'margin-top': 2, 'margin-right': 2,
                        'margin-left': 2, 'padding-left':0}

class DashComponentStyles(): 
    
    def __init__(self):
        self.colors = colors
        self.styleDropdown =  styleDropdown
        self.ticker_picker_card = ticker_picker_card
        self.style_card2 = style_card2
        self.style_info = style_info

    