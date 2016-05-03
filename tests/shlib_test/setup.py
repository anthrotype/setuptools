from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command import build_ext as build_ext_mod
from setuptools.extension import Library
from distutils.ccompiler import new_compiler
import os
import sys


# disable automatic creation of "dl-*" stub loaders on OS X
if sys.platform == "darwin":
    build_ext_mod.use_stubs = False


class BuildExt(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        compiler_type = new_compiler(compiler=self.compiler).compiler_type
        # add build_temp to library_dirs so linker finds the DLL import lib
        for ext in self.extensions:
            if compiler_type == "msvc":
                ext.library_dirs.append(self.build_temp)
            elif sys.platform == "darwin" and compiler_type == "unix":
                # set the dylib 'install_name' relative to the extension's path
                if isinstance(ext, Library):
                    fullname = self.get_ext_fullname(ext.name)
                    modpath = fullname.split(".")
                    filename = self.get_ext_filename(modpath[-1])
                    ext.extra_link_args.extend(
                        ['-install_name', "@loader_path/"+filename])


setup(
    name="shlib_test",
    ext_modules=[
        Library("hello.hellolib", ["hellolib.c"], export_symbols=["get_hello_msg"]),
        Extension("hello.hello", ["hello.pyx"], libraries=["hellolib"])
    ],
    test_suite="test_hello.HelloWorldTest",
    cmdclass={'build_ext': BuildExt},
    packages=["hello"],
    zip_safe=False,
)
