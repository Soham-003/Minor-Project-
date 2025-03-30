import sys

def error_info(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno
    error_message = f"Error: {str(error)} in {file_name} at line {line_no}"
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error = error_info(error_message,error_detail)

    def __str__(self):
        return self.error

if __name__ == "__main__":
    try:
        print(1/0)
    except Exception as e:
        raise CustomException(e,sys)            