from model.util import CompositeType, CompositeObject, register_type, get_type, get_array_type_of, \
    create_object, create_object_array, WObject, ArrayObject
from model.util import Observable, Observer, do_notification_cycle

import pytest

notification_count = 0


class Controller(Observer):

    def __init__(self):
        pass

    def notify(self, obs: WObject):
        global notification_count
        notification_count = notification_count + 1


def test_1():

    t = register_type(CompositeType("Department"))
    t.add_field("name", get_type("String"), True)

    t = register_type(CompositeType("Person"))
    t.add_field("name", get_type("String"), True)
    t.add_field("age", get_type("Float"), True)
    t.add_field("department", get_type("Department"), True)
    t.add_field("team", get_array_type_of("Person"), True)

    dept = create_object("Department")
    s0 = create_object("String")
    s0.set_value("Rescue")
    assert s0.get_value() == "Rescue"
    dept.set("name", s0)
    assert dept.get("name").get_value() == "Rescue"

    person_1: CompositeObject = create_object("Person")
    s0 = create_object("String")
    s0.set_value("Bruce")
    person_1.set("name", s0)
    person_1.set("department", dept)

    assert person_1.get("department").get("name").get_value() == "Rescue"

    person_2 = create_object("Person")
    s0 = create_object("String")
    s0.set_value("Henry")
    person_2.set("name", s0)
    person_2.set("department", dept)

    assert person_2.get("department").get("name").get_value() == "Rescue"

    # Now test array stuff
    a = create_object_array("Person")
    assert a.get_type().get_name() == "array of Person"
    person_1.set("team", a)
    assert person_1.get("team").length() == 0
    # Here is where the item gets added to the array
    person_1.get("team").add(person_2)
    assert person_1.get("team").length() == 1
    assert person_1.get("team").get(0).get("name").get_value() == "Henry"

    # Validate that the types are enforced
    with pytest.raises(Exception):
        person_1.get("team").add(dept)
    with pytest.raises(Exception):
        person_1.set("age", dept)

    # Do some observables
    c = Controller()

    person_1.get("name").add_observer(c)
    person_1.get("team").add_observer(c)

    # Change the value.  We should see the observer fire
    person_1.get("name").set_value("Laura")

    # Add another person.  This should cause the observer to fire
    person_3 = create_object("Person")
    s0 = create_object("String")
    s0.set_value("Izzy")
    person_3.set("name", s0)
    person_3.set("department", dept)
    # Here is where the item gets added to the array
    person_1.get("team").add(person_3)

    do_notification_cycle()
    assert notification_count == 2

    # Create an array of persons
    li = ArrayObject(get_array_type_of("Person"))
    li.add_observer(c)
    print("Changing ...")
    li.add(person_1)
    li.add(person_2)
    li.add(person_3)
    assert li.length() == 3
    do_notification_cycle()
    # Note here that the notifications are batched and we only get one call
    # even though three things were added to the list
    assert notification_count == 3