from unittest import main, TestCase

class HelloWorldTest(TestCase):
    def testHelloMsg(self):
        from hello import hello
        self.assertEqual(hello(), "Hello, world!")

if __name__ == "__main__":
    main()
