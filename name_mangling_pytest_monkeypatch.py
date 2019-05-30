"""
Some examples of python classes and name mangling and monkeyPatching for tests and attributes of a class
"""


class monkeyTest():
    def __init__(self, x):
        self.createCategoryMap(x)
        self.createSession()
        self.a = 1

    def createCategoryMap(self, x):
        self._categories = {'a': x, 'b': x+1}
        self.__dcat = {'g': x+2, 'h': x+3}
        print('In createCategory Map self._categories:{}'.format(self._categories))
        print('In createCategory Map self.__dcat:{}'.format(self.__dcat))


    def createSession(self):
        self.session = 1
        print("In session self._categories:{}".format(self._categories))
        self._categories['t'] = 4
        print("In session self._categories:{}".format(self._categories))

        print("In session self.__dcat:{}".format(self.__dcat))
        self.__dcat['i'] = 4
        print("In session self.__dcat:{}".format(self.__dcat))


def test_createCategoryMap(monkeypatch):

    obj = monkeyTest(2)
    print("dir of monkeyTest instance :{}".format(dir(obj))) # Notice _monkeyTest__dcat. This is name mangling
    """
    https://stackoverflow.com/questions/1301346/what-is-the-meaning-of-a-single-and-a-double-underscore-before-an-object-name
    
    ._variable is semiprivate and meant just for convention

    .__variable is often incorrectly considered superprivate, while it's actual meaning is 
    just to namemangle to prevent accidental access[1]

    .__variable__ is typically reserved for builtin methods or variables

    You can still access .__mangled variables if you desperately want to. 
    The double underscores just namemangles, or renames, the variable to something like instance._className__mangled"""


    print(getattr(obj, '_categories'))
    monkeypatch.setattr(obj, '_categories', {'s':2})
    monkeypatch.setattr(obj, '_monkeyTest__dcat', {'j': 2})

    assert obj._categories == {'s': 2}
    assert obj._monkeyTest__dcat == {'j': 2}

    obj.createSession()

    assert obj._categories == {'s': 2, 't': 4}
    assert obj._monkeyTest__dcat == {'i': 4, 'j': 2}

    assert obj.a == 1






