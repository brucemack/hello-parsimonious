import pytest
from model.util import Observable, Observer, do_notification_cycle


class Instrument(Observable):

    def __init__(self):
        super().__init__()
        self.price = 0

    def set_price(self, p: float):
        self.price = p
        self.record_change()

    def get_price(self) -> float:
        return self.price

notification_count = 0

class Controller(Observer):

    def __init__(self):
        pass

    def notify(self, obs: Instrument):
        print("Notification with price=", obs.get_price())
        global notification_count
        notification_count = notification_count + 1


def test_1():

    global notification_count

    i0 = Instrument()
    i1 = Instrument()
    c = Controller()
    i0.add_observer(c)
    i1.add_observer(c)

    print("Starting cycle 1")
    i0.set_price(66)
    i0.set_price(77)
    assert notification_count == 0
    do_notification_cycle()
    print("Ending cycle 1")
    assert notification_count == 1

    print("Starting cycle 2")
    do_notification_cycle()
    print("Ending cycle 2")
    assert notification_count == 1
