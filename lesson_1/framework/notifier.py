class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for obs in self.observers:
            obs.update(self)


class SmsNotifier(Observer):
    def update(self, subject):
        print(f'<SMS> {subject.students[-1].name} was added')


class EmailNotifier(Observer):
    def update(self, subject):
        print(f'<EMAIL> {subject.students[-1].name} was added ')
