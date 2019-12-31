from inspect import getargspec


class EventSourceMixin(object):
    def __init__(self):
        self.events_and_observing_methods = {}

    def when_event_do(self, event_name, observing_method):
        if event_name not in self.events_and_observing_methods:
            self.events_and_observing_methods[event_name] = []
        self.events_and_observing_methods[event_name].append(observing_method)

    def when_event_do_not(self, event_name, observing_method):
        if event_name in self.events_and_observing_methods:
            if observing_method in self.events_and_observing_methods[event_name]:
                self.events_and_observing_methods[event_name].remove(observing_method)

    def trigger_event(self, event_name, object_to_pass=None):
        if event_name in self.events_and_observing_methods:
            for observing_method in self.events_and_observing_methods[event_name]:
                if getargspec(observing_method).args.__len__() == 2:
                    observing_method(object_to_pass)
                else:
                    observing_method()
