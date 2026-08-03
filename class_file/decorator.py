def decorator(func):

    def wrapper():
        print("Before Function")

        

        print("After Function")
        func()

    return wrapper


@decorator
def hello():
    print("Hello")


hello()