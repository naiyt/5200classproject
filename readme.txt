Project #3
CS 5890
Nate Collings (n.colligs@aggiemail.usu.edu) and Dale Flamm (tiki.man163@gmail.com)

How to run:

An example Python script using our RPC mechanism is located in "test_example.py". First, you also need the RPC server started with the command:

`python run_server.py`

Then, you can start the example test with:

`python test_example.py`

We've included two example functions that can be executed via rpc ('add', and 'subtract'). To register a new function, you need to first define its interface in rpc/interface.py. The IDL we have defined works as follows:

* Add a new entry to the 'self.methods' dictionary of the Interface class
* Your entry must follow this format:
  - 'function_name': { 'sig': ('type', 'type'), 'return': 'type' }

As Python is dynamically typed and does not have Java style interfaces, this is necessary to ensure that you are
getting the right types for transmission and return. Allowed types are:

* int (int's are also longs in Python)
* float
* bool (booleans)
* str (strings)

Then, you simply implement the function in the `method_implementations.py` file! The server will properly import
that code and run it according to your interface and the function required. Please follow the example of the
two functions already defined (they must use the `@staticmethod` decorator).
