# -*- coding: utf-8 -*

from .. import Matcher, default_matcher


class _raise_error(Matcher):
    def __init__(self, expected, *args):
        self._expected = expected
        self._args = args

    def __call__(self, *args, **kwargs):
        return _raise_error(*args, **kwargs)

    def _match(self, subject):
        try:
            subject()
        except self._expected as exc:
            if len(self._args) != 0:
                actual_value = exc.args[0]
                expected_value = default_matcher(self._args[0])
                result, _ = expected_value._match(actual_value)
                return result, ['{} raised with {!r}'.format(type(exc).__name__, actual_value)]

            return True, ['{} raised'.format(type(exc).__name__)]

        except Exception as err:
            return False, ['{} raised'.format(type(err).__name__)]
        else:
            return False, ['no exception raised']

    def _failure_message(self, subject, reasons):
        return '\nexpected: {!r} to {}\n     but: {}'.format(
            subject,
            repr(self),
            '\n          '.join(reasons))

    def _failure_message_negated(self, subject, reasons):
        return '\nexpected: {!r} not to {}\n     but: {}'.format(
            subject,
            repr(self),
            '\n          '.join(reasons))


raise_error = _raise_error(Exception)
