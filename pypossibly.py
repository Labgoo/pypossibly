import logging
import sys

class Maybe(object):
    pass


class Nothing(Maybe):
    def is_some(self):
        return False

    def is_none(self):
        return True

    def get(self):
        raise Exception('No such element')

    def or_else(self, els = None):
        if callable(els):
            return els()

        return els

    def __cmp__(self):
        if (other.__class__ == Nothing):
            return 0

        return 1


    # region Dict
    def __len__(self):
        return 0

    def __getitem__(self, key):
        return Nothing()

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    # endregion

    # region Custom representation
    def __repr__(self):
        return repr(None)

    def __str__(self):
        return str(None)

    def __unicode__(self):
        return unicode(None)

    def __nonzero__(self):
        return False

    # endregion


class Something(Maybe):
    def __init__(self, value):
        self.__value = value

    def __cmp__(self, other):
        if other.__class__ == Nothing:
            return 1

        return self.get().__cmp__(other.get())

    def is_some(self):
        return True

    def is_none(self):
        return False

    def get(self):
        return self.__value

    def or_else(self, els = None):
        return self.__value

    def __iter__(self):
        try:
            iterator = iter(self.value)
        except TypeError, te:
            iterator = iter([self.value])

        return iterator

    def __getattr__(self, name):
        try:
            return maybe(getattr(self.__value, name))
        except:
            return Nothing()

    def __setattr__(self, name, v):
        if (name == "_Something__value"):
            return super(Something, self).__setattr__(name, v)

        return setattr(self.__value, name, v)

    #region Dict
    def __len__(self):
        return len(self.__value)

    def __getitem__(self, key):
        return maybe(self.__value.get(key, None))

    def __setitem__(self, key, value):
        self.__value[key] = value

    def __delitem__(self, key):
        del self.__value[key]

    #endregion

    # region Custom representation

    def __repr__(self):
        return repr(self.__value)

    def __str__(self):
        return str(self.__value)

    def __unicode__(self):
        return unicode(self.__value)

    def __nonzero__(self):
        return True

    def __dir__(self):
        return dir(self.__value)

    def __sizeof__(self):
        return sizeof(self.__value)

    #endregion

def maybe(value):
    """Wraps an object with a Maybe instance.

      >>> maybe("I'm a value")
      "I'm a value"

      >>> maybe(None);
      None

      Testing for value:

        >>> maybe("I'm a value").is_some()
        True
        >>> maybe("I'm a value").is_none()
        False
        >>> maybe(None).is_some()
        False
        >>> maybe(None).is_none()
        True

      Simplifying IF statements:

        >>> maybe("I'm a value").get()
        "I'm a value"

        >>> maybe("I'm a value").or_else(lambda: "No value")
        "I'm a value"

        >>> maybe(None).get()
        Traceback (most recent call last):
        ...
        Exception: No such element

        >>> maybe(None).or_else(lambda: "value")
        'value'

        >>> maybe(None).or_else("value")
        'value'

      Wrap around values from object's attributes:

        class Person(object):
          def __init__(name):
            self.eran = name

        eran = maybe(Person('eran'))

        >>> eran.name
        'eran'
        >>> eran.phone_number
        None
        >>> eran.phone_number.or_else('no phone number')
        'no phone number'

      Enabled easily using NestedDictionaries without having to worry
      if a value is missing.
      For example lets assume we want to load some value from the
      following dictionary:
        nested_dict = maybe({
          'store': {
            'name': 'MyStore',
            'departments': {
                'sales': { 'head_count': '10' }
            }
          }
        })

        >>> nested_dict['store']['name']
        'MyStore'
        >>> nested_dict['store']['address']
        None
        >>> nested_dict['store']['address']['street'].or_else('No Address Specified')
        'No Address Specified'
        >>> nested_dict['store']['departments']['sales']['head_count'].or_else('0')
        '10'
        >>> nested_dict['store']['departments']['marketing']['head_count'].or_else('0')
        '0'

    """
    if isinstance(value, Maybe):
        return value
    
    if value:
        return Something(value)

    return Nothing()

if __name__ == "__main__":
    import doctest

    class Person(object):
      def __init__(self, name):
        self.name = name

    eran = Person('eran')

    globals_dict = {
      'nested_dict': maybe({
        'store': {
          'name': 'MyStore',
          'departments': {
              'sales': { 'head_count': '10' }
          }
        }
      }),
      'eran' : maybe(eran),
      'maybe': maybe
    }

    doctest.testmod(globs=globals_dict)
