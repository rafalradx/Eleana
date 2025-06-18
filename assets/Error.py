from modules.CTkMessagebox.ctkmessagebox import CTkMessagebox

class Error:
    @classmethod
    def show(cls, info = '', details = '', title = '', master = None):
        if details:
            message = info + f'\n\nDetails:\n{details}'
        else:
            message = info
        if not title:
            title = 'Error'
        error = CTkMessagebox(title=title, message=message, icon='cancel', master = master)

    @classmethod
    def ask_for_option(self, option, info = '', details = '', title = '', option_2 = 'OK'):
        if details:
            message = info + f'\n\nDetails:\n{details}'
        else:
            message = info
        if not title:
            title = 'Dialog'
        question = CTkMessagebox(master = master, title=title, message=message, icon="warning", option_1=option_2, option_2=option)
        answer = question.get()
        return answer
