import sublime


class Loader():
    """ Shows a loader in the status bar, untill you set instance.done = True
    Example usage:

        loader = Loader('Loading some stuff...')  #loader starts spinning
        # after some operations (like api calls)
        loader.done = True  # loader stops

    """
    def __init__(self, message, success_message=''):
        self.message = message
        self.success_message = success_message
        self.addend = 1
        self.size = 10
        sublime.set_timeout(lambda: self.run(0), 50)

    def run(self, i):
        if hasattr(self, 'done') and self.done is True:
            return sublime.status_message(self.success_message)

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('{0} [{1}={2}]'.format(
            self.message,
            ' ' * before,
            ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 50)
