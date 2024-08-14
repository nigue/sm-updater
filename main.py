from src.service.SyncUseCase import SyncUseCase


if __name__ == '__main__':
    name = 'SM-UPDATER 1.0.0'
    print(f'Init, {name}')
    use_case = SyncUseCase()
    use_case.process()
