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

env.Replace(
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    GDB="arm-none-eabi-gdb",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",
    LINK="$CXX",

    ARFLAGS=["rcPs"],

    PIODEBUGFLAGS=["-Os", "-g3", "-ggdb", "-gdwarf-2"],

    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.vectors)\s+([0-9]+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    UPLOADER="gdb_agent_console",
    UPLOADERFLAGS=[
        "xds110_msp432_swd.dat"
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS "prog $SOURCES"',

    PROGSUFFIX=".elf"
)

env.Append(
    ASFLAGS=["-x","assembler-with-cpp"],

    CCFLAGS=[
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-mthumb-interwork",
        "-nostdlib",
    ],

    CFLAGS=[
        #"-I platform.get_package_dir(toolchain-timsp432)/arm_compiler/arm-none-eabi/include",
        "-std=gnu11"
    ],

    CXXFLAGS=[
        #"-I platform.get_package_dir(toolchain-timsp432)/arm_compiler/arm-none-eabi/include/c++/9.2.0",
        "-fno-threadsafe-statics",
        "-fno-rtti",
        "-fno-exceptions",
        "-std=gnu++11"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        "xdc_target_types__=gnu/targets/arm/std.h", 
        "xdc_target_name__=M4F", 
        "xdc_cfg__xheader__=configPkg/package/cfg/energia_pm4fg.h", 
        "xdc__nolocalstring=1",
    ],

    LINKFLAGS=[
        "-Os",
        "-mthumb-interwork",
    ],

    LIBS=["c","stdc++","gcc","m"],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        ),

        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET",
            ]), "Building $TARGET"),
            suffix=".hex"
        ),
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
