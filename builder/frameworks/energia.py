"""
Energia
Energia Wiring-based framework enables pretty much anyone to start easily
creating microcontroller-based projects and applications. Its easy-to-use
libraries and functions provide developers of all experience levels to start
blinking LEDs, buzzing buzzers and sensing sensors more quickly than ever
before.
http://energia.nu/reference/
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-energiamsp432r")
FRAMEWORK_VERSION = platform.get_package_version("framework-energiamsp432r")
assert isdir(FRAMEWORK_DIR)

board = env.BoardConfig()

variants_dir = join(
    "$PROJECT_DIR", board.get("build.variants_dir")) if board.get(
        "build.variants_dir", "") else join(FRAMEWORK_DIR, "variants")

env.Append(
    CPPDEFINES=[
        ("ARDUINO", 10807),
        ("ENERGIA", int(FRAMEWORK_VERSION.split(".")[1]))
    ],
    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", env.BoardConfig().get("build.core")),
        join(variants_dir, board.get("build.variant")),
        join(platform.get_package_dir("toolchain-timsp432"), "arm"),
        join(platform.get_package_dir("toolchain-timsp432"), "arm_compiler"),
        join(FRAMEWORK_DIR,"system","source"),
        join(FRAMEWORK_DIR,"system","source","ti","devices","msp432p4xx"),
        join(FRAMEWORK_DIR,"system","kernel","tirtos"),
        join(FRAMEWORK_DIR,"system","kernel","tirtos","packages"),
        join(FRAMEWORK_DIR,"system","tools","xdctools_core"),
        join(platform.get_package_dir("toolchain-timsp432"), "arm_compiler","lib","gcc","arm-none-eabi","6.2.1","include"),
        join(platform.get_package_dir("toolchain-timsp432"), "arm_compiler","arm-none-eabi","include"),
        join(platform.get_package_dir("toolchain-timsp432"), "arm_compiler","arm-none-eabi","include","c++","6.2.1"),
        join(platform.get_package_dir("toolchain-timsp432"),"arm","include"),
        join(platform.get_package_dir("toolchain-timsp432"),"arm","include","CMSIS"),
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries"),
    ]
)

#
# Target: Build Core Library
#

libs = []

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkEnergia"),
    join(FRAMEWORK_DIR, "cores", board.get("build.core")),
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "ti_drivers"),
    join(FRAMEWORK_DIR, "system","source","ti","drivers"),
))

env.Append(LIBS=libs)