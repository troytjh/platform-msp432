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
    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Os",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-mcpu=cortex-m4",
        "-mthumb",
        #"-mfloat-abi=hard",
        "-mfpu=fpv4-sp-d16",
        "-mabi=aapcs",
        "-lm"
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-fno-threadsafe-statics"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU")
    ],

    LIBPATH=[
        join(platform.get_package_dir("toolchain-timsp432"),"arm","include"),
        #join(platform.get_package_dir("toolchain-timsp432"), "arm_compiler","arm-none-eabi","lib"),
    ],

    LINKFLAGS=[
        "-Os",
        "-mcpu=cortex-m4",
        "-mthumb",
        "--specs=nosys.specs",
        #"-L{build.system.path}/kernel/tirtos/packages/gnu/targets/arm/libs/install-native/arm-none-eabi/lib/thumb/v7e-m/fpv4-sp/hard" "-L{build.path}" "-L{build.core.path}" "-L{build.system.path}/energia" "-L{build.system.path}/kernel" "-L{build.system.path}/source" "-L{build.system.path}/kernel/tirtos/builds/{build.variant}/energia/" "-L{build.system.path}/kernel/tirtos/packages",
        #"-Wl,-Tmsp432p401r.lds,-gc-sections,-u,main"
        "-Wl,-u,main",
        "-L{build.core.path}/ti/runtime/wiring/msp432",
        "-L{build.core.path}/ti/runtime/wiring/msp432/variants/MSP_EXP432P401R",
        "-Wl,--check-sections",
        "-Wl,--gc-sections",
        "-Wl,-Tmsp432p401r.lds {build.system.path}/source/ti/devices/msp432p4xx/driverlib/gcc/msp432p4xx_driverlib.a",
        "-Wl,--start-group", 
        "-lstdc++", 
        "-lgcc", 
        "-lm", 
        "-lnosys", 
        "-lc", 
        "-Wl,--end-group"
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
                "$TARGET",
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