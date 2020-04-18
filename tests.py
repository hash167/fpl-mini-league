#!/usr/bin/env python

import coverage
import pytest

# define coverage to check app module
c = coverage.coverage(branch=True, include='src/*')
c.start()

# discover finds tests in 'tests' folder
pytest.main(["-x", "./tests"])

c.stop()
c.report()
