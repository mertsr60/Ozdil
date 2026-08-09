# -*- coding: utf-8 -*-

class OzdilError(Exception):
    def __init__(self, friendly_type, message, lineno, original_exception=None):
        super().__init__(message)
        self.friendly_type = friendly_type
        self.message = message
        self.lineno = lineno
        self.original_exception = original_exception

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class InputRequestException(Exception):
    def __init__(self, prompt):
        self.prompt = prompt

