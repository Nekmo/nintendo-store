from nintendo_store.session import NintendoStoreSession


class NintendoStoreClient:
    def __init__(self, session: NintendoStoreSession):
        self.session = session
