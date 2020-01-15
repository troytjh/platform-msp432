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

    CCFLAGS=[
        "-march=armv7e-m+fp",
        "-mfloat-abi=hard", 
        "-mfpu=fpv4-sp-d16", 
        "-mabi=aapcs",
    ],

    LINKFLAGS=[
        "-T msp432p401r.lds",
        "-Wl,--check-sections",
        "-Wl,--gc-sections",
        "-Wl,--unresolved-symbols=report-all",
        "-Wl,--warn-common",
        #"-Wl,--warn-section-align",
        "-Wl,--start-group", 
        "-lstdc++","-lm","-lgcc","-lc", 
        "-Wl,--end-group",
        "-march=armv7e-m+fp",
        "-mfloat-abi=hard", 
        "-mfpu=fpv4-sp-d16", 
        #"-fsingle-precision-constant",
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", env.BoardConfig().get("build.core")),
        join(variants_dir, board.get("build.variant")),
        join(platform.get_package_dir("toolchain-timsp432"),"arm-none-eabi","include"),
        join(FRAMEWORK_DIR,"system","source"),
        join(FRAMEWORK_DIR,"system","source","energia"),
        join(FRAMEWORK_DIR,"system","source","third_party","CMSIS","Include"),
        join(FRAMEWORK_DIR,"system","source","ti","drivers"),
        join(FRAMEWORK_DIR,"system","source","ti","devices","msp432p4xx"),
        join(FRAMEWORK_DIR,"system","source","ti","devices","msp432p4xx","inc"),
        join(FRAMEWORK_DIR,"system","source","ti","devices","msp432p4xx","inc","CMSIS"),
        join(FRAMEWORK_DIR,"system","source","ti","devices","msp432p4xx","driverlib"),
        join(FRAMEWORK_DIR,"system","kernel","tirtos"),
        join(FRAMEWORK_DIR,"system","kernel","tirtos","packages"),

    ],

    LIBPATH=[
        join(FRAMEWORK_DIR,"system","source","ti","devices","msp432p4xx","linker_files","gcc"),
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries"),
    ],
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
    join("$BUILD_DIR","msp432p4xx_driverlib"),
    join(FRAMEWORK_DIR,"system","source","ti","devices","msp432p4xx","driverlib"),
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR","newlib"),
    join(platform.get_package_dir("toolchain-timsp432"),"lib","newlib"),
))

env.Append(LIBS=libs)