from conans import ConanFile, CMake, tools
import os


class RedoxConan(ConanFile):
    name = "Redox"
    version = "1.0.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
       self.run("git clone https://github.com/hmartiro/redox")
       self.run("cd redox")
       # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
       # if the packaged project doesn't have variables to set it properly
       #tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()''')

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake redox %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="redox/include")
        self.copy("*.hpp", dst="include", src="redox/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["redox_static", "ev", "hiredis"]
