class Flow:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        name = kwargs['name']
        return f'Hello {name}'
