import sys
from os.path import join
from platform import system

from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default,
                          DefaultEnvironment)

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-energiamsp432r")

board = env.BoardConfig()

variants_dir = join(
    "$PROJECT_DIR", board.get("build.variants_dir")) if board.get(
        "build.variants_dir", "") else join(FRAMEWORK_DIR, "variants")

CC=join(platform.get_package_dir("toolchain-timsp432"), "lib", "gcc","msp432","8.2.1")
print("CC")

env.Replace(
    AR="msp432-ar",
    AS="msp432-as",
    CC="msp432-gcc",
    CXX="msp432-g++",
    GDB="msp432-gdb",
    OBJCOPY="msp432-objcopy",
    RANLIB="msp432-ranlib",
    SIZETOOL="msp432-size",
    LINK="$CC",

    ARFLAGS=["rc"],

    PIODEBUGFLAGS=["-O0", "-g3", "-ggdb", "-gdwarf-2"],

    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.vectors)\s+([0-9]+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    UPLOADER="mspdebug",
    UPLOADERFLAGS=[
        "$UPLOAD_PROTOCOL" if system() != "Windows" else "tilib",
        "--force-reset"
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS "prog $SOURCES"',

    PROGSUFFIX=".elf"
)

env.Append(
    print("$CC"),
    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Os",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        #"-mmcu=$BOARD_MCU"
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-fno-threadsafe-statics"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", env.BoardConfig().get("build.core")),
        join(variants_dir, board.get("build.variant")),
        join(platform.get_package_dir("toolchain-timsp432"),"arm","src"),
        join(platform.get_package_dir("toolchain-timsp432"), "lib", "gcc","msp432","8.2.1"),
        join(platform.get_package_dir("toolchain-timsp432"), "msp432", "include"),
        join(platform.get_package_dir("toolchain-timsp432"),"lib","gcc","msp432","8.2.1","include"),
        join(platform.get_package_dir("toolchain-timsp432"),"arm","include"),
        #join(FRAMEWORK_DIR, "cores", board.get("build.core"),"xdc","runtime"),
        #join(FRAMEWORK_DIR, "cores", board.get("build.core"),"xdc","runtime","package"),
        #join(FRAMEWORK_DIR, "cores", board.get("build.core"),"xdc","runtime","package","internal"),
        #join(FRAMEWORK_DIR, "cores", board.get("build.core"),"xdc","runtime","knl"),
        #join(FRAMEWORK_DIR, "cores", board.get("build.core"),"xdc","runtime","knl","package"),
        #join(FRAMEWORK_DIR, "cores", board.get("build.core"),"xdc","runtime","knl","package","internal"),
        #join(FRAMEWORK_DIR,"system","kernel","tirtos","packages","gnu","targets","arm"),
        #join(FRAMEWORK_DIR,"system","kernel","tirtos","packages","ti"),
        #join(FRAMEWORK_DIR,"system","source")
    ],

    LINKFLAGS=[
        "-Os",
        #"-mmcu=$BOARD_MCU",
        "-Wl,-gc-sections,-u,main"
    ],

    LIBS=["m"],

    BUILDERS=dict(
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        )
    )
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])


# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

if "energia" in env.get("PIOFRAMEWORK", []):
    sys.stderr.write(
        "WARNING!!! Using of `framework = energia` in `platformio.ini` is "
        "deprecated. Please replace with `framework = arduino`.\n")
    env.Replace(PIOFRAMEWORK=["arduino"])

#
# Target: Build executable and linkable firmware
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.hex")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToHex(join("$BUILD_DIR", "${PROGNAME}"), target_elf)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload firmware
#

upload_target = target_firm
if env.subst("$UPLOAD_PROTOCOL") == "dslite":
    env.Replace(
        UPLOADER=join(env.PioPlatform().get_package_dir(
            "tool-dslite") or "", "DebugServer", "bin", "DSLite"),
        UPLOADERFLAGS=[
            "load", "-c",
            join(env.PioPlatform().get_package_dir("tool-dslite") or "",
                 "%s.ccxml" % env.BoardConfig().get("build.variant")), "-f"
        ],
        UPLOADCMD="$UPLOADER $UPLOADERFLAGS $SOURCES"
    )
    upload_target = target_elf
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

target_upload = env.Alias("upload", upload_target,
                          env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE"))
AlwaysBuild(target_upload)

#
# Default targets
#

Default([target_buildprog, target_size])