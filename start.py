from my_package import __main__

__main__.__name__ = '__main__' # Make it look like `my_package.__main__` is the main script
__main__.run()  # Call your main function if required