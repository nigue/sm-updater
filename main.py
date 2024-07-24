from src.service.SyncUseCase import SyncUseCase


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Init, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    use_case = SyncUseCase()
    use_case.process()


if __name__ == '__main__':
    print_hi('SM-UPDATER 1.0.0')
