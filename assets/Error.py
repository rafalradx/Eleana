from modules.CTkMessagebox.ctkmessagebox import CTkMessagebox
class Error:
    @classmethod
    def show(cls, info = '', details = '', title = ''):
        message = info + f'\n\nDetails:\n{details}'
        if not title:
            title = 'Error'
        error = CTkMessagebox(title=title, message=message, icon='cancel')
    def ask(self):
        pass
