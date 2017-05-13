master_password
===============

`master_password` is a Python implementation of the Master Password ([Lyndir/MasterPassword](https://github.com/Lyndir/MasterPassword), [Site](http://masterpasswordapp.com/)) algorithm.

Usage
-----

Note: All strings are assumed to be encoded in UTF-8, but you can also provide a `bytes` or `bytearray` in a different encoding.

Generate a password for someone with the fullname _John Smith_ and the password _example password_ for the domain _example.org_

```python
import master_password

mpw = master_password.MPW('John Smith', 'example password')
print(mpw.password('example.org'))  # --> 'Dicd0!JoniLeza'
```

Create a `master_password.MPW` directly from a key without making a key from a username and password

```python
key = mpw.key  # Get the key from the old mpw to reuse
# Or you can calculate a key manually
key = master_password.MPW.calculate_key(
  password='example password',
  salt=master_password.MPW.calculate_salt(
    name='John Smith'
  )
)

new_mpw = master_password.MPW.from_key(key)
print(new_mpw == mpw)  # --> True
```

Generate using any template

```python
mpw.generate(
  site,  # Non-optional arg, e.g., 'example.org'. Site to generate for.
  counter=1,  # Increment counter for a new password.
              # Must be less than 2 ** 32.
  context=None,  # Like counter, changes password. Meant for security
                 # questions, as it is easier to remember.
  template='long',  # The name of the template
  namespace=None  # The namespace to use. Will not change the namespace
                  # used for the key. Defaults to `self.namespace.name`.
)

## Shortcuts
mpw.password(
  site,  # Non-optional arg
  counter=1,
  template='long'
)  # context=None, namespace=self.namespace.password

mpw.login(
  site,  # Non-optional arg
  counter=1,
)  # context=None, template='name', namespace=self.namespace.answer

mpw.answer(
  site,  # Non-optional arg
  counter=1,
  context=''
)  # template='phrase', namespace=self.namespace.answer

mpw.pin(
  site,  # Non-optional arg
  counter=1
)  # context=None, template='pin', namespace=self.namespace.password
```

Don't store the name

```python
print(mpw.name)  # --> 'John Smith'

# Either create a new MPW and recalculate the key
mpw = master_password.MPW('John Smith', 'example password', keep_name=False)
print(mpw.name)  # --> None

# Or use the existing key
mpw = master_password.MPW.from_key(mpw.key, name=None)
# You can specify an arbitrary name here.
```

Create a new name space (Note: The passwords generated depend on the name space. If you use the same name space, you will get the same results. By default, `com.lyndir.masterpassword` name spaces are used, to match with the original app)

```python
example_ns = master_password.MPWNameSpace.create(
  name='org.example',  # Namespace to use in the seed with the URL
  password='org.example',  # Namespace to use when creating a password
  login='org.example.login',  # Namespace to use when creating a login
  answer='org.example.answer'  # Namespace to use when creating an
                               # answer to a secret question
)
# This is equivalent to
example_ns = master_password.MPWNameSpace.create(
  name='org.example'
)  # '', '.login' and '.answer' are concatenated automatically when a
   # unique namespace is not provided.

# Different namespaces are needed to avoid the same password being generated for
# different fields.

print(example_ns is master_password.MPWNameSpace('org.example'))  # --> True
# You can access namespaces by their name.
```

Note that all the classes defined under the `master_password` module should not be modified after they are created.

Disclaimer
----------

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
