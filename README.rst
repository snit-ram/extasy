h1. EXTasy

EXTasy is a "Behaviour-Driven-Development-style":http://behaviour-driven.org tool written in Python that aims to make it easier to write automated acceptance tests for ExtJS interfaces. It is based on "Pyccuracy":http://github.com/heynemann/pyccuracy and It improves the readability of those tests by using a structured natural language - and a simple mechanism to extend this language - so that both developers and customers can collaborate and understand what the tests do.

h2. Get in touch with the team

If you have further questions, please contact the team:

  * "snit-ram":http://github.com/snit-ram ("@snit_ram":http://twitter.com/snit_ram)


EXTasy
=======

EXTasy is a Cucumber-like BDD tool for ExtJS developers. It is written in python and built on top of Pycukes.


Installation
=====

You can install it using Python's easy_install::

    $ easy_install extasy

Or You can download source code and install using setup.py script::

    $ python setup.py install



Usage
=====

First, make sure you have installed story_runner, pyhistorian, pycukes and extasy.
By default, if you just call ``extasy`` from your command line into some dir, it will look for a ``stories`` dir (expecting your stories files are there).
Each story file by convention ends with .story, like ``calculator.story``.

So, lets say you have the directory tree::

 |-- calculator
    `-- stories
        |-- calculator.story


To run your stories, you can simple call::

    $ extasy

Or if you can specify exactly what stories run::
    
    $ extasy stories/calculator.story

