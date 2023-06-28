from flask_login import current_user

class UsersPolicy:
    def __init__(self, record):
        self.record = record

    def show(self):
        return True

    def delete(self):
        return current_user.is_admin

    def new(self):
        return current_user.is_admin

    def edit(self):
        if current_user.is_admin or current_user.is_moder:
            return True
        return False

    def show_review(self):
        if current_user.is_moder:
            return True
        return False
    
