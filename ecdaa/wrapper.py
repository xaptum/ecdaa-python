__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64', '/usr/local/lib', '/usr/lib'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# No libraries

# No modules

class struct_ecdaa_member_public_key_BLS383(Structure):
    pass

class struct_ecdaa_issuer_secret_key_BLS383(Structure):
    pass

class struct_ecdaa_group_public_key_BLS383(Structure):
    pass

class struct_ecdaa_prng(Structure):
    pass


class struct_anon_29(Structure):
    pass

struct_anon_29.__slots__ = [
    'ira',
    'rndptr',
    'borrow',
    'pool_ptr',
    'pool',
]
struct_anon_29._fields_ = [
    ('ira', c_uint32 * 21),
    ('rndptr', c_int),
    ('borrow', c_uint32),
    ('pool_ptr', c_int),
    ('pool', c_char * 32),
]

csprng = struct_anon_29 

BIG_384_56 = c_int64 * (1 + (((8 * 48) - 1) / 56)) 


class struct_anon_31(Structure):
    pass

struct_anon_31.__slots__ = [
    'g',
    'XES',
]
struct_anon_31._fields_ = [
    ('g', BIG_384_56),
    ('XES', c_int32),
]

FP_BLS383 = struct_anon_31 


class struct_anon_32(Structure):
    pass

struct_anon_32.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_32._fields_ = [
    ('inf', c_int),
    ('x', FP_BLS383),
    ('y', FP_BLS383),
    ('z', FP_BLS383),
]

ECP_BLS383 = struct_anon_32 

class struct_ecdaa_credential_BLS383(Structure):
    pass

struct_ecdaa_credential_BLS383.__slots__ = [
    'A',
    'B',
    'C',
    'D',
]
struct_ecdaa_credential_BLS383._fields_ = [
    ('A', ECP_BLS383),
    ('B', ECP_BLS383),
    ('C', ECP_BLS383),
    ('D', ECP_BLS383),
]

class struct_ecdaa_credential_BLS383_signature(Structure):
    pass

struct_ecdaa_credential_BLS383_signature.__slots__ = [
    'c',
    's',
]
struct_ecdaa_credential_BLS383_signature._fields_ = [
    ('c', BIG_384_56),
    ('s', BIG_384_56),
]

class struct_ecdaa_member_public_key_BN254CX(Structure):
    pass

class struct_ecdaa_issuer_secret_key_BN254CX(Structure):
    pass

class struct_ecdaa_group_public_key_BN254CX(Structure):
    pass

BIG_256_56 = c_int64 * (1 + (((8 * 32) - 1) / 56)) 


class struct_anon_33(Structure):
    pass

struct_anon_33.__slots__ = [
    'g',
    'XES',
]
struct_anon_33._fields_ = [
    ('g', BIG_256_56),
    ('XES', c_int32),
]

FP_BN254CX = struct_anon_33 


class struct_anon_34(Structure):
    pass

struct_anon_34.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_34._fields_ = [
    ('inf', c_int),
    ('x', FP_BN254CX),
    ('y', FP_BN254CX),
    ('z', FP_BN254CX),
]

ECP_BN254CX = struct_anon_34 

class struct_ecdaa_credential_BN254CX(Structure):
    pass

struct_ecdaa_credential_BN254CX.__slots__ = [
    'A',
    'B',
    'C',
    'D',
]
struct_ecdaa_credential_BN254CX._fields_ = [
    ('A', ECP_BN254CX),
    ('B', ECP_BN254CX),
    ('C', ECP_BN254CX),
    ('D', ECP_BN254CX),
]

class struct_ecdaa_credential_BN254CX_signature(Structure):
    pass

struct_ecdaa_credential_BN254CX_signature.__slots__ = [
    'c',
    's',
]
struct_ecdaa_credential_BN254CX_signature._fields_ = [
    ('c', BIG_256_56),
    ('s', BIG_256_56),
]

class struct_ecdaa_member_public_key_BN254(Structure):
    pass

class struct_ecdaa_issuer_secret_key_BN254(Structure):
    pass

class struct_ecdaa_group_public_key_BN254(Structure):
    pass


class struct_anon_35(Structure):
    pass

struct_anon_35.__slots__ = [
    'g',
    'XES',
]
struct_anon_35._fields_ = [
    ('g', BIG_256_56),
    ('XES', c_int32),
]

FP_BN254 = struct_anon_35 


class struct_anon_36(Structure):
    pass

struct_anon_36.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_36._fields_ = [
    ('inf', c_int),
    ('x', FP_BN254),
    ('y', FP_BN254),
    ('z', FP_BN254),
]

ECP_BN254 = struct_anon_36 

class struct_ecdaa_credential_BN254(Structure):
    pass

struct_ecdaa_credential_BN254.__slots__ = [
    'A',
    'B',
    'C',
    'D',
]
struct_ecdaa_credential_BN254._fields_ = [
    ('A', ECP_BN254),
    ('B', ECP_BN254),
    ('C', ECP_BN254),
    ('D', ECP_BN254),
]

class struct_ecdaa_credential_BN254_signature(Structure):
    pass

struct_ecdaa_credential_BN254_signature.__slots__ = [
    'c',
    's',
]
struct_ecdaa_credential_BN254_signature._fields_ = [
    ('c', BIG_256_56),
    ('s', BIG_256_56),
]

class struct_ecdaa_member_public_key_FP256BN(Structure):
    pass

class struct_ecdaa_issuer_secret_key_FP256BN(Structure):
    pass

class struct_ecdaa_group_public_key_FP256BN(Structure):
    pass


class struct_anon_37(Structure):
    pass

struct_anon_37.__slots__ = [
    'g',
    'XES',
]
struct_anon_37._fields_ = [
    ('g', BIG_256_56),
    ('XES', c_int32),
]

FP_FP256BN = struct_anon_37 


class struct_anon_38(Structure):
    pass

struct_anon_38.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_38._fields_ = [
    ('inf', c_int),
    ('x', FP_FP256BN),
    ('y', FP_FP256BN),
    ('z', FP_FP256BN),
]

ECP_FP256BN = struct_anon_38 

class struct_ecdaa_credential_FP256BN(Structure):
    pass

struct_ecdaa_credential_FP256BN.__slots__ = [
    'A',
    'B',
    'C',
    'D',
]
struct_ecdaa_credential_FP256BN._fields_ = [
    ('A', ECP_FP256BN),
    ('B', ECP_FP256BN),
    ('C', ECP_FP256BN),
    ('D', ECP_FP256BN),
]

class struct_ecdaa_credential_FP256BN_signature(Structure):
    pass

struct_ecdaa_credential_FP256BN_signature.__slots__ = [
    'c',
    's',
]
struct_ecdaa_credential_FP256BN_signature._fields_ = [
    ('c', BIG_256_56),
    ('s', BIG_256_56),
]

class struct_anon_39(Structure):
    pass

struct_anon_39.__slots__ = [
    'a',
    'b',
]
struct_anon_39._fields_ = [
    ('a', FP_BLS383),
    ('b', FP_BLS383),
]

FP2_BLS383 = struct_anon_39 


class struct_anon_40(Structure):
    pass

struct_anon_40.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_40._fields_ = [
    ('inf', c_int),
    ('x', FP2_BLS383),
    ('y', FP2_BLS383),
    ('z', FP2_BLS383),
]

ECP2_BLS383 = struct_anon_40 

struct_ecdaa_group_public_key_BLS383.__slots__ = [
    'X',
    'Y',
]
struct_ecdaa_group_public_key_BLS383._fields_ = [
    ('X', ECP2_BLS383),
    ('Y', ECP2_BLS383),
]

class struct_anon_41(Structure):
    pass

struct_anon_41.__slots__ = [
    'a',
    'b',
]
struct_anon_41._fields_ = [
    ('a', FP_BN254CX),
    ('b', FP_BN254CX),
]

FP2_BN254CX = struct_anon_41 


class struct_anon_42(Structure):
    pass

struct_anon_42.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_42._fields_ = [
    ('inf', c_int),
    ('x', FP2_BN254CX),
    ('y', FP2_BN254CX),
    ('z', FP2_BN254CX),
]

ECP2_BN254CX = struct_anon_42 

struct_ecdaa_group_public_key_BN254CX.__slots__ = [
    'X',
    'Y',
]
struct_ecdaa_group_public_key_BN254CX._fields_ = [
    ('X', ECP2_BN254CX),
    ('Y', ECP2_BN254CX),
]

class struct_anon_43(Structure):
    pass

struct_anon_43.__slots__ = [
    'a',
    'b',
]
struct_anon_43._fields_ = [
    ('a', FP_BN254),
    ('b', FP_BN254),
]

FP2_BN254 = struct_anon_43 


class struct_anon_44(Structure):
    pass

struct_anon_44.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_44._fields_ = [
    ('inf', c_int),
    ('x', FP2_BN254),
    ('y', FP2_BN254),
    ('z', FP2_BN254),
]

ECP2_BN254 = struct_anon_44 

struct_ecdaa_group_public_key_BN254.__slots__ = [
    'X',
    'Y',
]
struct_ecdaa_group_public_key_BN254._fields_ = [
    ('X', ECP2_BN254),
    ('Y', ECP2_BN254),
]

class struct_anon_45(Structure):
    pass

struct_anon_45.__slots__ = [
    'a',
    'b',
]
struct_anon_45._fields_ = [
    ('a', FP_FP256BN),
    ('b', FP_FP256BN),
]

FP2_FP256BN = struct_anon_45 


class struct_anon_46(Structure):
    pass

struct_anon_46.__slots__ = [
    'inf',
    'x',
    'y',
    'z',
]
struct_anon_46._fields_ = [
    ('inf', c_int),
    ('x', FP2_FP256BN),
    ('y', FP2_FP256BN),
    ('z', FP2_FP256BN),
]

ECP2_FP256BN = struct_anon_46 

struct_ecdaa_group_public_key_FP256BN.__slots__ = [
    'X',
    'Y',
]
struct_ecdaa_group_public_key_FP256BN._fields_ = [
    ('X', ECP2_FP256BN),
    ('Y', ECP2_FP256BN),
]

class struct_ecdaa_issuer_public_key_BLS383(Structure):
    pass

struct_ecdaa_issuer_public_key_BLS383.__slots__ = [
    'gpk',
    'c',
    'sx',
    'sy',
]
struct_ecdaa_issuer_public_key_BLS383._fields_ = [
    ('gpk', struct_ecdaa_group_public_key_BLS383),
    ('c', BIG_384_56),
    ('sx', BIG_384_56),
    ('sy', BIG_384_56),
]

struct_ecdaa_issuer_secret_key_BLS383.__slots__ = [
    'x',
    'y',
]
struct_ecdaa_issuer_secret_key_BLS383._fields_ = [
    ('x', BIG_384_56),
    ('y', BIG_384_56),
]

class struct_ecdaa_issuer_public_key_BN254CX(Structure):
    pass

struct_ecdaa_issuer_public_key_BN254CX.__slots__ = [
    'gpk',
    'c',
    'sx',
    'sy',
]
struct_ecdaa_issuer_public_key_BN254CX._fields_ = [
    ('gpk', struct_ecdaa_group_public_key_BN254CX),
    ('c', BIG_256_56),
    ('sx', BIG_256_56),
    ('sy', BIG_256_56),
]

struct_ecdaa_issuer_secret_key_BN254CX.__slots__ = [
    'x',
    'y',
]
struct_ecdaa_issuer_secret_key_BN254CX._fields_ = [
    ('x', BIG_256_56),
    ('y', BIG_256_56),
]

class struct_ecdaa_issuer_public_key_BN254(Structure):
    pass

struct_ecdaa_issuer_public_key_BN254.__slots__ = [
    'gpk',
    'c',
    'sx',
    'sy',
]
struct_ecdaa_issuer_public_key_BN254._fields_ = [
    ('gpk', struct_ecdaa_group_public_key_BN254),
    ('c', BIG_256_56),
    ('sx', BIG_256_56),
    ('sy', BIG_256_56),
]

struct_ecdaa_issuer_secret_key_BN254.__slots__ = [
    'x',
    'y',
]
struct_ecdaa_issuer_secret_key_BN254._fields_ = [
    ('x', BIG_256_56),
    ('y', BIG_256_56),
]

class struct_ecdaa_issuer_public_key_FP256BN(Structure):
    pass

struct_ecdaa_issuer_public_key_FP256BN.__slots__ = [
    'gpk',
    'c',
    'sx',
    'sy',
]
struct_ecdaa_issuer_public_key_FP256BN._fields_ = [
    ('gpk', struct_ecdaa_group_public_key_FP256BN),
    ('c', BIG_256_56),
    ('sx', BIG_256_56),
    ('sy', BIG_256_56),
]

struct_ecdaa_issuer_secret_key_FP256BN.__slots__ = [
    'x',
    'y',
]
struct_ecdaa_issuer_secret_key_FP256BN._fields_ = [
    ('x', BIG_256_56),
    ('y', BIG_256_56),
]

struct_ecdaa_member_public_key_BLS383.__slots__ = [
    'Q',
    'c',
    's',
]
struct_ecdaa_member_public_key_BLS383._fields_ = [
    ('Q', ECP_BLS383),
    ('c', BIG_384_56),
    ('s', BIG_384_56),
]

class struct_ecdaa_member_secret_key_BLS383(Structure):
    pass

struct_ecdaa_member_secret_key_BLS383.__slots__ = [
    'sk',
]
struct_ecdaa_member_secret_key_BLS383._fields_ = [
    ('sk', BIG_384_56),
]

struct_ecdaa_member_public_key_BN254CX.__slots__ = [
    'Q',
    'c',
    's',
]
struct_ecdaa_member_public_key_BN254CX._fields_ = [
    ('Q', ECP_BN254CX),
    ('c', BIG_256_56),
    ('s', BIG_256_56),
]

class struct_ecdaa_member_secret_key_BN254CX(Structure):
    pass

struct_ecdaa_member_secret_key_BN254CX.__slots__ = [
    'sk',
]
struct_ecdaa_member_secret_key_BN254CX._fields_ = [
    ('sk', BIG_256_56),
]

struct_ecdaa_member_public_key_BN254.__slots__ = [
    'Q',
    'c',
    's',
]
struct_ecdaa_member_public_key_BN254._fields_ = [
    ('Q', ECP_BN254),
    ('c', BIG_256_56),
    ('s', BIG_256_56),
]

class struct_ecdaa_member_secret_key_BN254(Structure):
    pass

struct_ecdaa_member_secret_key_BN254.__slots__ = [
    'sk',
]
struct_ecdaa_member_secret_key_BN254._fields_ = [
    ('sk', BIG_256_56),
]

struct_ecdaa_member_public_key_FP256BN.__slots__ = [
    'Q',
    'c',
    's',
]
struct_ecdaa_member_public_key_FP256BN._fields_ = [
    ('Q', ECP_FP256BN),
    ('c', BIG_256_56),
    ('s', BIG_256_56),
]

class struct_ecdaa_member_secret_key_FP256BN(Structure):
    pass

struct_ecdaa_member_secret_key_FP256BN.__slots__ = [
    'sk',
]
struct_ecdaa_member_secret_key_FP256BN._fields_ = [
    ('sk', BIG_256_56),
]

TPM_HANDLE = c_uint32 # /usr/local/include/tss2/tss2_tpm2_types.h: 48

TPMI_SH_AUTH_SESSION = TPM_HANDLE # /usr/local/include/tss2/tss2_tpm2_types.h: 62

# /usr/local/include/tss2/tss2_tpm2_types.h: 120
class union_anon_50(Union):
    pass

union_anon_50.__slots__ = [
    'sha256',
    'sha512',
    'null',
]
union_anon_50._fields_ = [
    ('sha256', c_uint8 * 32),
    ('sha512', c_uint8 * 64),
    ('null', c_uint8),
]

TPMU_HA = union_anon_50 # /usr/local/include/tss2/tss2_tpm2_types.h: 120

# /usr/local/include/tss2/tss2_tpm2_types.h: 130
class struct_anon_52(Structure):
    pass

struct_anon_52.__slots__ = [
    'size',
    'buffer',
]
struct_anon_52._fields_ = [
    ('size', c_uint16),
    ('buffer', c_uint8 * sizeof(TPMU_HA)),
]

TPM2B_DIGEST = struct_anon_52 # /usr/local/include/tss2/tss2_tpm2_types.h: 130

TPM2B_NONCE = TPM2B_DIGEST # /usr/local/include/tss2/tss2_tpm2_types.h: 132

TPM2B_AUTH = TPM2B_DIGEST # /usr/local/include/tss2/tss2_tpm2_types.h: 134

# /usr/local/include/tss2/tss2_tpm2_types.h: 144
class struct_anon_53(Structure):
    pass

struct_anon_53.__slots__ = [
    'continueSession',
    'auditExclusive',
    'auditReset',
    'Reserved',
    'decrypt',
    'encrypt',
    'audit',
]
struct_anon_53._fields_ = [
    ('continueSession', c_uint, 1),
    ('auditExclusive', c_uint, 1),
    ('auditReset', c_uint, 1),
    ('Reserved', c_uint, 2),
    ('decrypt', c_uint, 1),
    ('encrypt', c_uint, 1),
    ('audit', c_uint, 1),
]

TPMA_SESSION = struct_anon_53 # /usr/local/include/tss2/tss2_tpm2_types.h: 144

# /usr/local/include/tss2/tss2_tpm2_types.h: 170
class struct_anon_55(Structure):
    pass

struct_anon_55.__slots__ = [
    'sessionHandle',
    'nonce',
    'sessionAttributes',
    'hmac',
]
struct_anon_55._fields_ = [
    ('sessionHandle', TPMI_SH_AUTH_SESSION),
    ('nonce', TPM2B_NONCE),
    ('sessionAttributes', TPMA_SESSION),
    ('hmac', TPM2B_AUTH),
]

TPMS_AUTH_COMMAND = struct_anon_55 # /usr/local/include/tss2/tss2_tpm2_types.h: 170

# /usr/local/include/tss2/tss2_tpm2_types.h: 176
class struct_anon_56(Structure):
    pass

struct_anon_56.__slots__ = [
    'nonce',
    'sessionAttributes',
    'hmac',
]
struct_anon_56._fields_ = [
    ('nonce', TPM2B_NONCE),
    ('sessionAttributes', TPMA_SESSION),
    ('hmac', TPM2B_AUTH),
]

TPMS_AUTH_RESPONSE = struct_anon_56 # /usr/local/include/tss2/tss2_tpm2_types.h: 176

TSS2_RC = c_uint32 # /usr/local/include/tss2/tss2_common.h: 40

# /usr/local/include/tss2/tss2_sys.h: 34
class struct__TSS2_SYS_OPAQUE_CONTEXT_BLOB(Structure):
    pass

TSS2_SYS_CONTEXT = struct__TSS2_SYS_OPAQUE_CONTEXT_BLOB # /usr/local/include/tss2/tss2_sys.h: 34

# /usr/local/include/tss2/tss2_sys.h: 39
class struct_anon_95(Structure):
    pass

struct_anon_95.__slots__ = [
    'cmdAuthsCount',
    'cmdAuths',
]
struct_anon_95._fields_ = [
    ('cmdAuthsCount', c_uint8),
    ('cmdAuths', POINTER(POINTER(TPMS_AUTH_COMMAND))),
]

TSS2_SYS_CMD_AUTHS = struct_anon_95 # /usr/local/include/tss2/tss2_sys.h: 39

# /usr/local/include/tss2/tss2_sys.h: 44
class struct_anon_96(Structure):
    pass

struct_anon_96.__slots__ = [
    'rspAuthsCount',
    'rspAuths',
]
struct_anon_96._fields_ = [
    ('rspAuthsCount', c_uint8),
    ('rspAuths', POINTER(POINTER(TPMS_AUTH_RESPONSE))),
]

TSS2_SYS_RSP_AUTHS = struct_anon_96 # /usr/local/include/tss2/tss2_sys.h: 44


class struct_ecdaa_tpm_context(Structure):
    pass

struct_ecdaa_tpm_context.__slots__ = [
    'context_buffer',
    'sapi_context',
    'public_key',
    'commit_counter',
    'key_handle',
    'key_authentication',
    'key_authentication_array',
    'key_authentication_cmd',
    'last_auth_response',
    'last_auth_response_array',
    'last_auth_response_cmd',
    'last_return_code',
]
struct_ecdaa_tpm_context._fields_ = [
    ('context_buffer', c_uint8 * 5120),
    ('sapi_context', POINTER(TSS2_SYS_CONTEXT)),
    ('public_key', ECP_FP256BN),
    ('commit_counter', c_uint16),
    ('key_handle', TPM_HANDLE),
    ('key_authentication', TPMS_AUTH_COMMAND),
    ('key_authentication_array', POINTER(TPMS_AUTH_COMMAND) * 1),
    ('key_authentication_cmd', TSS2_SYS_CMD_AUTHS),
    ('last_auth_response', TPMS_AUTH_RESPONSE),
    ('last_auth_response_array', POINTER(TPMS_AUTH_RESPONSE) * 1),
    ('last_auth_response_cmd', TSS2_SYS_RSP_AUTHS),
    ('last_return_code', TSS2_RC),
]


enum_ecdaa_prng_initialized = c_int 

ECDAA_PRNG_INITIALIZED_NO = 0 

ECDAA_PRNG_INITIALIZED_YES = (ECDAA_PRNG_INITIALIZED_NO + 1) 

struct_ecdaa_prng.__slots__ = [
    'initialized',
    'impl',
]
struct_ecdaa_prng._fields_ = [
    ('initialized', enum_ecdaa_prng_initialized),
    ('impl', csprng),
]

class struct_ecdaa_revocations_BLS383(Structure):
    pass

struct_ecdaa_revocations_BLS383.__slots__ = [
    'sk_length',
    'sk_list',
    'bsn_length',
    'bsn_list',
]
struct_ecdaa_revocations_BLS383._fields_ = [
    ('sk_length', c_size_t),
    ('sk_list', POINTER(struct_ecdaa_member_secret_key_BLS383)),
    ('bsn_length', c_size_t),
    ('bsn_list', POINTER(ECP_BLS383)),
]

class struct_ecdaa_revocations_BN254CX(Structure):
    pass

struct_ecdaa_revocations_BN254CX.__slots__ = [
    'sk_length',
    'sk_list',
    'bsn_length',
    'bsn_list',
]
struct_ecdaa_revocations_BN254CX._fields_ = [
    ('sk_length', c_size_t),
    ('sk_list', POINTER(struct_ecdaa_member_secret_key_BN254CX)),
    ('bsn_length', c_size_t),
    ('bsn_list', POINTER(ECP_BN254CX)),
]

class struct_ecdaa_revocations_BN254(Structure):
    pass

struct_ecdaa_revocations_BN254.__slots__ = [
    'sk_length',
    'sk_list',
    'bsn_length',
    'bsn_list',
]
struct_ecdaa_revocations_BN254._fields_ = [
    ('sk_length', c_size_t),
    ('sk_list', POINTER(struct_ecdaa_member_secret_key_BN254)),
    ('bsn_length', c_size_t),
    ('bsn_list', POINTER(ECP_BN254)),
]

class struct_ecdaa_revocations_FP256BN(Structure):
    pass

struct_ecdaa_revocations_FP256BN.__slots__ = [
    'sk_length',
    'sk_list',
    'bsn_length',
    'bsn_list',
]
struct_ecdaa_revocations_FP256BN._fields_ = [
    ('sk_length', c_size_t),
    ('sk_list', POINTER(struct_ecdaa_member_secret_key_FP256BN)),
    ('bsn_length', c_size_t),
    ('bsn_list', POINTER(ECP_FP256BN)),
]

class struct_ecdaa_signature_BLS383(Structure):
    pass

struct_ecdaa_signature_BLS383.__slots__ = [
    'c',
    's',
    'R',
    'S',
    'T',
    'W',
    'K',
]
struct_ecdaa_signature_BLS383._fields_ = [
    ('c', BIG_384_56),
    ('s', BIG_384_56),
    ('R', ECP_BLS383),
    ('S', ECP_BLS383),
    ('T', ECP_BLS383),
    ('W', ECP_BLS383),
    ('K', ECP_BLS383),
]

class struct_ecdaa_signature_BN254CX(Structure):
    pass

struct_ecdaa_signature_BN254CX.__slots__ = [
    'c',
    's',
    'R',
    'S',
    'T',
    'W',
    'K',
]
struct_ecdaa_signature_BN254CX._fields_ = [
    ('c', BIG_256_56),
    ('s', BIG_256_56),
    ('R', ECP_BN254CX),
    ('S', ECP_BN254CX),
    ('T', ECP_BN254CX),
    ('W', ECP_BN254CX),
    ('K', ECP_BN254CX),
]

class struct_ecdaa_signature_BN254(Structure):
    pass

struct_ecdaa_signature_BN254.__slots__ = [
    'c',
    's',
    'R',
    'S',
    'T',
    'W',
    'K',
]
struct_ecdaa_signature_BN254._fields_ = [
    ('c', BIG_256_56),
    ('s', BIG_256_56),
    ('R', ECP_BN254),
    ('S', ECP_BN254),
    ('T', ECP_BN254),
    ('W', ECP_BN254),
    ('K', ECP_BN254),
]

class struct_ecdaa_signature_FP256BN(Structure):
    pass

struct_ecdaa_signature_FP256BN.__slots__ = [
    'c',
    's',
    'R',
    'S',
    'T',
    'W',
    'K',
]
struct_ecdaa_signature_FP256BN._fields_ = [
    ('c', BIG_256_56),
    ('s', BIG_256_56),
    ('R', ECP_FP256BN),
    ('S', ECP_FP256BN),
    ('T', ECP_FP256BN),
    ('W', ECP_FP256BN),
    ('K', ECP_FP256BN),
]

try:
    MODBYTES_384_56 = 48
except:
    pass

try:
    ECDAA_CREDENTIAL_BLS383_LENGTH = (4 * ((2 * MODBYTES_384_56) + 1))
except:
    pass

try:
    ECDAA_CREDENTIAL_BLS383_SIGNATURE_LENGTH = (2 * MODBYTES_384_56)
except:
    pass


try:
    MODBYTES_256_56 = 32
except:
    pass

try:
    ECDAA_CREDENTIAL_BN254CX_LENGTH = (4 * ((2 * MODBYTES_256_56) + 1))
except:
    pass

try:
    ECDAA_CREDENTIAL_BN254CX_SIGNATURE_LENGTH = (2 * MODBYTES_256_56)
except:
    pass

try:
    ECDAA_CREDENTIAL_BN254_LENGTH = (4 * ((2 * MODBYTES_256_56) + 1))
except:
    pass

try:
    ECDAA_CREDENTIAL_BN254_SIGNATURE_LENGTH = (2 * MODBYTES_256_56)
except:
    pass

try:
    ECDAA_CREDENTIAL_FP256BN_LENGTH = (4 * ((2 * MODBYTES_256_56) + 1))
except:
    pass

try:
    ECDAA_CREDENTIAL_FP256BN_SIGNATURE_LENGTH = (2 * MODBYTES_256_56)
except:
    pass

try:
    ECDAA_GROUP_PUBLIC_KEY_BLS383_LENGTH = (2 * ((4 * MODBYTES_384_56) + 1))
except:
    pass

try:
    ECDAA_GROUP_PUBLIC_KEY_BN254CX_LENGTH = (2 * ((4 * MODBYTES_256_56) + 1))
except:
    pass

try:
    ECDAA_GROUP_PUBLIC_KEY_BN254_LENGTH = (2 * ((4 * MODBYTES_256_56) + 1))
except:
    pass

try:
    ECDAA_GROUP_PUBLIC_KEY_FP256BN_LENGTH = (2 * ((4 * MODBYTES_256_56) + 1))
except:
    pass

try:
    ECDAA_ISSUER_PUBLIC_KEY_BLS383_LENGTH = (((ECDAA_GROUP_PUBLIC_KEY_BLS383_LENGTH + MODBYTES_384_56) + MODBYTES_384_56) + MODBYTES_384_56)
except:
    pass

try:
    ECDAA_ISSUER_SECRET_KEY_BLS383_LENGTH = (2 * MODBYTES_384_56)
except:
    pass

try:
    ECDAA_ISSUER_PUBLIC_KEY_BN254CX_LENGTH = (((ECDAA_GROUP_PUBLIC_KEY_BN254CX_LENGTH + MODBYTES_256_56) + MODBYTES_256_56) + MODBYTES_256_56)
except:
    pass

try:
    ECDAA_ISSUER_SECRET_KEY_BN254CX_LENGTH = (2 * MODBYTES_256_56)
except:
    pass

try:
    ECDAA_ISSUER_PUBLIC_KEY_BN254_LENGTH = (((ECDAA_GROUP_PUBLIC_KEY_BN254_LENGTH + MODBYTES_256_56) + MODBYTES_256_56) + MODBYTES_256_56)
except:
    pass

try:
    ECDAA_ISSUER_SECRET_KEY_BN254_LENGTH = (2 * MODBYTES_256_56)
except:
    pass

try:
    ECDAA_ISSUER_PUBLIC_KEY_FP256BN_LENGTH = (((ECDAA_GROUP_PUBLIC_KEY_FP256BN_LENGTH + MODBYTES_256_56) + MODBYTES_256_56) + MODBYTES_256_56)
except:
    pass

try:
    ECDAA_ISSUER_SECRET_KEY_FP256BN_LENGTH = (2 * MODBYTES_256_56)
except:
    pass

try:
    ECDAA_MEMBER_PUBLIC_KEY_BLS383_LENGTH = ((((2 * MODBYTES_384_56) + 1) + MODBYTES_384_56) + MODBYTES_384_56)
except:
    pass

try:
    ECDAA_MEMBER_SECRET_KEY_BLS383_LENGTH = MODBYTES_384_56
except:
    pass

try:
    ECDAA_MEMBER_PUBLIC_KEY_BN254CX_LENGTH = ((((2 * MODBYTES_256_56) + 1) + MODBYTES_256_56) + MODBYTES_256_56)
except:
    pass

try:
    ECDAA_MEMBER_SECRET_KEY_BN254CX_LENGTH = MODBYTES_256_56
except:
    pass

try:
    ECDAA_MEMBER_PUBLIC_KEY_BN254_LENGTH = ((((2 * MODBYTES_256_56) + 1) + MODBYTES_256_56) + MODBYTES_256_56)
except:
    pass

try:
    ECDAA_MEMBER_SECRET_KEY_BN254_LENGTH = MODBYTES_256_56
except:
    pass

try:
    ECDAA_MEMBER_PUBLIC_KEY_FP256BN_LENGTH = ((((2 * MODBYTES_256_56) + 1) + MODBYTES_256_56) + MODBYTES_256_56)
except:
    pass

try:
    ECDAA_MEMBER_SECRET_KEY_FP256BN_LENGTH = MODBYTES_256_56
except:
    pass


try:
    TPM_CONTEXT_BUFFER_SIZE = 5120
except:
    pass

try:
    AMCL_SEED_SIZE = 128
except:
    pass

try:
    ECDAA_SIGNATURE_BLS383_LENGTH = ((2 * MODBYTES_384_56) + (4 * ((2 * MODBYTES_384_56) + 1)))
except:
    pass

try:
    ECDAA_SIGNATURE_BLS383_WITH_NYM_LENGTH = ((2 * MODBYTES_384_56) + (5 * ((2 * MODBYTES_384_56) + 1)))
except:
    pass

try:
    ECDAA_SIGNATURE_BN254CX_LENGTH = ((2 * MODBYTES_256_56) + (4 * ((2 * MODBYTES_256_56) + 1)))
except:
    pass

try:
    ECDAA_SIGNATURE_BN254CX_WITH_NYM_LENGTH = ((2 * MODBYTES_256_56) + (5 * ((2 * MODBYTES_256_56) + 1)))
except:
    pass

try:
    ECDAA_SIGNATURE_BN254_LENGTH = ((2 * MODBYTES_256_56) + (4 * ((2 * MODBYTES_256_56) + 1)))
except:
    pass

try:
    ECDAA_SIGNATURE_BN254_WITH_NYM_LENGTH = ((2 * MODBYTES_256_56) + (5 * ((2 * MODBYTES_256_56) + 1)))
except:
    pass

try:
    ECDAA_SIGNATURE_FP256BN_LENGTH = ((2 * MODBYTES_256_56) + (4 * ((2 * MODBYTES_256_56) + 1)))
except:
    pass

try:
    ECDAA_SIGNATURE_FP256BN_WITH_NYM_LENGTH = ((2 * MODBYTES_256_56) + (5 * ((2 * MODBYTES_256_56) + 1)))
except:
    pass

ecdaa_member_public_key_BLS383 = struct_ecdaa_member_public_key_BLS383 

ecdaa_issuer_secret_key_BLS383 = struct_ecdaa_issuer_secret_key_BLS383 

ecdaa_group_public_key_BLS383 = struct_ecdaa_group_public_key_BLS383 

ecdaa_prng = struct_ecdaa_prng 

ecdaa_credential_BLS383 = struct_ecdaa_credential_BLS383 

ecdaa_credential_BLS383_signature = struct_ecdaa_credential_BLS383_signature 

ecdaa_member_public_key_BN254CX = struct_ecdaa_member_public_key_BN254CX 

ecdaa_issuer_secret_key_BN254CX = struct_ecdaa_issuer_secret_key_BN254CX 

ecdaa_group_public_key_BN254CX = struct_ecdaa_group_public_key_BN254CX 

ecdaa_credential_BN254CX = struct_ecdaa_credential_BN254CX 

ecdaa_credential_BN254CX_signature = struct_ecdaa_credential_BN254CX_signature 

ecdaa_member_public_key_BN254 = struct_ecdaa_member_public_key_BN254 

ecdaa_issuer_secret_key_BN254 = struct_ecdaa_issuer_secret_key_BN254 

ecdaa_group_public_key_BN254 = struct_ecdaa_group_public_key_BN254 

ecdaa_credential_BN254 = struct_ecdaa_credential_BN254 

ecdaa_credential_BN254_signature = struct_ecdaa_credential_BN254_signature 

ecdaa_member_public_key_FP256BN = struct_ecdaa_member_public_key_FP256BN 

ecdaa_issuer_secret_key_FP256BN = struct_ecdaa_issuer_secret_key_FP256BN 

ecdaa_group_public_key_FP256BN = struct_ecdaa_group_public_key_FP256BN 

ecdaa_credential_FP256BN = struct_ecdaa_credential_FP256BN 

ecdaa_credential_FP256BN_signature = struct_ecdaa_credential_FP256BN_signature 

ecdaa_issuer_public_key_BLS383 = struct_ecdaa_issuer_public_key_BLS383 

ecdaa_issuer_public_key_BN254CX = struct_ecdaa_issuer_public_key_BN254CX 

ecdaa_issuer_public_key_BN254 = struct_ecdaa_issuer_public_key_BN254 

ecdaa_issuer_public_key_FP256BN = struct_ecdaa_issuer_public_key_FP256BN 

ecdaa_member_secret_key_BLS383 = struct_ecdaa_member_secret_key_BLS383 

ecdaa_member_secret_key_BN254CX = struct_ecdaa_member_secret_key_BN254CX 

ecdaa_member_secret_key_BN254 = struct_ecdaa_member_secret_key_BN254 

ecdaa_member_secret_key_FP256BN = struct_ecdaa_member_secret_key_FP256BN 

ecdaa_tpm_context = struct_ecdaa_tpm_context 

ecdaa_revocations_BLS383 = struct_ecdaa_revocations_BLS383 

ecdaa_revocations_BN254CX = struct_ecdaa_revocations_BN254CX 

ecdaa_revocations_BN254 = struct_ecdaa_revocations_BN254 

ecdaa_revocations_FP256BN = struct_ecdaa_revocations_FP256BN 

ecdaa_signature_BLS383 = struct_ecdaa_signature_BLS383 

ecdaa_signature_BN254CX = struct_ecdaa_signature_BN254CX 

ecdaa_signature_BN254 = struct_ecdaa_signature_BN254 

ecdaa_signature_FP256BN = struct_ecdaa_signature_FP256BN 

def set_functions_from_library(extra_lib_paths):
    add_library_search_dirs(extra_lib_paths)
    lib = load_library("ecdaa")

    global ecdaa_credential_BLS383_length
    ecdaa_credential_BLS383_length = lib.ecdaa_credential_BLS383_length
    ecdaa_credential_BLS383_length.argtypes = []
    ecdaa_credential_BLS383_length.restype = c_size_t

    global ecdaa_credential_BLS383_signature_length
    ecdaa_credential_BLS383_signature_length = lib.ecdaa_credential_BLS383_signature_length
    ecdaa_credential_BLS383_signature_length.argtypes = []
    ecdaa_credential_BLS383_signature_length.restype = c_size_t

    global ecdaa_credential_BLS383_generate
    ecdaa_credential_BLS383_generate = lib.ecdaa_credential_BLS383_generate
    ecdaa_credential_BLS383_generate.argtypes = [POINTER(struct_ecdaa_credential_BLS383), POINTER(struct_ecdaa_credential_BLS383_signature), POINTER(struct_ecdaa_issuer_secret_key_BLS383), POINTER(struct_ecdaa_member_public_key_BLS383), POINTER(struct_ecdaa_prng)]
    ecdaa_credential_BLS383_generate.restype = c_int

    global ecdaa_credential_BLS383_validate
    ecdaa_credential_BLS383_validate = lib.ecdaa_credential_BLS383_validate
    ecdaa_credential_BLS383_validate.argtypes = [POINTER(struct_ecdaa_credential_BLS383), POINTER(struct_ecdaa_credential_BLS383_signature), POINTER(struct_ecdaa_member_public_key_BLS383), POINTER(struct_ecdaa_group_public_key_BLS383)]
    ecdaa_credential_BLS383_validate.restype = c_int

    global ecdaa_credential_BLS383_serialize
    ecdaa_credential_BLS383_serialize = lib.ecdaa_credential_BLS383_serialize
    ecdaa_credential_BLS383_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_BLS383)]
    ecdaa_credential_BLS383_serialize.restype = None

    global ecdaa_credential_BLS383_signature_serialize
    ecdaa_credential_BLS383_signature_serialize = lib.ecdaa_credential_BLS383_signature_serialize
    ecdaa_credential_BLS383_signature_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_BLS383_signature)]
    ecdaa_credential_BLS383_signature_serialize.restype = None

    global ecdaa_credential_BLS383_deserialize_with_signature
    ecdaa_credential_BLS383_deserialize_with_signature = lib.ecdaa_credential_BLS383_deserialize_with_signature
    ecdaa_credential_BLS383_deserialize_with_signature.argtypes = [POINTER(struct_ecdaa_credential_BLS383), POINTER(struct_ecdaa_member_public_key_BLS383), POINTER(struct_ecdaa_group_public_key_BLS383), POINTER(c_uint8), POINTER(c_uint8)]
    ecdaa_credential_BLS383_deserialize_with_signature.restype = c_int

    global ecdaa_credential_BLS383_deserialize
    ecdaa_credential_BLS383_deserialize = lib.ecdaa_credential_BLS383_deserialize
    ecdaa_credential_BLS383_deserialize.argtypes = [POINTER(struct_ecdaa_credential_BLS383), POINTER(c_uint8)]
    ecdaa_credential_BLS383_deserialize.restype = c_int

    global ecdaa_credential_BN254CX_length
    ecdaa_credential_BN254CX_length = lib.ecdaa_credential_BN254CX_length
    ecdaa_credential_BN254CX_length.argtypes = []
    ecdaa_credential_BN254CX_length.restype = c_size_t

    global ecdaa_credential_BN254CX_signature_length
    ecdaa_credential_BN254CX_signature_length = lib.ecdaa_credential_BN254CX_signature_length
    ecdaa_credential_BN254CX_signature_length.argtypes = []
    ecdaa_credential_BN254CX_signature_length.restype = c_size_t

    global ecdaa_credential_BN254CX_generate
    ecdaa_credential_BN254CX_generate = lib.ecdaa_credential_BN254CX_generate
    ecdaa_credential_BN254CX_generate.argtypes = [POINTER(struct_ecdaa_credential_BN254CX), POINTER(struct_ecdaa_credential_BN254CX_signature), POINTER(struct_ecdaa_issuer_secret_key_BN254CX), POINTER(struct_ecdaa_member_public_key_BN254CX), POINTER(struct_ecdaa_prng)]
    ecdaa_credential_BN254CX_generate.restype = c_int

    global ecdaa_credential_BN254CX_validate
    ecdaa_credential_BN254CX_validate = lib.ecdaa_credential_BN254CX_validate
    ecdaa_credential_BN254CX_validate.argtypes = [POINTER(struct_ecdaa_credential_BN254CX), POINTER(struct_ecdaa_credential_BN254CX_signature), POINTER(struct_ecdaa_member_public_key_BN254CX), POINTER(struct_ecdaa_group_public_key_BN254CX)]
    ecdaa_credential_BN254CX_validate.restype = c_int

    global ecdaa_credential_BN254CX_serialize
    ecdaa_credential_BN254CX_serialize = lib.ecdaa_credential_BN254CX_serialize
    ecdaa_credential_BN254CX_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_BN254CX)]
    ecdaa_credential_BN254CX_serialize.restype = None

    global ecdaa_credential_BN254CX_signature_serialize
    ecdaa_credential_BN254CX_signature_serialize = lib.ecdaa_credential_BN254CX_signature_serialize
    ecdaa_credential_BN254CX_signature_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_BN254CX_signature)]
    ecdaa_credential_BN254CX_signature_serialize.restype = None

    global ecdaa_credential_BN254CX_deserialize_with_signature
    ecdaa_credential_BN254CX_deserialize_with_signature = lib.ecdaa_credential_BN254CX_deserialize_with_signature
    ecdaa_credential_BN254CX_deserialize_with_signature.argtypes = [POINTER(struct_ecdaa_credential_BN254CX), POINTER(struct_ecdaa_member_public_key_BN254CX), POINTER(struct_ecdaa_group_public_key_BN254CX), POINTER(c_uint8), POINTER(c_uint8)]
    ecdaa_credential_BN254CX_deserialize_with_signature.restype = c_int

    global ecdaa_credential_BN254CX_deserialize
    ecdaa_credential_BN254CX_deserialize = lib.ecdaa_credential_BN254CX_deserialize
    ecdaa_credential_BN254CX_deserialize.argtypes = [POINTER(struct_ecdaa_credential_BN254CX), POINTER(c_uint8)]
    ecdaa_credential_BN254CX_deserialize.restype = c_int

    global ecdaa_credential_BN254_length
    ecdaa_credential_BN254_length = lib.ecdaa_credential_BN254_length
    ecdaa_credential_BN254_length.argtypes = []
    ecdaa_credential_BN254_length.restype = c_size_t

    global ecdaa_credential_BN254_signature_length
    ecdaa_credential_BN254_signature_length = lib.ecdaa_credential_BN254_signature_length
    ecdaa_credential_BN254_signature_length.argtypes = []
    ecdaa_credential_BN254_signature_length.restype = c_size_t

    global ecdaa_credential_BN254_generate
    ecdaa_credential_BN254_generate = lib.ecdaa_credential_BN254_generate
    ecdaa_credential_BN254_generate.argtypes = [POINTER(struct_ecdaa_credential_BN254), POINTER(struct_ecdaa_credential_BN254_signature), POINTER(struct_ecdaa_issuer_secret_key_BN254), POINTER(struct_ecdaa_member_public_key_BN254), POINTER(struct_ecdaa_prng)]
    ecdaa_credential_BN254_generate.restype = c_int

    global ecdaa_credential_BN254_validate
    ecdaa_credential_BN254_validate = lib.ecdaa_credential_BN254_validate
    ecdaa_credential_BN254_validate.argtypes = [POINTER(struct_ecdaa_credential_BN254), POINTER(struct_ecdaa_credential_BN254_signature), POINTER(struct_ecdaa_member_public_key_BN254), POINTER(struct_ecdaa_group_public_key_BN254)]
    ecdaa_credential_BN254_validate.restype = c_int

    global ecdaa_credential_BN254_serialize
    ecdaa_credential_BN254_serialize = lib.ecdaa_credential_BN254_serialize
    ecdaa_credential_BN254_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_BN254)]
    ecdaa_credential_BN254_serialize.restype = None

    global ecdaa_credential_BN254_signature_serialize
    ecdaa_credential_BN254_signature_serialize = lib.ecdaa_credential_BN254_signature_serialize
    ecdaa_credential_BN254_signature_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_BN254_signature)]
    ecdaa_credential_BN254_signature_serialize.restype = None

    global ecdaa_credential_BN254_deserialize_with_signature
    ecdaa_credential_BN254_deserialize_with_signature = lib.ecdaa_credential_BN254_deserialize_with_signature
    ecdaa_credential_BN254_deserialize_with_signature.argtypes = [POINTER(struct_ecdaa_credential_BN254), POINTER(struct_ecdaa_member_public_key_BN254), POINTER(struct_ecdaa_group_public_key_BN254), POINTER(c_uint8), POINTER(c_uint8)]
    ecdaa_credential_BN254_deserialize_with_signature.restype = c_int

    global ecdaa_credential_BN254_deserialize
    ecdaa_credential_BN254_deserialize = lib.ecdaa_credential_BN254_deserialize
    ecdaa_credential_BN254_deserialize.argtypes = [POINTER(struct_ecdaa_credential_BN254), POINTER(c_uint8)]
    ecdaa_credential_BN254_deserialize.restype = c_int

    global ecdaa_credential_FP256BN_length
    ecdaa_credential_FP256BN_length = lib.ecdaa_credential_FP256BN_length
    ecdaa_credential_FP256BN_length.argtypes = []
    ecdaa_credential_FP256BN_length.restype = c_size_t

    global ecdaa_credential_FP256BN_signature_length
    ecdaa_credential_FP256BN_signature_length = lib.ecdaa_credential_FP256BN_signature_length
    ecdaa_credential_FP256BN_signature_length.argtypes = []
    ecdaa_credential_FP256BN_signature_length.restype = c_size_t

    global ecdaa_credential_FP256BN_generate
    ecdaa_credential_FP256BN_generate = lib.ecdaa_credential_FP256BN_generate
    ecdaa_credential_FP256BN_generate.argtypes = [POINTER(struct_ecdaa_credential_FP256BN), POINTER(struct_ecdaa_credential_FP256BN_signature), POINTER(struct_ecdaa_issuer_secret_key_FP256BN), POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(struct_ecdaa_prng)]
    ecdaa_credential_FP256BN_generate.restype = c_int

    global ecdaa_credential_FP256BN_validate
    ecdaa_credential_FP256BN_validate = lib.ecdaa_credential_FP256BN_validate
    ecdaa_credential_FP256BN_validate.argtypes = [POINTER(struct_ecdaa_credential_FP256BN), POINTER(struct_ecdaa_credential_FP256BN_signature), POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(struct_ecdaa_group_public_key_FP256BN)]
    ecdaa_credential_FP256BN_validate.restype = c_int

    global ecdaa_credential_FP256BN_serialize
    ecdaa_credential_FP256BN_serialize = lib.ecdaa_credential_FP256BN_serialize
    ecdaa_credential_FP256BN_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_FP256BN)]
    ecdaa_credential_FP256BN_serialize.restype = None

    global ecdaa_credential_FP256BN_signature_serialize
    ecdaa_credential_FP256BN_signature_serialize = lib.ecdaa_credential_FP256BN_signature_serialize
    ecdaa_credential_FP256BN_signature_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_credential_FP256BN_signature)]
    ecdaa_credential_FP256BN_signature_serialize.restype = None

    global ecdaa_credential_FP256BN_deserialize_with_signature
    ecdaa_credential_FP256BN_deserialize_with_signature = lib.ecdaa_credential_FP256BN_deserialize_with_signature
    ecdaa_credential_FP256BN_deserialize_with_signature.argtypes = [POINTER(struct_ecdaa_credential_FP256BN), POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(struct_ecdaa_group_public_key_FP256BN), POINTER(c_uint8), POINTER(c_uint8)]
    ecdaa_credential_FP256BN_deserialize_with_signature.restype = c_int

    global ecdaa_credential_FP256BN_deserialize
    ecdaa_credential_FP256BN_deserialize = lib.ecdaa_credential_FP256BN_deserialize
    ecdaa_credential_FP256BN_deserialize.argtypes = [POINTER(struct_ecdaa_credential_FP256BN), POINTER(c_uint8)]
    ecdaa_credential_FP256BN_deserialize.restype = c_int

    global ecdaa_group_public_key_BLS383_length
    ecdaa_group_public_key_BLS383_length = lib.ecdaa_group_public_key_BLS383_length
    ecdaa_group_public_key_BLS383_length.argtypes = []
    ecdaa_group_public_key_BLS383_length.restype = c_size_t

    global ecdaa_group_public_key_BLS383_serialize
    ecdaa_group_public_key_BLS383_serialize = lib.ecdaa_group_public_key_BLS383_serialize
    ecdaa_group_public_key_BLS383_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_group_public_key_BLS383)]
    ecdaa_group_public_key_BLS383_serialize.restype = None

    global ecdaa_group_public_key_BLS383_deserialize
    ecdaa_group_public_key_BLS383_deserialize = lib.ecdaa_group_public_key_BLS383_deserialize
    ecdaa_group_public_key_BLS383_deserialize.argtypes = [POINTER(struct_ecdaa_group_public_key_BLS383), POINTER(c_uint8)]
    ecdaa_group_public_key_BLS383_deserialize.restype = c_int

    global ecdaa_group_public_key_BN254CX_length
    ecdaa_group_public_key_BN254CX_length = lib.ecdaa_group_public_key_BN254CX_length
    ecdaa_group_public_key_BN254CX_length.argtypes = []
    ecdaa_group_public_key_BN254CX_length.restype = c_size_t

    global ecdaa_group_public_key_BN254CX_serialize
    ecdaa_group_public_key_BN254CX_serialize = lib.ecdaa_group_public_key_BN254CX_serialize
    ecdaa_group_public_key_BN254CX_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_group_public_key_BN254CX)]
    ecdaa_group_public_key_BN254CX_serialize.restype = None

    global ecdaa_group_public_key_BN254CX_deserialize
    ecdaa_group_public_key_BN254CX_deserialize = lib.ecdaa_group_public_key_BN254CX_deserialize
    ecdaa_group_public_key_BN254CX_deserialize.argtypes = [POINTER(struct_ecdaa_group_public_key_BN254CX), POINTER(c_uint8)]
    ecdaa_group_public_key_BN254CX_deserialize.restype = c_int

    global ecdaa_group_public_key_BN254_length
    ecdaa_group_public_key_BN254_length = lib.ecdaa_group_public_key_BN254_length
    ecdaa_group_public_key_BN254_length.argtypes = []
    ecdaa_group_public_key_BN254_length.restype = c_size_t

    global ecdaa_group_public_key_BN254_serialize
    ecdaa_group_public_key_BN254_serialize = lib.ecdaa_group_public_key_BN254_serialize
    ecdaa_group_public_key_BN254_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_group_public_key_BN254)]
    ecdaa_group_public_key_BN254_serialize.restype = None

    global ecdaa_group_public_key_BN254_deserialize
    ecdaa_group_public_key_BN254_deserialize = lib.ecdaa_group_public_key_BN254_deserialize
    ecdaa_group_public_key_BN254_deserialize.argtypes = [POINTER(struct_ecdaa_group_public_key_BN254), POINTER(c_uint8)]
    ecdaa_group_public_key_BN254_deserialize.restype = c_int

    global ecdaa_group_public_key_FP256BN_length
    ecdaa_group_public_key_FP256BN_length = lib.ecdaa_group_public_key_FP256BN_length
    ecdaa_group_public_key_FP256BN_length.argtypes = []
    ecdaa_group_public_key_FP256BN_length.restype = c_size_t

    global ecdaa_group_public_key_FP256BN_serialize
    ecdaa_group_public_key_FP256BN_serialize = lib.ecdaa_group_public_key_FP256BN_serialize
    ecdaa_group_public_key_FP256BN_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_group_public_key_FP256BN)]
    ecdaa_group_public_key_FP256BN_serialize.restype = None

    global ecdaa_group_public_key_FP256BN_deserialize
    ecdaa_group_public_key_FP256BN_deserialize = lib.ecdaa_group_public_key_FP256BN_deserialize
    ecdaa_group_public_key_FP256BN_deserialize.argtypes = [POINTER(struct_ecdaa_group_public_key_FP256BN), POINTER(c_uint8)]
    ecdaa_group_public_key_FP256BN_deserialize.restype = c_int

    global ecdaa_issuer_public_key_BLS383_length
    ecdaa_issuer_public_key_BLS383_length = lib.ecdaa_issuer_public_key_BLS383_length
    ecdaa_issuer_public_key_BLS383_length.argtypes = []
    ecdaa_issuer_public_key_BLS383_length.restype = c_size_t

    global ecdaa_issuer_secret_key_BLS383_length
    ecdaa_issuer_secret_key_BLS383_length = lib.ecdaa_issuer_secret_key_BLS383_length
    ecdaa_issuer_secret_key_BLS383_length.argtypes = []
    ecdaa_issuer_secret_key_BLS383_length.restype = c_size_t

    global ecdaa_issuer_key_pair_BLS383_generate
    ecdaa_issuer_key_pair_BLS383_generate = lib.ecdaa_issuer_key_pair_BLS383_generate
    ecdaa_issuer_key_pair_BLS383_generate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BLS383), POINTER(struct_ecdaa_issuer_secret_key_BLS383), POINTER(struct_ecdaa_prng)]
    ecdaa_issuer_key_pair_BLS383_generate.restype = c_int

    global ecdaa_issuer_public_key_BLS383_validate
    ecdaa_issuer_public_key_BLS383_validate = lib.ecdaa_issuer_public_key_BLS383_validate
    ecdaa_issuer_public_key_BLS383_validate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BLS383)]
    ecdaa_issuer_public_key_BLS383_validate.restype = c_int

    global ecdaa_issuer_public_key_BLS383_serialize
    ecdaa_issuer_public_key_BLS383_serialize = lib.ecdaa_issuer_public_key_BLS383_serialize
    ecdaa_issuer_public_key_BLS383_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_public_key_BLS383)]
    ecdaa_issuer_public_key_BLS383_serialize.restype = None

    global ecdaa_issuer_public_key_BLS383_deserialize
    ecdaa_issuer_public_key_BLS383_deserialize = lib.ecdaa_issuer_public_key_BLS383_deserialize
    ecdaa_issuer_public_key_BLS383_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BLS383), POINTER(c_uint8)]
    ecdaa_issuer_public_key_BLS383_deserialize.restype = c_int

    global ecdaa_issuer_secret_key_BLS383_serialize
    ecdaa_issuer_secret_key_BLS383_serialize = lib.ecdaa_issuer_secret_key_BLS383_serialize
    ecdaa_issuer_secret_key_BLS383_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_secret_key_BLS383)]
    ecdaa_issuer_secret_key_BLS383_serialize.restype = None

    global ecdaa_issuer_secret_key_BLS383_deserialize
    ecdaa_issuer_secret_key_BLS383_deserialize = lib.ecdaa_issuer_secret_key_BLS383_deserialize
    ecdaa_issuer_secret_key_BLS383_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_secret_key_BLS383), POINTER(c_uint8)]
    ecdaa_issuer_secret_key_BLS383_deserialize.restype = c_int

    global ecdaa_issuer_public_key_BN254CX_length
    ecdaa_issuer_public_key_BN254CX_length = lib.ecdaa_issuer_public_key_BN254CX_length
    ecdaa_issuer_public_key_BN254CX_length.argtypes = []
    ecdaa_issuer_public_key_BN254CX_length.restype = c_size_t

    global ecdaa_issuer_secret_key_BN254CX_length
    ecdaa_issuer_secret_key_BN254CX_length = lib.ecdaa_issuer_secret_key_BN254CX_length
    ecdaa_issuer_secret_key_BN254CX_length.argtypes = []
    ecdaa_issuer_secret_key_BN254CX_length.restype = c_size_t

    global ecdaa_issuer_key_pair_BN254CX_generate
    ecdaa_issuer_key_pair_BN254CX_generate = lib.ecdaa_issuer_key_pair_BN254CX_generate
    ecdaa_issuer_key_pair_BN254CX_generate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BN254CX), POINTER(struct_ecdaa_issuer_secret_key_BN254CX), POINTER(struct_ecdaa_prng)]
    ecdaa_issuer_key_pair_BN254CX_generate.restype = c_int

    global ecdaa_issuer_public_key_BN254CX_validate
    ecdaa_issuer_public_key_BN254CX_validate = lib.ecdaa_issuer_public_key_BN254CX_validate
    ecdaa_issuer_public_key_BN254CX_validate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BN254CX)]
    ecdaa_issuer_public_key_BN254CX_validate.restype = c_int

    global ecdaa_issuer_public_key_BN254CX_serialize
    ecdaa_issuer_public_key_BN254CX_serialize = lib.ecdaa_issuer_public_key_BN254CX_serialize
    ecdaa_issuer_public_key_BN254CX_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_public_key_BN254CX)]
    ecdaa_issuer_public_key_BN254CX_serialize.restype = None

    global ecdaa_issuer_public_key_BN254CX_deserialize
    ecdaa_issuer_public_key_BN254CX_deserialize = lib.ecdaa_issuer_public_key_BN254CX_deserialize
    ecdaa_issuer_public_key_BN254CX_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BN254CX), POINTER(c_uint8)]
    ecdaa_issuer_public_key_BN254CX_deserialize.restype = c_int

    global ecdaa_issuer_secret_key_BN254CX_serialize
    ecdaa_issuer_secret_key_BN254CX_serialize = lib.ecdaa_issuer_secret_key_BN254CX_serialize
    ecdaa_issuer_secret_key_BN254CX_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_secret_key_BN254CX)]
    ecdaa_issuer_secret_key_BN254CX_serialize.restype = None

    global ecdaa_issuer_secret_key_BN254CX_deserialize
    ecdaa_issuer_secret_key_BN254CX_deserialize = lib.ecdaa_issuer_secret_key_BN254CX_deserialize
    ecdaa_issuer_secret_key_BN254CX_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_secret_key_BN254CX), POINTER(c_uint8)]
    ecdaa_issuer_secret_key_BN254CX_deserialize.restype = c_int

    global ecdaa_issuer_public_key_BN254_length
    ecdaa_issuer_public_key_BN254_length = lib.ecdaa_issuer_public_key_BN254_length
    ecdaa_issuer_public_key_BN254_length.argtypes = []
    ecdaa_issuer_public_key_BN254_length.restype = c_size_t

    global ecdaa_issuer_secret_key_BN254_length
    ecdaa_issuer_secret_key_BN254_length = lib.ecdaa_issuer_secret_key_BN254_length
    ecdaa_issuer_secret_key_BN254_length.argtypes = []
    ecdaa_issuer_secret_key_BN254_length.restype = c_size_t

    global ecdaa_issuer_key_pair_BN254_generate
    ecdaa_issuer_key_pair_BN254_generate = lib.ecdaa_issuer_key_pair_BN254_generate
    ecdaa_issuer_key_pair_BN254_generate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BN254), POINTER(struct_ecdaa_issuer_secret_key_BN254), POINTER(struct_ecdaa_prng)]
    ecdaa_issuer_key_pair_BN254_generate.restype = c_int

    global ecdaa_issuer_public_key_BN254_validate
    ecdaa_issuer_public_key_BN254_validate = lib.ecdaa_issuer_public_key_BN254_validate
    ecdaa_issuer_public_key_BN254_validate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BN254)]
    ecdaa_issuer_public_key_BN254_validate.restype = c_int

    global ecdaa_issuer_public_key_BN254_serialize
    ecdaa_issuer_public_key_BN254_serialize = lib.ecdaa_issuer_public_key_BN254_serialize
    ecdaa_issuer_public_key_BN254_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_public_key_BN254)]
    ecdaa_issuer_public_key_BN254_serialize.restype = None

    global ecdaa_issuer_public_key_BN254_deserialize
    ecdaa_issuer_public_key_BN254_deserialize = lib.ecdaa_issuer_public_key_BN254_deserialize
    ecdaa_issuer_public_key_BN254_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_public_key_BN254), POINTER(c_uint8)]
    ecdaa_issuer_public_key_BN254_deserialize.restype = c_int

    global ecdaa_issuer_secret_key_BN254_serialize
    ecdaa_issuer_secret_key_BN254_serialize = lib.ecdaa_issuer_secret_key_BN254_serialize
    ecdaa_issuer_secret_key_BN254_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_secret_key_BN254)]
    ecdaa_issuer_secret_key_BN254_serialize.restype = None

    global ecdaa_issuer_secret_key_BN254_deserialize
    ecdaa_issuer_secret_key_BN254_deserialize = lib.ecdaa_issuer_secret_key_BN254_deserialize
    ecdaa_issuer_secret_key_BN254_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_secret_key_BN254), POINTER(c_uint8)]
    ecdaa_issuer_secret_key_BN254_deserialize.restype = c_int

    global ecdaa_issuer_public_key_FP256BN_length
    ecdaa_issuer_public_key_FP256BN_length = lib.ecdaa_issuer_public_key_FP256BN_length
    ecdaa_issuer_public_key_FP256BN_length.argtypes = []
    ecdaa_issuer_public_key_FP256BN_length.restype = c_size_t

    global ecdaa_issuer_secret_key_FP256BN_length
    ecdaa_issuer_secret_key_FP256BN_length = lib.ecdaa_issuer_secret_key_FP256BN_length
    ecdaa_issuer_secret_key_FP256BN_length.argtypes = []
    ecdaa_issuer_secret_key_FP256BN_length.restype = c_size_t

    global ecdaa_issuer_key_pair_FP256BN_generate
    ecdaa_issuer_key_pair_FP256BN_generate = lib.ecdaa_issuer_key_pair_FP256BN_generate
    ecdaa_issuer_key_pair_FP256BN_generate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_FP256BN), POINTER(struct_ecdaa_issuer_secret_key_FP256BN), POINTER(struct_ecdaa_prng)]
    ecdaa_issuer_key_pair_FP256BN_generate.restype = c_int

    global ecdaa_issuer_public_key_FP256BN_validate
    ecdaa_issuer_public_key_FP256BN_validate = lib.ecdaa_issuer_public_key_FP256BN_validate
    ecdaa_issuer_public_key_FP256BN_validate.argtypes = [POINTER(struct_ecdaa_issuer_public_key_FP256BN)]
    ecdaa_issuer_public_key_FP256BN_validate.restype = c_int

    global ecdaa_issuer_public_key_FP256BN_serialize
    ecdaa_issuer_public_key_FP256BN_serialize = lib.ecdaa_issuer_public_key_FP256BN_serialize
    ecdaa_issuer_public_key_FP256BN_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_public_key_FP256BN)]
    ecdaa_issuer_public_key_FP256BN_serialize.restype = None

    global ecdaa_issuer_public_key_FP256BN_deserialize
    ecdaa_issuer_public_key_FP256BN_deserialize = lib.ecdaa_issuer_public_key_FP256BN_deserialize
    ecdaa_issuer_public_key_FP256BN_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_public_key_FP256BN), POINTER(c_uint8)]
    ecdaa_issuer_public_key_FP256BN_deserialize.restype = c_int

    global ecdaa_issuer_secret_key_FP256BN_serialize
    ecdaa_issuer_secret_key_FP256BN_serialize = lib.ecdaa_issuer_secret_key_FP256BN_serialize
    ecdaa_issuer_secret_key_FP256BN_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_issuer_secret_key_FP256BN)]
    ecdaa_issuer_secret_key_FP256BN_serialize.restype = None

    global ecdaa_issuer_secret_key_FP256BN_deserialize
    ecdaa_issuer_secret_key_FP256BN_deserialize = lib.ecdaa_issuer_secret_key_FP256BN_deserialize
    ecdaa_issuer_secret_key_FP256BN_deserialize.argtypes = [POINTER(struct_ecdaa_issuer_secret_key_FP256BN), POINTER(c_uint8)]
    ecdaa_issuer_secret_key_FP256BN_deserialize.restype = c_int

    global ecdaa_member_public_key_BLS383_length
    ecdaa_member_public_key_BLS383_length = lib.ecdaa_member_public_key_BLS383_length
    ecdaa_member_public_key_BLS383_length.argtypes = []
    ecdaa_member_public_key_BLS383_length.restype = c_size_t

    global ecdaa_member_secret_key_BLS383_length
    ecdaa_member_secret_key_BLS383_length = lib.ecdaa_member_secret_key_BLS383_length
    ecdaa_member_secret_key_BLS383_length.argtypes = []
    ecdaa_member_secret_key_BLS383_length.restype = c_size_t

    global ecdaa_member_key_pair_BLS383_generate
    ecdaa_member_key_pair_BLS383_generate = lib.ecdaa_member_key_pair_BLS383_generate
    ecdaa_member_key_pair_BLS383_generate.argtypes = [POINTER(struct_ecdaa_member_public_key_BLS383), POINTER(struct_ecdaa_member_secret_key_BLS383), POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_prng)]
    ecdaa_member_key_pair_BLS383_generate.restype = c_int

    global ecdaa_member_public_key_BLS383_validate
    ecdaa_member_public_key_BLS383_validate = lib.ecdaa_member_public_key_BLS383_validate
    ecdaa_member_public_key_BLS383_validate.argtypes = [POINTER(struct_ecdaa_member_public_key_BLS383), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_BLS383_validate.restype = c_int

    global ecdaa_member_public_key_BLS383_serialize
    ecdaa_member_public_key_BLS383_serialize = lib.ecdaa_member_public_key_BLS383_serialize
    ecdaa_member_public_key_BLS383_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_public_key_BLS383)]
    ecdaa_member_public_key_BLS383_serialize.restype = None

    global ecdaa_member_public_key_BLS383_deserialize
    ecdaa_member_public_key_BLS383_deserialize = lib.ecdaa_member_public_key_BLS383_deserialize
    ecdaa_member_public_key_BLS383_deserialize.argtypes = [POINTER(struct_ecdaa_member_public_key_BLS383), POINTER(c_uint8), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_BLS383_deserialize.restype = c_int

    global ecdaa_member_public_key_BLS383_deserialize_no_check
    ecdaa_member_public_key_BLS383_deserialize_no_check = lib.ecdaa_member_public_key_BLS383_deserialize_no_check
    ecdaa_member_public_key_BLS383_deserialize_no_check.argtypes = [POINTER(struct_ecdaa_member_public_key_BLS383), POINTER(c_uint8)]
    ecdaa_member_public_key_BLS383_deserialize_no_check.restype = c_int

    global ecdaa_member_secret_key_BLS383_serialize
    ecdaa_member_secret_key_BLS383_serialize = lib.ecdaa_member_secret_key_BLS383_serialize
    ecdaa_member_secret_key_BLS383_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_secret_key_BLS383)]
    ecdaa_member_secret_key_BLS383_serialize.restype = None

    global ecdaa_member_secret_key_BLS383_deserialize
    ecdaa_member_secret_key_BLS383_deserialize = lib.ecdaa_member_secret_key_BLS383_deserialize
    ecdaa_member_secret_key_BLS383_deserialize.argtypes = [POINTER(struct_ecdaa_member_secret_key_BLS383), POINTER(c_uint8)]
    ecdaa_member_secret_key_BLS383_deserialize.restype = c_int

    global ecdaa_member_public_key_BN254CX_length
    ecdaa_member_public_key_BN254CX_length = lib.ecdaa_member_public_key_BN254CX_length
    ecdaa_member_public_key_BN254CX_length.argtypes = []
    ecdaa_member_public_key_BN254CX_length.restype = c_size_t

    global ecdaa_member_secret_key_BN254CX_length
    ecdaa_member_secret_key_BN254CX_length = lib.ecdaa_member_secret_key_BN254CX_length
    ecdaa_member_secret_key_BN254CX_length.argtypes = []
    ecdaa_member_secret_key_BN254CX_length.restype = c_size_t

    global ecdaa_member_key_pair_BN254CX_generate
    ecdaa_member_key_pair_BN254CX_generate = lib.ecdaa_member_key_pair_BN254CX_generate
    ecdaa_member_key_pair_BN254CX_generate.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254CX), POINTER(struct_ecdaa_member_secret_key_BN254CX), POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_prng)]
    ecdaa_member_key_pair_BN254CX_generate.restype = c_int

    global ecdaa_member_public_key_BN254CX_validate
    ecdaa_member_public_key_BN254CX_validate = lib.ecdaa_member_public_key_BN254CX_validate
    ecdaa_member_public_key_BN254CX_validate.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254CX), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_BN254CX_validate.restype = c_int

    global ecdaa_member_public_key_BN254CX_serialize
    ecdaa_member_public_key_BN254CX_serialize = lib.ecdaa_member_public_key_BN254CX_serialize
    ecdaa_member_public_key_BN254CX_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_public_key_BN254CX)]
    ecdaa_member_public_key_BN254CX_serialize.restype = None

    global ecdaa_member_public_key_BN254CX_deserialize
    ecdaa_member_public_key_BN254CX_deserialize = lib.ecdaa_member_public_key_BN254CX_deserialize
    ecdaa_member_public_key_BN254CX_deserialize.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254CX), POINTER(c_uint8), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_BN254CX_deserialize.restype = c_int

    global ecdaa_member_public_key_BN254CX_deserialize_no_check
    ecdaa_member_public_key_BN254CX_deserialize_no_check = lib.ecdaa_member_public_key_BN254CX_deserialize_no_check
    ecdaa_member_public_key_BN254CX_deserialize_no_check.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254CX), POINTER(c_uint8)]
    ecdaa_member_public_key_BN254CX_deserialize_no_check.restype = c_int

    global ecdaa_member_secret_key_BN254CX_serialize
    ecdaa_member_secret_key_BN254CX_serialize = lib.ecdaa_member_secret_key_BN254CX_serialize
    ecdaa_member_secret_key_BN254CX_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_secret_key_BN254CX)]
    ecdaa_member_secret_key_BN254CX_serialize.restype = None

    global ecdaa_member_secret_key_BN254CX_deserialize
    ecdaa_member_secret_key_BN254CX_deserialize = lib.ecdaa_member_secret_key_BN254CX_deserialize
    ecdaa_member_secret_key_BN254CX_deserialize.argtypes = [POINTER(struct_ecdaa_member_secret_key_BN254CX), POINTER(c_uint8)]
    ecdaa_member_secret_key_BN254CX_deserialize.restype = c_int

    global ecdaa_member_public_key_BN254_length
    ecdaa_member_public_key_BN254_length = lib.ecdaa_member_public_key_BN254_length
    ecdaa_member_public_key_BN254_length.argtypes = []
    ecdaa_member_public_key_BN254_length.restype = c_size_t

    global ecdaa_member_secret_key_BN254_length
    ecdaa_member_secret_key_BN254_length = lib.ecdaa_member_secret_key_BN254_length
    ecdaa_member_secret_key_BN254_length.argtypes = []
    ecdaa_member_secret_key_BN254_length.restype = c_size_t

    global ecdaa_member_key_pair_BN254_generate
    ecdaa_member_key_pair_BN254_generate = lib.ecdaa_member_key_pair_BN254_generate
    ecdaa_member_key_pair_BN254_generate.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254), POINTER(struct_ecdaa_member_secret_key_BN254), POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_prng)]
    ecdaa_member_key_pair_BN254_generate.restype = c_int

    global ecdaa_member_public_key_BN254_validate
    ecdaa_member_public_key_BN254_validate = lib.ecdaa_member_public_key_BN254_validate
    ecdaa_member_public_key_BN254_validate.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_BN254_validate.restype = c_int

    global ecdaa_member_public_key_BN254_serialize
    ecdaa_member_public_key_BN254_serialize = lib.ecdaa_member_public_key_BN254_serialize
    ecdaa_member_public_key_BN254_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_public_key_BN254)]
    ecdaa_member_public_key_BN254_serialize.restype = None

    global ecdaa_member_public_key_BN254_deserialize
    ecdaa_member_public_key_BN254_deserialize = lib.ecdaa_member_public_key_BN254_deserialize
    ecdaa_member_public_key_BN254_deserialize.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254), POINTER(c_uint8), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_BN254_deserialize.restype = c_int

    global ecdaa_member_public_key_BN254_deserialize_no_check
    ecdaa_member_public_key_BN254_deserialize_no_check = lib.ecdaa_member_public_key_BN254_deserialize_no_check
    ecdaa_member_public_key_BN254_deserialize_no_check.argtypes = [POINTER(struct_ecdaa_member_public_key_BN254), POINTER(c_uint8)]
    ecdaa_member_public_key_BN254_deserialize_no_check.restype = c_int

    global ecdaa_member_secret_key_BN254_serialize
    ecdaa_member_secret_key_BN254_serialize = lib.ecdaa_member_secret_key_BN254_serialize
    ecdaa_member_secret_key_BN254_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_secret_key_BN254)]
    ecdaa_member_secret_key_BN254_serialize.restype = None

    global ecdaa_member_secret_key_BN254_deserialize
    ecdaa_member_secret_key_BN254_deserialize = lib.ecdaa_member_secret_key_BN254_deserialize
    ecdaa_member_secret_key_BN254_deserialize.argtypes = [POINTER(struct_ecdaa_member_secret_key_BN254), POINTER(c_uint8)]
    ecdaa_member_secret_key_BN254_deserialize.restype = c_int

    global ecdaa_member_public_key_FP256BN_length
    ecdaa_member_public_key_FP256BN_length = lib.ecdaa_member_public_key_FP256BN_length
    ecdaa_member_public_key_FP256BN_length.argtypes = []
    ecdaa_member_public_key_FP256BN_length.restype = c_size_t

    global ecdaa_member_secret_key_FP256BN_length
    ecdaa_member_secret_key_FP256BN_length = lib.ecdaa_member_secret_key_FP256BN_length
    ecdaa_member_secret_key_FP256BN_length.argtypes = []
    ecdaa_member_secret_key_FP256BN_length.restype = c_size_t

    global ecdaa_member_key_pair_FP256BN_generate
    ecdaa_member_key_pair_FP256BN_generate = lib.ecdaa_member_key_pair_FP256BN_generate
    ecdaa_member_key_pair_FP256BN_generate.argtypes = [POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(struct_ecdaa_member_secret_key_FP256BN), POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_prng)]
    ecdaa_member_key_pair_FP256BN_generate.restype = c_int

    global ecdaa_member_public_key_FP256BN_validate
    ecdaa_member_public_key_FP256BN_validate = lib.ecdaa_member_public_key_FP256BN_validate
    ecdaa_member_public_key_FP256BN_validate.argtypes = [POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_FP256BN_validate.restype = c_int

    global ecdaa_member_public_key_FP256BN_serialize
    ecdaa_member_public_key_FP256BN_serialize = lib.ecdaa_member_public_key_FP256BN_serialize
    ecdaa_member_public_key_FP256BN_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_public_key_FP256BN)]
    ecdaa_member_public_key_FP256BN_serialize.restype = None

    global ecdaa_member_public_key_FP256BN_deserialize
    ecdaa_member_public_key_FP256BN_deserialize = lib.ecdaa_member_public_key_FP256BN_deserialize
    ecdaa_member_public_key_FP256BN_deserialize.argtypes = [POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(c_uint8), POINTER(c_uint8), c_uint32]
    ecdaa_member_public_key_FP256BN_deserialize.restype = c_int

    global ecdaa_member_public_key_FP256BN_deserialize_no_check
    ecdaa_member_public_key_FP256BN_deserialize_no_check = lib.ecdaa_member_public_key_FP256BN_deserialize_no_check
    ecdaa_member_public_key_FP256BN_deserialize_no_check.argtypes = [POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(c_uint8)]
    ecdaa_member_public_key_FP256BN_deserialize_no_check.restype = c_int

    global ecdaa_member_secret_key_FP256BN_serialize
    ecdaa_member_secret_key_FP256BN_serialize = lib.ecdaa_member_secret_key_FP256BN_serialize
    ecdaa_member_secret_key_FP256BN_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_member_secret_key_FP256BN)]
    ecdaa_member_secret_key_FP256BN_serialize.restype = None

    global ecdaa_member_secret_key_FP256BN_deserialize
    ecdaa_member_secret_key_FP256BN_deserialize = lib.ecdaa_member_secret_key_FP256BN_deserialize
    ecdaa_member_secret_key_FP256BN_deserialize.argtypes = [POINTER(struct_ecdaa_member_secret_key_FP256BN), POINTER(c_uint8)]
    ecdaa_member_secret_key_FP256BN_deserialize.restype = c_int

    global ecdaa_tpm_context_init_socket
    ecdaa_tpm_context_init_socket = lib.ecdaa_tpm_context_init_socket
    ecdaa_tpm_context_init_socket.argtypes = [POINTER(struct_ecdaa_tpm_context), POINTER(c_uint8), TPM_HANDLE, String, String, String, c_uint16]
    ecdaa_tpm_context_init_socket.restype = c_int

    global ecdaa_tpm_context_free
    ecdaa_tpm_context_free = lib.ecdaa_tpm_context_free
    ecdaa_tpm_context_free.argtypes = [POINTER(struct_ecdaa_tpm_context)]
    ecdaa_tpm_context_free.restype = None

    global ecdaa_member_key_pair_TPM_generate
    ecdaa_member_key_pair_TPM_generate = lib.ecdaa_member_key_pair_TPM_generate
    ecdaa_member_key_pair_TPM_generate.argtypes = [POINTER(struct_ecdaa_member_public_key_FP256BN), POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_tpm_context)]
    ecdaa_member_key_pair_TPM_generate.restype = c_int

    global get_csprng
    get_csprng = lib.get_csprng
    get_csprng.argtypes = [POINTER(struct_ecdaa_prng)]
    get_csprng.restype = POINTER(csprng)

    global ecdaa_prng_free
    ecdaa_prng_free = lib.ecdaa_prng_free
    ecdaa_prng_free.argtypes = [POINTER(struct_ecdaa_prng)]
    ecdaa_prng_free.restype = None

    global ecdaa_prng_init
    ecdaa_prng_init = lib.ecdaa_prng_init
    ecdaa_prng_init.argtypes = [POINTER(struct_ecdaa_prng)]
    ecdaa_prng_init.restype = c_int

    global ecdaa_prng_init_custom
    ecdaa_prng_init_custom = lib.ecdaa_prng_init_custom
    ecdaa_prng_init_custom.argtypes = [POINTER(struct_ecdaa_prng), String, c_size_t]
    ecdaa_prng_init_custom.restype = c_int

    global ecdaa_signature_BLS383_length
    ecdaa_signature_BLS383_length = lib.ecdaa_signature_BLS383_length
    ecdaa_signature_BLS383_length.argtypes = []
    ecdaa_signature_BLS383_length.restype = c_size_t

    global ecdaa_signature_BLS383_with_nym_length
    ecdaa_signature_BLS383_with_nym_length = lib.ecdaa_signature_BLS383_with_nym_length
    ecdaa_signature_BLS383_with_nym_length.argtypes = []
    ecdaa_signature_BLS383_with_nym_length.restype = c_size_t

    global ecdaa_signature_BLS383_sign
    ecdaa_signature_BLS383_sign = lib.ecdaa_signature_BLS383_sign
    ecdaa_signature_BLS383_sign.argtypes = [POINTER(struct_ecdaa_signature_BLS383), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_member_secret_key_BLS383), POINTER(struct_ecdaa_credential_BLS383), POINTER(struct_ecdaa_prng)]
    ecdaa_signature_BLS383_sign.restype = c_int

    global ecdaa_signature_BLS383_verify
    ecdaa_signature_BLS383_verify = lib.ecdaa_signature_BLS383_verify
    ecdaa_signature_BLS383_verify.argtypes = [POINTER(struct_ecdaa_signature_BLS383), POINTER(struct_ecdaa_group_public_key_BLS383), POINTER(struct_ecdaa_revocations_BLS383), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32]
    ecdaa_signature_BLS383_verify.restype = c_int

    global ecdaa_signature_BLS383_serialize
    ecdaa_signature_BLS383_serialize = lib.ecdaa_signature_BLS383_serialize
    ecdaa_signature_BLS383_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_signature_BLS383), c_int]
    ecdaa_signature_BLS383_serialize.restype = None

    global ecdaa_signature_BLS383_deserialize
    ecdaa_signature_BLS383_deserialize = lib.ecdaa_signature_BLS383_deserialize
    ecdaa_signature_BLS383_deserialize.argtypes = [POINTER(struct_ecdaa_signature_BLS383), POINTER(c_uint8), c_int]
    ecdaa_signature_BLS383_deserialize.restype = c_int

    global ecdaa_signature_BLS383_deserialize_and_verify
    ecdaa_signature_BLS383_deserialize_and_verify = lib.ecdaa_signature_BLS383_deserialize_and_verify
    ecdaa_signature_BLS383_deserialize_and_verify.argtypes = [POINTER(struct_ecdaa_signature_BLS383), POINTER(struct_ecdaa_group_public_key_BLS383), POINTER(struct_ecdaa_revocations_BLS383), POINTER(c_uint8), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, c_int]
    ecdaa_signature_BLS383_deserialize_and_verify.restype = c_int

    global ecdaa_signature_BN254CX_length
    ecdaa_signature_BN254CX_length = lib.ecdaa_signature_BN254CX_length
    ecdaa_signature_BN254CX_length.argtypes = []
    ecdaa_signature_BN254CX_length.restype = c_size_t

    global ecdaa_signature_BN254CX_with_nym_length
    ecdaa_signature_BN254CX_with_nym_length = lib.ecdaa_signature_BN254CX_with_nym_length
    ecdaa_signature_BN254CX_with_nym_length.argtypes = []
    ecdaa_signature_BN254CX_with_nym_length.restype = c_size_t

    global ecdaa_signature_BN254CX_sign
    ecdaa_signature_BN254CX_sign = lib.ecdaa_signature_BN254CX_sign
    ecdaa_signature_BN254CX_sign.argtypes = [POINTER(struct_ecdaa_signature_BN254CX), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_member_secret_key_BN254CX), POINTER(struct_ecdaa_credential_BN254CX), POINTER(struct_ecdaa_prng)]
    ecdaa_signature_BN254CX_sign.restype = c_int

    global ecdaa_signature_BN254CX_verify
    ecdaa_signature_BN254CX_verify = lib.ecdaa_signature_BN254CX_verify
    ecdaa_signature_BN254CX_verify.argtypes = [POINTER(struct_ecdaa_signature_BN254CX), POINTER(struct_ecdaa_group_public_key_BN254CX), POINTER(struct_ecdaa_revocations_BN254CX), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32]
    ecdaa_signature_BN254CX_verify.restype = c_int

    global ecdaa_signature_BN254CX_serialize
    ecdaa_signature_BN254CX_serialize = lib.ecdaa_signature_BN254CX_serialize
    ecdaa_signature_BN254CX_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_signature_BN254CX), c_int]
    ecdaa_signature_BN254CX_serialize.restype = None

    global ecdaa_signature_BN254CX_deserialize
    ecdaa_signature_BN254CX_deserialize = lib.ecdaa_signature_BN254CX_deserialize
    ecdaa_signature_BN254CX_deserialize.argtypes = [POINTER(struct_ecdaa_signature_BN254CX), POINTER(c_uint8), c_int]
    ecdaa_signature_BN254CX_deserialize.restype = c_int

    global ecdaa_signature_BN254CX_deserialize_and_verify
    ecdaa_signature_BN254CX_deserialize_and_verify = lib.ecdaa_signature_BN254CX_deserialize_and_verify
    ecdaa_signature_BN254CX_deserialize_and_verify.argtypes = [POINTER(struct_ecdaa_signature_BN254CX), POINTER(struct_ecdaa_group_public_key_BN254CX), POINTER(struct_ecdaa_revocations_BN254CX), POINTER(c_uint8), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, c_int]
    ecdaa_signature_BN254CX_deserialize_and_verify.restype = c_int

    global ecdaa_signature_BN254_length
    ecdaa_signature_BN254_length = lib.ecdaa_signature_BN254_length
    ecdaa_signature_BN254_length.argtypes = []
    ecdaa_signature_BN254_length.restype = c_size_t

    global ecdaa_signature_BN254_with_nym_length
    ecdaa_signature_BN254_with_nym_length = lib.ecdaa_signature_BN254_with_nym_length
    ecdaa_signature_BN254_with_nym_length.argtypes = []
    ecdaa_signature_BN254_with_nym_length.restype = c_size_t

    global ecdaa_signature_BN254_sign
    ecdaa_signature_BN254_sign = lib.ecdaa_signature_BN254_sign
    ecdaa_signature_BN254_sign.argtypes = [POINTER(struct_ecdaa_signature_BN254), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_member_secret_key_BN254), POINTER(struct_ecdaa_credential_BN254), POINTER(struct_ecdaa_prng)]
    ecdaa_signature_BN254_sign.restype = c_int

    global ecdaa_signature_BN254_verify
    ecdaa_signature_BN254_verify = lib.ecdaa_signature_BN254_verify
    ecdaa_signature_BN254_verify.argtypes = [POINTER(struct_ecdaa_signature_BN254), POINTER(struct_ecdaa_group_public_key_BN254), POINTER(struct_ecdaa_revocations_BN254), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32]
    ecdaa_signature_BN254_verify.restype = c_int

    global ecdaa_signature_BN254_serialize
    ecdaa_signature_BN254_serialize = lib.ecdaa_signature_BN254_serialize
    ecdaa_signature_BN254_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_signature_BN254), c_int]
    ecdaa_signature_BN254_serialize.restype = None

    global ecdaa_signature_BN254_deserialize
    ecdaa_signature_BN254_deserialize = lib.ecdaa_signature_BN254_deserialize
    ecdaa_signature_BN254_deserialize.argtypes = [POINTER(struct_ecdaa_signature_BN254), POINTER(c_uint8), c_int]
    ecdaa_signature_BN254_deserialize.restype = c_int

    global ecdaa_signature_BN254_deserialize_and_verify
    ecdaa_signature_BN254_deserialize_and_verify = lib.ecdaa_signature_BN254_deserialize_and_verify
    ecdaa_signature_BN254_deserialize_and_verify.argtypes = [POINTER(struct_ecdaa_signature_BN254), POINTER(struct_ecdaa_group_public_key_BN254), POINTER(struct_ecdaa_revocations_BN254), POINTER(c_uint8), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, c_int]
    ecdaa_signature_BN254_deserialize_and_verify.restype = c_int

    global ecdaa_signature_FP256BN_length
    ecdaa_signature_FP256BN_length = lib.ecdaa_signature_FP256BN_length
    ecdaa_signature_FP256BN_length.argtypes = []
    ecdaa_signature_FP256BN_length.restype = c_size_t

    global ecdaa_signature_FP256BN_with_nym_length
    ecdaa_signature_FP256BN_with_nym_length = lib.ecdaa_signature_FP256BN_with_nym_length
    ecdaa_signature_FP256BN_with_nym_length.argtypes = []
    ecdaa_signature_FP256BN_with_nym_length.restype = c_size_t

    global ecdaa_signature_FP256BN_sign
    ecdaa_signature_FP256BN_sign = lib.ecdaa_signature_FP256BN_sign
    ecdaa_signature_FP256BN_sign.argtypes = [POINTER(struct_ecdaa_signature_FP256BN), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_member_secret_key_FP256BN), POINTER(struct_ecdaa_credential_FP256BN), POINTER(struct_ecdaa_prng)]
    ecdaa_signature_FP256BN_sign.restype = c_int

    global ecdaa_signature_FP256BN_verify
    ecdaa_signature_FP256BN_verify = lib.ecdaa_signature_FP256BN_verify
    ecdaa_signature_FP256BN_verify.argtypes = [POINTER(struct_ecdaa_signature_FP256BN), POINTER(struct_ecdaa_group_public_key_FP256BN), POINTER(struct_ecdaa_revocations_FP256BN), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32]
    ecdaa_signature_FP256BN_verify.restype = c_int

    global ecdaa_signature_FP256BN_serialize
    ecdaa_signature_FP256BN_serialize = lib.ecdaa_signature_FP256BN_serialize
    ecdaa_signature_FP256BN_serialize.argtypes = [POINTER(c_uint8), POINTER(struct_ecdaa_signature_FP256BN), c_int]
    ecdaa_signature_FP256BN_serialize.restype = None

    global ecdaa_signature_FP256BN_deserialize
    ecdaa_signature_FP256BN_deserialize = lib.ecdaa_signature_FP256BN_deserialize
    ecdaa_signature_FP256BN_deserialize.argtypes = [POINTER(struct_ecdaa_signature_FP256BN), POINTER(c_uint8), c_int]
    ecdaa_signature_FP256BN_deserialize.restype = c_int

    global ecdaa_signature_FP256BN_deserialize_and_verify
    ecdaa_signature_FP256BN_deserialize_and_verify = lib.ecdaa_signature_FP256BN_deserialize_and_verify
    ecdaa_signature_FP256BN_deserialize_and_verify.argtypes = [POINTER(struct_ecdaa_signature_FP256BN), POINTER(struct_ecdaa_group_public_key_FP256BN), POINTER(struct_ecdaa_revocations_FP256BN), POINTER(c_uint8), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, c_int]
    ecdaa_signature_FP256BN_deserialize_and_verify.restype = c_int

    global ecdaa_signature_TPM_sign
    ecdaa_signature_TPM_sign = lib.ecdaa_signature_TPM_sign
    ecdaa_signature_TPM_sign.argtypes = [POINTER(struct_ecdaa_signature_FP256BN), POINTER(c_uint8), c_uint32, POINTER(c_uint8), c_uint32, POINTER(struct_ecdaa_credential_FP256BN), POINTER(struct_ecdaa_prng), POINTER(struct_ecdaa_tpm_context)]
    ecdaa_signature_TPM_sign.restype = c_int
