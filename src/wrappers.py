import time

def retry_this_if_error(max_attempts: int = 2):
    '''Wrapper that executes the function again, until max_attempts is
    reached, upon any exception.

    Keyword arguments:
    max_attempts -- maximum number of attempts of execution, defaults to 2.
    '''

    def retry_wrapper(func):

        def wrapper(*args, **kwargs):

            current_retry_attempt = 1
            while current_retry_attempt <= max_attempts:
                try:
                    result = func(*args, **kwargs)
                    return result

                except:
                    current_retry_attempt += 1
            
            return None    
        return wrapper
    return retry_wrapper