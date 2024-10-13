import sys, os, random, math
from enum import Enum
from typing import Any, NoReturn, Union

ERRORS = {
    "InsufficientArguments": "You haven't provided enough arguments for the program to run. You need to provide a filename.",
    "ErrorDuringError": "An unexpected error has happend, please contact the developer of the language.",
    "InvalidExtension": "The file you provided as a script to run needs to have an extension .tost",
    "InvalidArgument": "Argument \"~\" doesn't start with - or --, therefore isn't valid.",
    "UnknownArgument": "Argument \"~\" isn't known to the T* interpreter.",
    "FileNotReal": "File with the name \"~\" that you have provided doesn't exist (can't be found).",
    "FileReadError": "File with the name \"~\" can't be read, this might be caused by permission errors.",
    "LineNoMIO": "~th line contains no MIO, therefore the line isn't valid.",
    "LineManyMIOs": "~th line contains more than one MIO, therefore the line isn't valid.",
    "LineNoLeft": "In ~th line the left side couldn't be identified, which renders it invalid.",
    "LineNoRight": "In ~th line the right side couldn't be identified, which renders it invalid.",
    "LineUndefMIO": "~th line is not valid, please check it - maybe you made a typo?",
    "LineWeirdOperator": "~th line contains an invalid operator on the sides of the line. Maybe you made a typo?",
    "LineUntermStr": "~th line contains an unterminated string literal. Please close it ^_^",
    "TooManyOperators": "~th line is invalid, because one of it's sides contains more than one operator.",
    "VarNotExist": "Variable with the name \"~\" doesn't exist.",
    "VarAlreadyExist": "Variable with the name \"~\" already exists.",
    "CantSetRES": "Variable with the name \"$res\" is already reserved, so it's value can't be changed.",
    "FuncNotExist": "Function with the name \"~\" doesn't exist, thus can't be executed in any way.",
    "ArgNotValue": "While function with the name \"~\" was being executed an argument was passed that isn't a Value.",
    "WrongArgumentFunction": "The argument that was provided to the function \"~\" should've been a different type.",
    "WrongValueCreation": "During the creation of a Value instance, the Value Type didn't match the \"val\" type.",
    "WrongVarCreation": "During the creation of a Variable with the name \"~\" an error happend: the value isn't an instance of Value.",
    "InvalidValueSetvar": "What has been provided to \"Set Var\" is not a Value instance.",
    "InvalidValueCreatevar": "What has been provided to \"Create Var\" is not a Value instance.",
    "FunctionBadReturn": "The function with the name \"~\" returned a bad value, so it can't be converted into a Value instance.",
    "ParseUnknownIdentifier": "On line ~ there has been encountered an identifier that can't be parsed.",
    "NeedThreeElements": "An operator isn't \"finished\" - there is a value on the left side of it but not a single thing on the right.",
    "FaultVITOS": "Are you sure you have something on the left side of a certain operator? You might've made a typo.",
    "KeyboardInterrupt": "Keyboard Interrupt occured.",
    "InvalidGoto": "You can't go to line ~ as it doesn't exist in this file.",
    "EmptyLineWarn": "This file contains an empty line, which is not recommend during coding in T*, as an empty line isn't treated as an actual instruction one, which leads to goto's not working properly (being behind). To supress warnings, use -N application argument."
}

OPERATOR_ABLE = "=+-/*%><."
VALID_OPERATOR_COMBINATIONS = [
    "==", ">=", "<=", "-", "+", "/", "*", "%", ">", "<", "..", "."
]

VALID_ARGS = ["-N", "-nowarns"]
ARG_EXECUTABLES = {
    "-N": "global should_warn; should_warn = False",
    "-nowarns": "global should_warn; should_warn = False",
} # These should go in format of "-V": "something = 4" (this will be executed via exec() globally)

should_warn: bool = True

class ErrorType(Enum):
    BASIC = 0
    INTERNAL = 1
    WARN = 2

class MioType(Enum):
    ASSIGN = 0
    CALL = 1

class TokenType(Enum):
    STRING = 0
    IDENTIFIER = 1
    OPERATOR = 2

class OperatorType(Enum):
    ADD = 0
    SUB = 1
    DIVIDE = 2
    MULTIPLY = 3
    MODULUS = 4
    EQUALS = 5
    GREATER_THAN = 6
    LESS_THAN = 7
    EQUALS_OR_GREATHER_THAN = 7
    EQUALS_OR_LESS_THAN = 8
    DOT = 9
    DUBLEDOT = 10
    EQUALITY = 11

class ValueType(Enum):
    NUMBER = 0
    STRING = 1

class Token:
    def __init__(self, tkn_t: TokenType, tkn_v) -> None:
        self.t = tkn_t
        self.v = tkn_v

class TokenizedLine:
    def __init__(self, left: list[Token], right: list[Token], mio_type: MioType) -> None:
        self.left = left
        self.right = right
        self.mio_type = mio_type

class Value:
    def __init__(self, type: ValueType, val) -> None:
        if type is ValueType.NUMBER and not isinstance(val, int):
            error("WrongValueCreation", ErrorType.INTERNAL)
        if type is ValueType.STRING and not isinstance(val, str):
            error("WrongValueCreation", ErrorType.INTERNAL)
        self.tp = type
        self.val = val

class TokenizedLineAdv:
    def __init__(self, left, right, mio_type: MioType) -> None:
        self.left = left
        self.right = right
        self.mio_type = mio_type

class Variable:
    def __init__(self, name: str, value: Value) -> None:
        if not isinstance(value, Value):
            error("WrongVarCreation", ErrorType.INTERNAL, name)
        self._name = name
        self._value = value

    def set_val(self, value: Value) -> None:
        self._value = value

    @property
    def val(self):
        return self._value

    @property
    def name(self):
        return self._name

class Variables:
    def __init__(self) -> None:
        self._vars = [Variable(
            "$res", Value(ValueType.NUMBER, 0)
        )]

    def exists(self, req_name: str) -> bool:
        for var in self._vars:
            if var.name == req_name:
                return True
        return False

    def get_var(self, req_name: str) -> Variable:
        for var in self._vars:
            if var.name == req_name:
                return var

        error("VarNotExist", ErrorType.INTERNAL, req_name)

    def set_var(self, req_name: str, new_value: Value, bypass: bool = False) -> None:
        if not isinstance(new_value, Value):
            error("InvalidValueSetvar", ErrorType.INTERNAL)

        if not bypass:
            if req_name == "$res": error("CantSetRES", ErrorType.INTERNAL)

        for var in self._vars:
            if var.name == req_name:
                self._vars[self._vars.index(var)].set_val(new_value)
                return

        error("VarNotExist", ErrorType.INTERNAL, req_name)

    def create_var(self, new_name: str, new_value: Value) -> None:
        if not isinstance(new_value, Value):
            error("InvalidValueCreatevar", ErrorType.INTERNAL)

        for var in self._vars:
            if var.name == new_name:
                error("VarAlreadyExist", ErrorType.INTERNAL, new_name)

        self._vars.append(Variable(
            new_name,
            new_value
        ))

class Functions: # ALL OF T*'s FUNCTIONS ARE HERE ^_^
    def exec(self, func_name: str, argument: Value):
        if not isinstance(argument, Value):
            error("ArgNotValue", ErrorType.INTERNAL, func_name)

        if hasattr(self, f"{func_name}_STRING_RUN") and not hasattr(self, f"{func_name}_NUMBER_RUN"):
            if argument.tp == ValueType.STRING:
                self._frun(f"{func_name}_STRING_RUN", argument)
            else: error("WrongArgumentFunction", ErrorType.BASIC, func_name)
        elif hasattr(self, f"{func_name}_NUMBER_RUN") and not hasattr(self, f"{func_name}_STRING_RUN"):
            if argument.tp == ValueType.NUMBER:
                self._frun(f"{func_name}_NUMBER_RUN", argument)
            else: error("WrongArgumentFunction", ErrorType.BASIC, func_name)
        elif hasattr(self, f"{func_name}_NUMBER_RUN") and hasattr(self, f"{func_name}_STRING_RUN"):
            if argument.tp == ValueType.NUMBER:
                self._frun(f"{func_name}_NUMBER_RUN", argument)
            elif argument.tp == ValueType.STRING:
                self._frun(f"{func_name}_STRING_RUN", argument)
        else:
            error("FuncNotExist", ErrorType.INTERNAL, func_name)

    def _frun(self, function_name: str, argument) -> None:
        res = getattr(self, f"{function_name}")(argument)

        if isinstance(res, int):
            vrs.set_var("$res", Value(ValueType.NUMBER, res), True)
        elif isinstance(res, str):
            vrs.set_var("$res", Value(ValueType.STRING, res), True)
        else:
            if res is None: return
            else: error("FunctionBadReturn", ErrorType.INTERNAL, function_name)

    def exists(self, req_name: str) -> bool:
        if hasattr(self, f"{req_name}_STRING_RUN") or hasattr(self, f"{req_name}_NUMBER_RUN"):
            return True
        return False

    def PRINT_STRING_RUN(self, argument: Value):
        print(f"{argument.val}")

    def PRINT_NUMBER_RUN(self, argument: Value):
        print(f"{argument.val}")

    def GOTO_NUMBER_RUN(self, argument: Value):
        global j, lines
        if not lines.get(argument.val): error("InvalidGoto", ErrorType.BASIC, str(argument.val)) # pyright: ignore
        j = argument.val - 2  # pyright: ignore

    def RUNIF_NUMBER_RUN(self, argument: Value):
        global j
        if argument.val == 0: j += 1
        return int(argument.val == 1)

    def NOT_NUMBER_RUN(self, argument: Value):
        if argument.val == 0: return 1
        else: return 0

    def UPPERCASE_STRING_RUN(self, argument: Value):
        return argument.val.upper() # pyright: ignore

    def LOWERCASE_STRING_RUN(self, argument: Value):
        return argument.val.lower() # pyright: ignore

    def RANDOMCASE_STRING_RUN(self, argument: Value):
        ret = ""
        for char in argument.val: # pyright: ignore
            rand = random.randint(0, 1)
            if rand == 0: ret += char.upper()
            else: ret += char.lower()
        return ret

    def STRIP_STRING_RUN(self, argument: Value):
        return argument.val.strip() # pyright: ignore

    def NOSPACES_STRING_RUN(self, argument: Value):
        return argument.val.replace(' ', '') # pyright: ignore

    def STARTSWITH_STRING_RUN(self, argument: Value):
        res = vrs.get_var("$res").val.val
        if res.startswith(argument.val): # pyright: ignore
            return 1
        return 0

    def ENDSWITH_STRING_RUN(self, argument: Value):
        res = vrs.get_var("$res").val.val
        if res.endswith(argument.val): # pyright: ignore
            return 1
        return 0

    def LENGTH_STRING_RUN(self, argument: Value):
        return len(argument.val) # pyright: ignore

    def LENGTH_NUMBER_RUN(self, argument: Value):
        return len(str(argument.val))

    def COUNTUP_STRING_RUN(self, argument: Value):
        times = 0
        for j in str(vrs.get_var("$res").val.val): # pyright: ignore
            if j == argument.val: times += 1
        return times

    def ISSTRING_NUMBER_RUN(self, argument: Value):
        return 0

    def ISSTRING_STRING_RUN(self, argument: Value):
        return 1

    def ISNUMBER_NUMBER_RUN(self, argument: Value):
        return 1

    def ISNUMBER_STRING_RUN(self, argument: Value):
        return 0

    def EMPOWER_NUMBER_RUN(self, argument: Value):
        res = vrs.get_var("$res").val.val
        if not isinstance(res, int): return -1
        else:
            return int(res ** argument.val) # pyright: ignore

    def ENROOT_NUMBER_RUN(self, argument: Value):
        res = vrs.get_var("$res").val.val
        if not isinstance(res, int): return -1
        else:
            return int(res ** (1 / argument.val)) # pyright: ignore

    def STORE_STRING_RUN(self, argument: Value):
        return argument.val

    def STORE_NUMBER_RUN(self, argument: Value):
        return argument.val

def ord_sum(wstr) -> int:
    ret = 0
    for j in wstr:
        ret += ord(j)
    return ret

def strXstr(str1, str2) -> str:
    ret = ""
    for j in str1:
        for i in str2:
            ret += j + i
    return ret

class Operators:
    @staticmethod
    def operate(operator: OperatorType, v1: Value, v2: Value):
        match operator:
            case OperatorType.ADD:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." + 0
                    return Value(
                        ValueType.STRING,
                        f"{v1.val}{v2.val}"
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." + "..."
                    return Value(
                        ValueType.STRING,
                        f"{v1.val}{v2.val}"
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 + "..."
                    try:
                        return Value(
                            ValueType.NUMBER,
                            int(v1.val) + int(v2.val)
                        )
                    except:
                        return Value(
                            ValueType.NUMBER,
                            -1
                        )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 + 0
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) + int(v2.val)
                    )
            case OperatorType.SUB:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." - 0
                    return Value(
                        ValueType.NUMBER,
                        ord_sum(v1.val) - int(v2.val)
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." - "..."
                    return Value(
                        ValueType.NUMBER,
                        ord_sum(v1.val) - ord_sum(v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 - "..."
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) - ord_sum(v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 - 0
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) - int(v2.val)
                    )
            case OperatorType.DIVIDE:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." / 0
                    return Value(
                        ValueType.NUMBER,
                        ord_sum(v1.val) // int(v2.val)
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." / "..."
                    return Value(
                        ValueType.NUMBER,
                        ord_sum(v1.val) // ord_sum(v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 / "..."
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) // ord_sum(v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 / 0
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) // int(v2.val)
                    )
            case OperatorType.MULTIPLY:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." * 0
                    return Value(
                        ValueType.STRING,
                        str(v1.val) * int(v2.val)
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." * "..."
                    return Value(
                        ValueType.STRING,
                        strXstr(v1.val, v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 * "..."
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) * ord_sum(v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 * 0
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) * int(v2.val)
                    )
            case OperatorType.MODULUS:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." % 0
                    return Value(
                        ValueType.NUMBER,
                        ord_sum(v1.val) % int(v2.val)
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." % "..."
                    return Value(
                        ValueType.NUMBER,
                        ord_sum(v1.val) % ord_sum(v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 % "..."
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) % ord_sum(v2.val)
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 % 0
                    return Value(
                        ValueType.NUMBER,
                        int(v1.val) % int(v2.val)
                    )
            case OperatorType.EQUALS:
                return Value( # ANY == ANY
                    ValueType.NUMBER,
                    int((v1.tp == v2.tp) and (v1.val == v2.val))
                )
            case OperatorType.GREATER_THAN:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." > 0
                    return Value(
                        ValueType.NUMBER,
                        int(ord_sum(v1.val) > int(v2.val))
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." > "..."
                    return Value(
                        ValueType.NUMBER,
                        int(ord_sum(v1.val) > ord_sum(v2.val))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 > "..."
                    return Value(
                        ValueType.NUMBER,
                        int(int(v1.val) > ord_sum(v2.val))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 > 0
                    return Value(
                        ValueType.NUMBER,
                        int(int(v1.val) > int(v2.val))
                    )
            case OperatorType.LESS_THAN:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." < 0
                    return Value(
                        ValueType.NUMBER,
                        int(ord_sum(v1.val) < int(v2.val))
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." < "..."
                    return Value(
                        ValueType.NUMBER,
                        int(ord_sum(v1.val) < ord_sum(v2.val))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 < "..."
                    return Value(
                        ValueType.NUMBER,
                        int(int(v1.val) < ord_sum(v2.val))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 < 0
                    return Value(
                        ValueType.NUMBER,
                        int(int(v1.val) < int(v2.val))
                    )
            case OperatorType.EQUALS_OR_GREATHER_THAN:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." >= 0
                    return Value(
                        ValueType.NUMBER,
                        int((ord_sum(v1.val) == int(v2.val)) or (ord_sum(v1.val) > int(v2.val)))
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." >= "..."
                    return Value(
                        ValueType.NUMBER,
                        int((ord_sum(v1.val) == ord_sum(v2.val)) or (ord_sum(v1.val) > ord_sum(v2.val)))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 >= "..."
                    return Value(
                        ValueType.NUMBER,
                        int((int(v1.val) == ord_sum(v2.val)) or (int(v1.val) > ord_sum(v2.val)))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 >= 0
                    return Value(
                        ValueType.NUMBER,
                        int((int(v1.val) == int(v2.val)) or (int(v1.val) > int(v2.val)))
                    )
            case OperatorType.EQUALS_OR_LESS_THAN:
                if v1.tp is ValueType.STRING and v2.tp is ValueType.NUMBER: # "..." <= 0
                    return Value(
                        ValueType.NUMBER,
                        int((ord_sum(v1.val) == int(v2.val)) or (ord_sum(v1.val) < int(v2.val)))
                    )
                elif v1.tp is ValueType.STRING and v2.tp is ValueType.STRING: # "..." <= "..."
                    return Value(
                        ValueType.NUMBER,
                        int((ord_sum(v1.val) == ord_sum(v2.val)) or (ord_sum(v1.val) < ord_sum(v2.val)))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.STRING: # 0 <= "..."
                    return Value(
                        ValueType.NUMBER,
                        int((int(v1.val) == ord_sum(v2.val)) or (int(v1.val) < ord_sum(v2.val)))
                    )
                elif v1.tp is ValueType.NUMBER and v2.tp is ValueType.NUMBER: # 0 <= 0
                    return Value(
                        ValueType.NUMBER,
                        int((int(v1.val) == int(v2.val)) or (int(v1.val) < int(v2.val)))
                    )
            case OperatorType.DOT:
                return Operators.operate(random.choice(
                    [OperatorType.ADD, OperatorType.SUB, OperatorType.DIVIDE, OperatorType.MULTIPLY, OperatorType.MODULUS, OperatorType.EQUALS, OperatorType.GREATER_THAN, OperatorType.LESS_THAN, OperatorType.EQUALS_OR_GREATHER_THAN, OperatorType.EQUALS_OR_LESS_THAN, OperatorType.EQUALITY, OperatorType.DUBLEDOT]
                ), v1, v2)
            case OperatorType.DUBLEDOT:
                rv = random.randint(0,1) # ANY .. ANY or ANY ANY
                if rv == 0: return v1
                else: return v2
            case OperatorType.EQUALITY:
                return Value( # ANY = ANY
                    ValueType.NUMBER,
                    int(str(v1.val) == str(v2.val))
                )

def error(id: str, etype: ErrorType, arg: Any = None) -> NoReturn: # pyright: ignore
    match etype:
        case ErrorType.BASIC:
            try: print(f"[ERR]\t{id}\t{ERRORS[id].replace('~', arg) if '~' in ERRORS[id] else ERRORS[id]}")
            except: error("ErrorDuringError", ErrorType.BASIC)
            print(f"[ERR]\tExiting ...")
            sys.exit(-1)

        case ErrorType.INTERNAL:
            try: print(f"[INT]\t{id}\t{ERRORS[id].replace('~', arg) if '~' in ERRORS[id] else ERRORS[id]}")
            except: error("ErrorDuringError", ErrorType.BASIC)
            print(f"[INT]\tExiting ...")
            sys.exit(-1)

        case ErrorType.WARN:
            if should_warn:
                try: print(f"[WRN]\t{id}\t{ERRORS[id].replace('~', arg) if '~' in ERRORS[id] else ERRORS[id]}\n")
                except: error("ErrorDuringError", ErrorType.BASIC)

        case _:
            print('Some mind-boggling antigrav happend; Exiting...')
            sys.exit(-1)

def check_arguments(args: list[str]) -> Union[str, NoReturn]:
    if len(args) == 0:
        error("InsufficientArguments", ErrorType.BASIC)
    elif len(args) == 1:
        if not args[0].endswith(".tost"):
            error("InvalidExtension", ErrorType.BASIC)
        return args[0]
    else:
        if not args[0].endswith(".tost"):
            error("InvalidExtension", ErrorType.BASIC)
        file_name: str = args.pop(0)
        for arg in args:
            if not arg.startswith('-'):
                error("InvalidArgument", ErrorType.BASIC, arg)
            if arg not in VALID_ARGS:
                error("UnknownArgument", ErrorType.BASIC, arg)
            exec(ARG_EXECUTABLES[arg])
        return file_name

def check_file(name: str) -> Union[None, NoReturn]:
    if not os.path.exists(name):
        error("FileNotReal", ErrorType.BASIC, name)

def get_lines(script: str) -> list[str]:
    lines: list[str] = []
    cur_line: str = ""
    j = 0
    while j < len(script):
        if script[j] == "\n":
            lines.append(cur_line)
            cur_line = ""
        else:
            cur_line += script[j]
        j += 1

    if cur_line:
        lines.append(cur_line)
    return lines

def no_comment(right: str) -> str:
    j = 0
    while j < len(right):
        char = right[j]
        unsafe = False
        if (j + 1 == len(right)) or (j == 0): unsafe = True

        if not unsafe:
            if (char == '/') and (right[j+1] == '/'):
                return right[:j-1]

        j += 1
    return right

def split_via_mio(line: str, line_num: int) -> list:
    left = ""
    right = ""
    mio = None
    lexing_string = False
    done = False
    then_j = 0
    j = 0
    while j < len(line):
        char = line[j]
        unsafe = False
        if (j + 1 == len(line)) or (j == 0): unsafe = True

        if lexing_string:
            if char == '"':
                lexing_string = False
        else:
            if not unsafe:
                if (char == '/') and (line[j+1] == '/'):
                    if not done:
                        error("LineNoMIO", ErrorType.BASIC, str(line_num))
                    return [left, no_comment(right), mio]

            if char == '"':
                lexing_string = True
            else:
                if not unsafe:
                    if ((char == '-') or (char == '=')) and (line[j+1] == '>'):
                        if done:
                            error("LineManyMIOs", ErrorType.BASIC, str(line_num))
                        done = True
                        left = line[0:j].strip()
                        right = line[j+2:].strip()
                        if char == '-': mio = MioType.CALL
                        else: mio = MioType.ASSIGN
                        then_j = j

        j += 1

    return [left, right, mio]

def lex_side(side: str, cur_line: int) -> list[Token]:
    side_tokens: list[Token] = []

    lexing_string = False
    lexing_id = False

    current_str = ""
    current_id = ""

    j = 0
    while j < len(side):
        char = side[j]

        unsafe = False
        if (j + 1 == len(side)) or (j == 0): unsafe = True
        unsafe_start = False
        if (j + 1 == len(side)): unsafe_start = True

        if lexing_string:
            if char == '"':
                lexing_string = False
                side_tokens.append(Token(
                    TokenType.STRING,
                    current_str
                ))
                current_str = ""
            else:
                current_str += char
        else:
            if char == '"':
                if current_id:
                    side_tokens.append(Token(
                        TokenType.IDENTIFIER,
                        current_id
                    ))
                    current_id = ""
                lexing_string = True
            elif char in OPERATOR_ABLE:
                if not unsafe_start:
                    if current_id:
                        side_tokens.append(Token(
                            TokenType.IDENTIFIER,
                            current_id
                        ))
                        current_id = ""
                    if side[j+1] in OPERATOR_ABLE:
                        if (char+side[j+1]) in VALID_OPERATOR_COMBINATIONS:
                            side_tokens.append(Token(
                                TokenType.OPERATOR,
                                (char+side[j+1])
                            ))
                            j += 2
                            continue
                        else:
                            side_tokens.append(Token(
                                TokenType.OPERATOR,
                                char
                            ))
                    else:
                        side_tokens.append(Token(
                            TokenType.OPERATOR,
                            char
                        ))
                else:
                    print(unsafe, unsafe_start, j, len(side))
                    error("LineWeirdOperator", ErrorType.BASIC, str(cur_line))
            else:
                if char != ' ':
                    current_id += char
                else:
                    if current_id:
                        side_tokens.append(Token(
                            TokenType.IDENTIFIER,
                            current_id
                        ))
                        current_id = ""

        j += 1

    if current_id:
        side_tokens.append(Token(
            TokenType.IDENTIFIER,
            current_id
        ))

    if current_str:
        error("LineUntermStr", ErrorType.BASIC, str(cur_line))

    op_tkn_met = False
    for tkn in side_tokens:
        if tkn.t == TokenType.OPERATOR:
            if op_tkn_met:
                error("TooManyOperators", ErrorType.BASIC, str(cur_line))
            else:
                op_tkn_met = True

    return side_tokens

def lex(script: str):
    loc = get_lines(script)
    tokens = []
    j = 0
    empty_line_warned = False
    while j < len(loc):
        line = loc[j]

        if not(('->' in line) or ('=>' in line)):
            if not line.strip() == "":
                error("LineNoMIO", ErrorType.BASIC, str(j+1))
            else:
                if not empty_line_warned:
                    error("EmptyLineWarn", ErrorType.WARN)
                    empty_line_warned = True
                j += 1
                continue

        line_tkn = split_via_mio(line, j+1)
        if line_tkn[0] == '':
            error("LineNoLeft", ErrorType.BASIC, str(j+1))
        if line_tkn[1] == '':
            error("LineNoRight", ErrorType.BASIC, str(j+1))
        if line_tkn[2] is None:
            error("LineUndefMIO", ErrorType.BASIC, str(j+1))

        tokens.append(TokenizedLine(
            lex_side(line_tkn[0], j+1),
            lex_side(line_tkn[1], j+1),
            line_tkn[2]
        ))

        j += 1

    return tokens

OTV_TO_OPERATOR_TYPE = {
    "==": OperatorType.EQUALS,
    ">=": OperatorType.EQUALS_OR_GREATHER_THAN,
    "<=": OperatorType.EQUALS_OR_LESS_THAN,
    "-": OperatorType.SUB,
    "+": OperatorType.ADD,
    "/": OperatorType.DIVIDE,
    "*": OperatorType.MULTIPLY,
    "%": OperatorType.MODULUS,
    ">": OperatorType.GREATER_THAN,
    "<": OperatorType.LESS_THAN,
    "..": OperatorType.DUBLEDOT,
    ".": OperatorType.DOT,
    "=": OperatorType.EQUALITY
}

def work_on_vitos(values: list) -> Value:
    if len(values) == 1:
        return values[0]

    to_ret: list = []

    if isinstance(values[0], Value) and isinstance(values[1], Token):
        if len(values) < 3: error("NeedThreeElements", ErrorType.BASIC)
        to_ret.append(Operators.operate(OTV_TO_OPERATOR_TYPE[values[1].v], values[0], values[2]))
        to_ret.extend(values[3:])
    elif isinstance(values[0], Value) and isinstance(values[1], Value):
        to_ret.append(Operators.operate(OperatorType.DUBLEDOT, values[0], values[1]))
        to_ret.extend(values[2:])
    elif isinstance(values[0], Token) and isinstance(values[1], Value) and values[0].v == "-" and values[1].tp is ValueType.NUMBER:
        to_ret.append(Operators.operate(OperatorType.SUB, Value(ValueType.NUMBER, 0), values[1]))
        to_ret.extend(values[2:])
    else:
        error("FaultVITOS", ErrorType.INTERNAL)

    return work_on_vitos(to_ret)

def parse(tokens) -> None:
    global lines, vrs, funcs, j, cl
    lines = dict(enumerate(tokens, 1))
    vrs = Variables()
    funcs = Functions()
    j = 0
    cl = None

    while j < len(lines):
        cl = lines[j+1]
        rmcl = TokenizedLineAdv([], [], cl.mio_type)
        for lt in cl.left:
            if lt.t == TokenType.STRING:
                rmcl.left.append(Value(ValueType.STRING, lt.v))
            elif lt.t == TokenType.IDENTIFIER:
                if lt.v == "$res" and vrs.exists(vrs.get_var("$res").val.val): # pyright: ignore
                    rmcl.left.append(vrs.get_var(vrs.get_var("$res").val.val).val) # pyright: ignore
                elif vrs.exists(lt.v):
                    rmcl.left.append(vrs.get_var(lt.v).val)
                else:
                    try: rmcl.left.append(Value(ValueType.NUMBER, int(lt.v)))
                    except Exception as e:
                        error("ParseUnknownIdentifier", ErrorType.BASIC, str(j+1))
            else:
                rmcl.left.append(lt)
        if (len(cl.right) == 1):
            if cl.right[0].t is TokenType.IDENTIFIER:
                rmcl.right = Value(ValueType.STRING, cl.right[0].v)
            else:
                for rt in cl.right:
                    if rt.t == TokenType.STRING:
                        rmcl.right.append(Value(ValueType.STRING, rt.v))
                    elif rt.t == TokenType.IDENTIFIER:
                        if vrs.exists(rt.v):
                            rmcl.right.append(vrs.get_var(rt.v).val)
                        else:
                            try: rmcl.right.append(Value(ValueType.NUMBER, int(rt.v)))
                            except Exception as e:
                                error("ParseUnknownIdentifier", ErrorType.BASIC, str(j+1))
                    else:
                        rmcl.right.append(rt)
                rmcl.right = work_on_vitos(rmcl.right)
        else:
            for rt in cl.right:
                if rt.t == TokenType.STRING:
                    rmcl.right.append(Value(ValueType.STRING, rt.v))
                elif rt.t == TokenType.IDENTIFIER:
                    if vrs.exists(rt.v):
                        rmcl.right.append(vrs.get_var(rt.v).val)
                    else:
                        try: rmcl.right.append(Value(ValueType.NUMBER, int(rt.v)))
                        except Exception as e:
                            error("ParseUnknownIdentifier", ErrorType.BASIC, str(j+1))
                else:
                    rmcl.right.append(rt)
            rmcl.right = work_on_vitos(rmcl.right)
        rmcl.left = work_on_vitos(rmcl.left)

        if rmcl.mio_type is MioType.ASSIGN:
            if vrs.exists(str(rmcl.right.val)):
                vrs.set_var(str(rmcl.right.val), rmcl.left)
            else:
                vrs.create_var(str(rmcl.right.val), rmcl.left)
            funcs.exec("STORE", Value(ValueType.STRING, str(rmcl.right.val)))
        else: # MioType.CALL
            funcs.exec(str(rmcl.right.val).upper(), rmcl.left)

        j += 1

def run() -> None:
    arguments: list[str] = sys.argv
    arguments.pop(0)
    file_name: str = check_arguments(arguments)
    check_file(file_name)
    script: str = ""
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            script = f.read()
    except:
        error("FileReadError", ErrorType.BASIC, file_name)

    parse(lex(script))

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        error("KeyboardInterrupt", ErrorType.BASIC)
