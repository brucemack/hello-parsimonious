from typing import List, Mapping, Tuple

class Observable:
    """ Allows an object to generate notifications when it changes. """

    def __init__(self):
        self._observers = []
        self._update_version = 0
        self._notification_version = 0

    def add_observer(self, o: 'Observer'):
        self._observers.append(o)

    def notify_observers(self):
        # If a notification has happened for this version of the observable
        # then we can skip notification generation - nothing left to do.
        if self._notification_version >= self._update_version:
            return

        # Make a local copy of the state in case something changes during notification
        observers_copy = self._observers[:]
        update_version_copy = self._update_version

        # Fire the callback on all observers and then move forward the notification
        # version so that we know that everyone has seen the starting version
        for observer in observers_copy:
            observer.notify(self)
        self._notification_version = update_version_copy

    def record_change(self):
        """ Call this method when the observable has changed.
            A notification is scheduled for this observable.  Duplicates are suppressed
            during the notification generation process. """
        self._update_version = self._update_version + 1
        changed_observables.append(self)


class Observer:

    def notify(self, observable: Observable):
        pass


# This is the list of observables that have changes
changed_observables: List[Observable] = []


def do_notification_cycle():
    # Notification happens from a copy to avoid corruption
    copy_changed_observables: [Observable] = changed_observables[:]
    for changed_observable in copy_changed_observables:
        changed_observable.notify_observers()



# ----- Type Related ---------------------------------------------------------

class WFieldType:
    """ Definition information for the field of a composite type. """

    _type: 'WType'
    _is_required: bool

    def __init__(self, field_type: 'WType', is_required: bool):
        self._type = field_type
        self._is_required = is_required

    def get_type(self):
        return self._type

    def is_required(self):
        return self._is_required


class WType:

    _name: str

    def __init__(self, name: str):
        self._name = name

    def get_name(self):
        return self._name


class SimpleType(WType):

    def __init__(self, name: str):
        super().__init__(name)


class CompositeType(WType):

    _fields: Mapping[str, WFieldType]

    def __init__(self, name: str):
        super().__init__(name)
        self._fields = dict()

    def add_field(self, name: str, field_type: WType, is_required: bool):
        self._fields[name] = WFieldType(field_type, is_required)

    def get_field_type(self, name: str) -> WType:
        return self._fields[name].get_type()


class ArrayType(WType):

    _items_type: WType

    def __init__(self, items_type: WType):
        super().__init__("array of " + items_type.get_name())
        self._items_type = items_type

    def get_items_type(self):
        return self._items_type


# This is where the known types are registered
type_registry: Mapping[str, WType] = dict()
array_type_registry: Mapping[str, WType] = dict()


def register_type(t: WType) -> WType:
    """ Makes a type known to the typing system """
    type_registry[t.get_name()] = t
    return t


def get_type(type_name: str) -> WType:
    """ Gets the WType object for the named type. """
    if type_name not in type_registry:
        raise Exception("Unknown type: " + type_name)
    return type_registry[type_name]


def get_array_type_of(type_name: str) -> WType:
    """ Gets the array type that corresponds to the type name provided.
        A WType is created internally if necessary.  """
    if type_name not in type_registry:
        raise Exception("Unknown type: " + type_name)
    if type_name not in array_type_registry:
        array_type_registry[type_name] = ArrayType(get_type(type_name))
    return array_type_registry[type_name]


# Register some built-in types
register_type(SimpleType("String"))
register_type(SimpleType("Float"))

# ------ Object Related -----------------------------------------------------


class WObject(Observable):

    _type: [WType]

    def __init__(self, t: WType):
        super().__init__()
        self._type = t

    def get_type(self):
        return self._type

    def is_array(self):
        return False


class ScalarObject(WObject):
    """ A simple object that contains a single value. """

    _value: any

    def __init__(self, t: WType):
        super().__init__(t)

    def get_value(self) -> any:
        return self._value

    def set_value(self, value: any):
        self._value = value
        self.record_change()


class ArrayObject(WObject):
    """ An object that holds a list of other objects.
        Change notifications are generated when things are added or removed from the list. """

    _items: List[WObject]

    def __init__(self, t: WType):
        super().__init__(t)
        self._items = []

    def is_array(self):
        return True

    def get(self, index: int) -> WObject:
        return self._items[index]

    def add(self, item: WObject):
        # Validation of the type being put into the array
        if item.get_type() != self.get_type().get_items_type():
            raise Exception("Invalid type")
        self._items.append(item)
        # Let the observers know that something changed
        self.record_change()

    def length(self) -> int:
        return len(self._items)


class CompositeObject(WObject):

    _fields: Mapping[str, WObject]

    def __init__(self, t: WType):
        super().__init__(t)
        self._fields = dict()

    def get(self, name: str) -> WObject:
        if name not in self._fields:
            raise Exception("Field not defined: " + name)
        return self._fields[name]

    def set(self, name: str, field: WObject):
        # Validation of the type being put into the array
        ft: WType = self._type.get_field_type(name)
        if field.get_type() is not ft:
            raise Exception("Invalid type.  Expected " + ft.get_name() + " got " + field.get_type().get_name())
        self._fields[name] = field


def create_object(type_name: str) -> WObject:
    t = get_type(type_name)
    if isinstance(t, SimpleType):
        return ScalarObject(t)
    elif isinstance(t, CompositeType):
        return CompositeObject(t)
    else:
        raise Exception("Type not supported")


def create_object_array(type_name: str):
    return ArrayObject(get_array_type_of(type_name))


