class ErrorCodes:
    UNSUPPORTED_RATIO = 1001
    FILE_NOT_FOUND = 1002
    INVALID_FILE_FORMAT = 1003

class ErrorMessages:
    messages = {
        ErrorCodes.UNSUPPORTED_RATIO: '지원되지 않는 비율입니다.',
        ErrorCodes.FILE_NOT_FOUND: '파일을 찾을 수 없습니다.',
        ErrorCodes.INVALID_FILE_FORMAT: '잘못된 파일 형식입니다.'
    }

    @classmethod
    def get_message(cls, error_code):
        return cls.messages.get(error_code, '알 수 없는 오류입니다.')
