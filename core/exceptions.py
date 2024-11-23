class IDErorr(KeyError):
    def __init__(self, message: str = 'Такого ID не существует.', *args: object) -> None:
        self.message = message
        super().__init__(message, *args)
