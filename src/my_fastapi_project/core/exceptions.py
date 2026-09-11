class BusinessError(Exception):
    status_code = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UsernameAlreadyExists(BusinessError):
    status_code = 409

    def __init__(self, username: str):
        super().__init__(f"用户名'{username}'已存在")


class InvalidOldPassword(BusinessError):
    status_code = 400

    def __init__(self):
        super().__init__("旧密码不正确")


class OutOfStock(BusinessError):
    status_code = 400

    def __init__(self):
        super().__init__("库存不足")


class BookAlreadyExists(BusinessError):
    status_code = 409

    def __init__(self, isbn: str):
        super().__init__(f"图书'{isbn}'已存在")


class EmailAlreadyExists(BusinessError):
    status_code = 409

    def __init__(self, email: str):
        super().__init__(f"邮箱'{email}'已被使用")
