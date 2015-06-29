import zope.interface


class IFoo(zope.interface.Interface):
    """Foo blah blah"""

    x = zope.interface.Attribute("""X blah blah""")

    def bar(q, r=None):
        """bar blah blah"""


class Foo:

    zope.interface.implements(IFoo)

    def __init__(self, x=None):
        self.x = x

    def bar(self, q, r=None):
        return q, r, self.x

    def __repr__(self):
        return "Foo(%s)" % self.x

print IFoo.implementedBy(Foo)
