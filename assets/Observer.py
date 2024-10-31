''' Observer/subscirber class.

INSTRUCTIONS:
Assume that you want to detect changes in Eleana instance:
to notify subprogram in Notify instance.
1. Initiate empty list of observers in __init__() of Eleana class:

    self._observers = []

2. Add the observer methods in Eleana class to allow to attach
   detach or notify observer that something changes:
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for observer in self._observers:
            observer.update(self)

3. Create setter for attribute you want to observe and notify:
    For example we want to observe changes in self.selection['first']
    then the setter should be similar to this:

    def set_selections(self, first):
        self.selections['first'] = first
        self.notify()

    This means that you should change the value of self.selections['first']
    using the setter. For example in you instantiate Eleana:

        eleana = Eleana()    <-- This creates instance
        eleana.set_selections(2)

    This will involve setter, sets the value to 2 and invoke
    eleana.notify() method.

4. Now you must create subscriber that will receive the notification.
    Assume that the program is an instance of Subscriber class:

        subscriber = Subscriber(parameters, OBSERVED_OBJ)

    Within the Subscriber() class you should import THIS file
    containing Observer() class.

        from "file_containing_Observer" import Observer

5. Instantiate Observer() class within __init__() method:

        self.eleana = OBSERVED_OBJ    <-- this creates reference to our eleana instance
                                          that we want to monitor
        self.observer = Observer(self.eleana)

    OBSERVED_OBJ is the instance of the class in which we
    want to detect changes. This will be "eleana" in our example.
    Therefore you must first pass eleana as instance to Subscriber

6. Create data_changed(self) method in Subscriber() class that will handle
   the event of changes in eleana.selections['first'] using the setter.
   If you don't you the setter then the changes in the value will not be notified.

7. Upon closing the subscriber you must detach the self.observer from the list of registered observers
   in eleana._observers list. Otherwise the observer will still work even if the subscriber window is closed:

        self.eleana.detach(self.observer)

   This will remove the created observers and the data_changed() method will no longer be triggered.
'''

class Observer:
    def __init__(self, observed_instance, subscriber_instance):
        self.observed = observed_instance
        self.subscriber = subscriber_instance
        self.observed.attach(self)
    def update(self, subject, variable=None, value=None):
        if subject == self.observed:
            self.subscriber.data_changed(variable=variable, value=value)
