import unittest2
import colour_runner.runner

loader = unittest2.TestLoader()
tests = loader.discover('.')
testRunner = colour_runner.runner.ColourTextTestRunner(verbosity=2)
#testRunner = unittest2.runner.TextTestRunner(verbosity=2)
testRunner.run(tests)


