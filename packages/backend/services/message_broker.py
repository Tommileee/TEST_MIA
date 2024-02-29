from shared.mq.broker import Broker

if __name__ == "__main__":
    broker = Broker()
    try:
        print("Starting message broker")
        broker.run()
    except KeyboardInterrupt:
        print("Shutting down message broker")
        del broker
        print("Message broker shut down")
