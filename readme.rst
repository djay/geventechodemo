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

Node vs Twisted vs GEvent
~~~~~~~~~~~~~~~~~~~~~~~~~

They do the same kind of thing and there are differences in libraries available,
underlying os switching library used etc, but for the purposes of this article we're
going to concentrate of the coding style differences.

Take the following example::

  .. include:: <threadecho2.py>

It's main thread will start a new thread for each connection. Each connection thread
will perform a blocking call to readline, perform another blocking call to urlopen,
a third blocking call to write that result back on it's TCP/IP connection... then
repeat. It's pretty easy to understand.

Now let's look at the basic twisted version::

  .. include:: <twistedecho2.py>

Now instead of loops we have callbacks, also called boomerang code. Python doesn't support
  full closures, ie inline anonymous functions. The consequence is that you have to read
  your code backwards. The code executed after d.addCallback(callback) is defined in
  the previous few lines. In a simple example such as this it's not too hard to understand
  but with a more complex application this can get confusing.

If we look at the node.js example

  .. include:: <nodeserver.js>

Closures have made it somewhat easier to read. The callbacks are inline with the call
and you can read code in the order it is executed.

There is a way to write twisted code in a more inline manner. An example is ::

  .. include:: <twistedecho3.py>

But it's isn't that intuitive which requires a funciton with a special decorator and
using the yield statement to give back control to twisted's main event loop.

So what of gevent. Gevent takes a different approach again. It uses Coroutines to create
Greenlets which act very much like threads however are really transparently handing control
back and forth between greenlets in a single thread.

Let's look at the GEvent example ::

  ..include:: <geventecho3.py>

First thing you'll notice is it's a lot longer. The reason for this is that GEvent only
includes low level functions and doesn't recreate standard library functions with it's own
versions like twisted does. So in this example I've had to create my own gevent_url_fetch.
If you ignore this for now, you'll notice the rest of the code looks very similar
to the threaded example. All the calls are written as if they block like in the threaded
example. You don't have to change your thinking from thinking about your code as
linearly executed independent threads. I'd content this is the easiest to understand and
write.

However, that's not the end. GEvent has a trick up it's sleave.

 ..include:: <geventecho4.py>

This is exactly the same code as the original threaded example with a single line added::

  from gevent.monkey import patch_all; patch_all()

This replaces all the low level python implementations of Threads, sockets etc for gevent
versions meaning you don't need to change your code at all. It automatically becomes
asyncrhonous. Neat trick.

