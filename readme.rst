 Why Gevent
 ==========

 It's about getting things done at the same time. In python we have three ways to do
 this.

 Threads
 -------

 The threading library and servers such as Paste.

 For example it's easy to create a very `simple tcp echo server`_ with the threading library

 .. _`simple tcp echo server`: threadecho.py

 This is easy to understand, where each new connection spawns its own thread which loops and blocks
 when waiting for each line.

 So what's wrong with using threads? In most cases nothing. However if you want to deal with
 a lot network traffic using threads you encounter two issues.

 Processes
 ---------

 New libraries such as multiprocessing look interesting to for this but we're not going to talk about
 this here.

 Asynchronous IO Frameworks
 --------------------------

 There are lots

 e.g. StacklessPython, Fibra, Cogen, Greenlet, Gevent, Eventlet, Circuits, Twisted, Kamaela, Concurrence,
 Parallel Python, pprocess, pysage, pypes, diesel, Chiral, tornado

 Essentially what they do is run everything in a single thread but instead work with the
 operating system to switch with of your code is worked on 


 Overhead
 ~~~~~~~~

 Every thread means context switches occur which means a certain amount of work needs to be done to
 save of the current thread and then reinstate the previous state of the next thread. Below is an attempt
 to measure that overhead.

 .. image:: https://github.com/zacharyvoase/gevent-threading-comparison

 This is for gevent but the result would be similar for any async io framework. The more the threads
 the more the overhead becomes a problem.

 Global Interpreter Lock
 ~~~~~~~~~~~~~~~~~~~~~~~

 The GIL makes maintaining the python interpreter easier and in most cases isn't a problem.
 There are many articles about why the GIL exists and it's implications.

  - http://jessenoller.com/2009/02/01/python-threads-and-the-global-interpreter-lock/