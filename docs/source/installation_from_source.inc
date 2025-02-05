

The current version of the ``mmgroup`` package is a source distribution that has 
been tested on a 64-bit Windows platform only. It runs with python 3.6 or higher. 
There is also experimental support for Linux. The source distribution can be 
downloaded from

https://github.com/Martin-Seysen/mmgroup . 

The distribution contains a number of extensions written
in ``C`` which have to be built before use. 

Dependencies
------------

Before you can use this source distribution or build its extensions you 
should install the following python packages:

.. table:: External Python packages required
  :widths: 30 70


  ======================== =========================================================
  Package                  Purpose 
  ======================== =========================================================
  ``cython``               Development: integrating ``C`` programs into the 
                           ``mmgroup`` package
  ``numpy``                Runtime: Most arrays used by the ``mmgroup`` package 
                           are ``numpy`` arrays
  ``pytest``               Testing: basic package used for testing
  ``regex``                Development: parsing balanced curly braces
  ``scipy``                Testing: statistical tests
  ``setuptools``           Development: basic package used for setup and building
                           extensions
  ``sphinx``               Documentation: basic package used for documentation
  ``sphinx-rtd-theme``     Documentation: 'theme' to be used by sphinx 
  ``sphinxcontrib-bibtex`` Documentation: bibliography in BibTeX style
  ``breathe``              Documentation: link between ``doxygen`` and ``sphinx``
  ======================== =========================================================

Packages used for the purpose of documentation are required only if you want to 
rebuild the documentation. If you want to rebuild the documentation you should
also install the following programs:


.. table:: External programs required
  :widths: 20 30 50


  ========= ============== ===========================================================
  Program   Purpose        Location 
  ========= ============== ===========================================================
  miktex    Documentation  https://miktex.org/
  Perl      Documentation  https://www.perl.org/get.html
  doxygen   Documentation  https://www.doxygen.nl/download.html
            of C files
  ========= ============== ===========================================================



Installing the package
----------------------

To install the required package, go to the root directory of the distribution.
This is the directory containing the files ``setup.py`` and ``README.rst``.
From there run the following command::

    python setup.py install -f

For testing the installation, run the following command::

    python -m pytest ./src/mmgroup/ -v -s -m "not slow"


For building a wheel you may run:: 

    python setup.py bdist_wheel

Distributing a *wheel* is the standard way to distribute a python
package, see e.g. 

https://packaging.python.org/guides/distributing-packages-using-setuptools/#wheels

The current version supports building wheels for 64-bit Windows only.

There is experimental support for building a Linux version from a
source distribution.

Remarks
.......

If you have installed any version of the ``mmgroup`` package (e.g. with
the ``pip`` tool) then you **must** uninstall that package before you can 
build a new version of the ``mmgroup`` package from the source files.

We recommend to run

.. code-block::

   python cleanup.py -pcx

in the root directory of the distribution for cleaning up intermediate
files before building the package from the source files.


Installing a C compiler for cython in Windows 
---------------------------------------------

The bad news for Windows developers is that there is no pre-installed 
``C`` compiler on a standard Windows system. However, the ``cython`` 
package requires a ``C`` compiler. Here in principle, the user has the 
choice between the following two compilers:

   *  ``MSVC``   

   *  ``MinGW-w64``

The user has to install a ``C`` compiler so that it cooperates with 
``cython``. 
That installation process is out of the scope of this document.

For installing ``MSVC``, one might start looking at 
https://wiki.python.org/moin/WindowsCompilers

For installing ``MinGW``, one might start looking at
https://cython.readthedocs.io/en/latest/src/tutorial/appendix.html.

The current ``setup.py`` supports ``MSVC`` and ``MinGW`` for 64-bit 
Windows. According to the last URL the ``MinGW`` compiler works with 
Python versions up to 3.4 only, so that it can no longer be recommended. 

The author has installed the ``MSVC`` compiler with the Microsoft
*Build Tools for Visual Studio* from:

https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16 ,

following the instructions in

https://www.scivision.dev/python-windows-visual-c-14-required/  .

Before typing ``python setup.py bdist_wheel`` in a Windows command 
line the author had to type::


  "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

Here the path my be different on the user's Windows system.


Installing the *mmgroup* package on Linux
-----------------------------------------

We describe some experimental support for building a Linux version
of the mmgroup package.
For building a Linux version of this package you have to install 
a source distribution of the package. Then you should run::

   python setup.py bdist_wheel

Please ignore all errors related to the *auditwheel* tool. After
completing the build process you will find a wheel for linux in
subdirectory ``dist``.

You may install that wheel using ``pip install`` in the standard way.
Afterwords you have to make sure that the Linux dynamic loader can 
find the shared libraries ``libmmgroup_mat24.so`` and 
``libmmgroup_mm_basics.so`` in subdirectory ``usr/mmgroup`` of the
package. Therefore you may either copy these
libraries to the  default path  for shared libraries in your system
(usually ``/lib`` or ``/usr/lib``). Alternatively, you may change 
the environment variable ``LD_LIBRARY_PATH`` appropriately.

A more comfortable installation process should be compliant with the 
*manylinux* standard, see e.g.:

https://github.com/pypa/python-manylinux-demo  .

In a Linux distribution, it may be necessary to install **pip**,
**sphinx**, **texlive**, and **doxygen** as follows:

 .. code-block:: none

    sudo apt-get install python-pip
    sudo apt-get install python-sphinx
    sudo apt-get install texlive
    sudo apt-get install doxygen

Note that some distributions require the string 'python' to be 
replaced by 'python3'.


Remarks
.......

On some Linux systems the user may have to type ``python3`` instead of
``python`` and ``pip3`` instead of ``pip`` when working with python 3.x.

On some Linux-like systems (e.g. on MacOS with a Clang C compiler) it 
might help to remove the string ``-static-libgc`` from all lists in 
file ``config.py``.




