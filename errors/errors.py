class ErrorCodes:
    UNSUPPORTED_RATIO = 1001
    FILE_NOT_FOUND = 1002
    INVALID_FILE_FORMAT = 1003
    SUBPROCESS_ERROR = 1004
    CUSTOM_ERROR = 1005

class ErrorMessages:
    messages = {
        ErrorCodes.UNSUPPORTED_RATIO: '지원되지 않는 비율입니다.',
        ErrorCodes.FILE_NOT_FOUND: '파일을 찾을 수 없습니다.',
        ErrorCodes.INVALID_FILE_FORMAT: '잘못된 파일 형식입니다.',
        ErrorCodes.SUBPROCESS_ERROR: '명령 실행 중 오류가 발생했습니다.',
        ErrorCodes.CUSTOM_ERROR: '사용자 정의 오류가 발생했습니다.'
    }

    @classmethod
    def get_message(cls, error_code):
        return cls.messages.get(error_code, '알 수 없는 오류입니다.')
