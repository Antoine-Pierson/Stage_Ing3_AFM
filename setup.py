from cx_Freeze import setup, Executable

setup(
    name='AFM',
    version='0.1',
    author='Pierson Antoine',
    executables=[Executable('__main__.py')]
)
