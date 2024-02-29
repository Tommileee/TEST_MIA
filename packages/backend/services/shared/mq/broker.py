import zmq


class Broker:
    FRONTEND_PORT = 5555
    BACKEND_PORT = 5556

    def __init__(self) -> None:
        # Initialize a zeromq context
        self.context = zmq.Context()

        # Initialize frontend and backend sockets
        self.frontend = self.context.socket(zmq.XSUB)
        self.backend = self.context.socket(zmq.XPUB)
        self.frontend.bind(f"tcp://*:{self.FRONTEND_PORT}")
        self.backend.bind(f"tcp://*:{self.BACKEND_PORT}")

    def run(self) -> None:
        # Proxy messages between frontend and backend
        zmq.proxy(self.frontend, self.backend)

    def __del__(self) -> None:
        self.frontend.close()
        self.backend.close()
        self.context.term()