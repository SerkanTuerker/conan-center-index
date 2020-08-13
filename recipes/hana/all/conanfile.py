from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration
import os


class HanaConan(ConanFile):
    name = "hana"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://boostorg.github.io/hana/"
    description = "Hana is a header-only library for C++ metaprogramming suited for computations on both types and values."
    license = "BSL-1.0"
    topics = ("hana", "metaprogramming", "boost")
    settings = "os", "compiler"
    no_copy_source = True
    exports_sources = "CMakeLists.txt"

    _compiler_cpp14_support = {
        "gcc": "5",
        "Visual Studio": "14",
        "clang": "3.4",
        "apple-clang": "3.4",
    }

    @property
    def _source_subfolder(self):
        return "_source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("hana-" + self.version, self._source_subfolder)

    def config_options(self):
        tools.check_min_cppstd(self, "14")
        try:
            minimum_required_version = self._compiler_cpp14_support[str(self.settings.compiler)]
            if self.settings.compiler.version < tools.Version(minimum_required_version):
                raise ConanInvalidConfiguration(
                    "This compiler is too old. This library needs a compiler with c++14 support")
        except KeyError:
            self.output.warn("This recipe might not support the compiler. Consider adding it.")

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.install()

        self.copy("LICENSE.md", dst="licenses", src=self._source_subfolder)
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_id(self):
        self.info.header_only()
