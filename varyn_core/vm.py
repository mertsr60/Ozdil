# -*- coding: utf-8 -*-
import math
import random
import time
import sys

from .bytecode import Bytecode
from .environment import Environment
from .errors import VarynError, ReturnException, InputRequestException
from .runtime_types import (
    wrap_value, OzValue, OzNull, OzBool, OzInt, OzFloat, OzString,
    OzList, OzMap, OzFunction, OzClass, OzBoundMethod, OzNativeCallable, OzInstance
)
from .object_model import get_attribute

def check_exception_match(exc, operand):
    if operand in ("Hata", "Error", "Exception", "Hepsi", "", None):
        return True
    friendly_type = getattr(exc, "friendly_type", "")
    exc_msg = str(exc)
    exc_class_name = type(exc).__name__
    operand_norm = operand.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    if operand_norm in ("turhatasi", "typeerror"):
        return "tür hatası" in friendly_type.lower() or exc_class_name == "TypeError" or "typeerror" in friendly_type.lower()
    if operand_norm in ("degerhatasi", "valueerror"):
        return "değer hatası" in friendly_type.lower() or exc_class_name == "ValueError" or "valueerror" in friendly_type.lower()
    if operand_norm in ("dizinhatasi", "indexerror"):
        return "dizin hatası" in friendly_type.lower() or exc_class_name == "IndexError" or "indexerror" in friendly_type.lower()
    if operand_norm in ("sifirabolmehatasi", "zerodivisionerror"):
        return "bölme" in friendly_type.lower() or "bölme" in exc_msg.lower() or exc_class_name == "ZeroDivisionError" or "zerodivision" in friendly_type.lower()
    if operand_norm in ("oznitelikhatasi", "attributeerror"):
        return "öznitelik" in friendly_type.lower() or exc_class_name == "AttributeError" or "attributeerror" in friendly_type.lower()
    if operand_norm in ("kutuphanehatasi", "importerror"):
        return "kütüphane" in friendly_type.lower() or exc_class_name == "ImportError" or "importerror" in friendly_type.lower()
    if operand_norm in ("dosyahatasi", "fileerror", "ioerror", "permissionerror", "filenotfounderror"):
        return "dosya" in friendly_type.lower() or exc_class_name in ("FileNotFoundError", "PermissionError", "OSError")
    if operand.lower() in exc_class_name.lower():
        return True
    if operand.lower() in friendly_type.lower():
        return True
    return False

class Frame:
    def __init__(self, bytecode, env, return_ip=0, prev_frame=None):
        self.bytecode = bytecode
        self.env = env
        self.ip = 0
        self.stack = []
        self.return_ip = return_ip
        self.prev_frame = prev_frame
        self.exception_handlers = []  # Stack of exception handler IPs
        self.building_class_name = None
        self.init_return_instance = None

class VirtualMachine:
    def __init__(self, inputs_list=None):
        self.stdout = []
        self.inputs_list = list(inputs_list) if inputs_list is not None else []
        self.global_env = Environment()
        self.current_frame = None
        self.init_builtins()

    def init_builtins(self):
        # 1. Custom Turkish yazdır (print)
        def varyn_yazdir(*args):
            # Print strings natively
            text = " ".join(repr(wrap_value(arg)) if isinstance(arg, OzValue) else str(arg) for arg in args)
            self.stdout.append(text + "\n")
            
        # 2. Custom Turkish girdi (input)
        def varyn_girdi(prompt=""):
            if self.inputs_list:
                val = str(self.inputs_list.pop(0))
                self.stdout.append(str(prompt) + val + "\n")
                return OzString(val)
            else:
                raise InputRequestException(str(prompt))

        # Core Built-ins
        self.global_env.define('yazdır', wrap_value(varyn_yazdir))
        self.global_env.define('yazdir', wrap_value(varyn_yazdir))
        self.global_env.define('girdi', wrap_value(varyn_girdi))
        self.global_env.define('input', wrap_value(varyn_girdi))
        
        # Native safe mappings
        self.global_env.define('uzunluk', wrap_value(lambda x: len(x.val if isinstance(x, (OzList, OzMap)) else x)))
        self.global_env.define('tam_sayı', wrap_value(lambda x: OzInt(int(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('tam_sayi', wrap_value(lambda x: OzInt(int(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('ondalık', wrap_value(lambda x: OzFloat(float(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('ondalik', wrap_value(lambda x: OzFloat(float(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('metin', wrap_value(lambda x: OzString(str(x))))
        self.global_env.define('aralık', wrap_value(lambda *args: OzList(list(range(*(a.val if isinstance(a, OzValue) else a for a in args))))))
        self.global_env.define('aralik', wrap_value(lambda *args: OzList(list(range(*(a.val if isinstance(a, OzValue) else a for a in args))))))

        # Math direct calls
        self.global_env.define('karekök', wrap_value(lambda x: OzFloat(math.sqrt(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('karekok', wrap_value(lambda x: OzFloat(math.sqrt(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('faktöriyel', wrap_value(lambda x: OzInt(math.factorial(int(x.val if isinstance(x, OzValue) else x)))))
        self.global_env.define('faktoriyel', wrap_value(lambda x: OzInt(math.factorial(int(x.val if isinstance(x, OzValue) else x)))))
        self.global_env.define('sinüs', wrap_value(lambda x: OzFloat(math.sin(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('sinus', wrap_value(lambda x: OzFloat(math.sin(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('kosinüs', wrap_value(lambda x: OzFloat(math.cos(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('kosinus', wrap_value(lambda x: OzFloat(math.cos(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('tanjant', wrap_value(lambda x: OzFloat(math.tan(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('radyan', wrap_value(lambda x: OzFloat(math.radians(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('derece', wrap_value(lambda x: OzFloat(math.degrees(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('üs', wrap_value(lambda x, y: OzFloat(math.pow(x.val if isinstance(x, OzValue) else x, y.val if isinstance(y, OzValue) else y))))
        self.global_env.define('us', wrap_value(lambda x, y: OzFloat(math.pow(x.val if isinstance(x, OzValue) else x, y.val if isinstance(y, OzValue) else y))))
        self.global_env.define('mutlak', wrap_value(lambda x: OzFloat(math.fabs(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('aşağı_yuvarla', wrap_value(lambda x: OzInt(math.floor(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('asagi_yuvarla', wrap_value(lambda x: OzInt(math.floor(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('yukarı_yuvarla', wrap_value(lambda x: OzInt(math.ceil(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('yukari_yuvarla', wrap_value(lambda x: OzInt(math.ceil(x.val if isinstance(x, OzValue) else x))))
        self.global_env.define('ebob', wrap_value(lambda x, y: OzInt(math.gcd(int(x.val if isinstance(x, OzValue) else x), int(y.val if isinstance(y, OzValue) else y)))))
        self.global_env.define('en_buyuk_ortak_bolen', wrap_value(lambda x, y: OzInt(math.gcd(int(x.val if isinstance(x, OzValue) else x), int(y.val if isinstance(y, OzValue) else y)))))
        self.global_env.define('pi_sayısı', OzFloat(math.pi))
        self.global_env.define('pi_sayisi', OzFloat(math.pi))

        # Random direct calls
        self.global_env.define('ondalık_seç', wrap_value(lambda: OzFloat(random.random())))
        self.global_env.define('ondalik_sec', wrap_value(lambda: OzFloat(random.random())))
        self.global_env.define('tamsayı_seç', wrap_value(lambda x, y: OzInt(random.randint(int(x.val if isinstance(x, OzValue) else x), int(y.val if isinstance(y, OzValue) else y)))))
        self.global_env.define('tamsayi_sec', wrap_value(lambda x, y: OzInt(random.randint(int(x.val if isinstance(x, OzValue) else x), int(y.val if isinstance(y, OzValue) else y)))))
        self.global_env.define('aralıkta_seç', wrap_value(lambda x, y: OzInt(random.randrange(int(x.val if isinstance(x, OzValue) else x), int(y.val if isinstance(y, OzValue) else y)))))
        self.global_env.define('aralikta_sec', wrap_value(lambda x, y: OzInt(random.randrange(int(x.val if isinstance(x, OzValue) else x), int(y.val if isinstance(y, OzValue) else y)))))
        self.global_env.define('seç', wrap_value(lambda x: wrap_value(random.choice(x.val if isinstance(x, OzList) else x))))
        self.global_env.define('sec', wrap_value(lambda x: wrap_value(random.choice(x.val if isinstance(x, OzList) else x))))

    def run(self, bytecode):
        self.current_frame = Frame(bytecode, self.global_env)
        
        while self.current_frame is not None:
            frame = self.current_frame
            if frame.ip >= len(frame.bytecode.instructions):
                # Implicit return of OzNull
                self.pop_frame(OzNull())
                continue
                
            opcode, operand = frame.bytecode.instructions[frame.ip]
            frame.ip += 1
            
            try:
                self.execute_instruction(opcode, operand, frame)
            except Exception as e:
                # Catch exception and try to handle it in exception_handlers stack
                handled = False
                # Traversal of current frame and previous frames to find exception handler
                curr = frame
                while curr is not None:
                    if curr.exception_handlers:
                        handler_ip = curr.exception_handlers.pop()
                        # Clean call stack up to curr
                        self.current_frame = curr
                        curr.stack.append(wrap_value(e))  # Push exception onto stack
                        curr.ip = handler_ip
                        handled = True
                        break
                    curr = curr.prev_frame
                    
                if not handled:
                    if isinstance(e, VarynError):
                        raise e
                    raise VarynError("Yürütme Hatası (RuntimeError)", f"Sanal makinede hata oluştu: {str(e)}", 1, e)

    def pop_frame(self, return_val):
        frame = self.current_frame
        prev = frame.prev_frame
        if prev is not None:
            if frame.init_return_instance is not None:
                prev.stack.append(frame.init_return_instance)
            else:
                prev.stack.append(return_val)
            self.current_frame = prev
        else:
            self.current_frame = None

    def execute_instruction(self, opcode, operand, frame):
        if opcode == 'LOAD_CONST':
            val = frame.bytecode.constants[operand]
            frame.stack.append(val)
            
        elif opcode == 'LOAD_VAR':
            val = frame.env.lookup(operand, 1)
            frame.stack.append(wrap_value(val))
            
        elif opcode == 'STORE_VAR':
            if isinstance(operand, tuple):
                name, modifier = operand
            else:
                name = operand
                modifier = None
            val = frame.stack.pop()
            frame.env.assign(name, val, 1, modifier)
            
        elif opcode == 'POP':
            frame.stack.pop()
            
        elif opcode == 'DUP':
            frame.stack.append(frame.stack[-1])
            
        elif opcode == 'BINARY_OP':
            right = frame.stack.pop()
            left = frame.stack.pop()
            res = self.perform_binary_op(left, right, operand)
            frame.stack.append(res)
            
        elif opcode == 'UNARY_OP':
            operand_val = frame.stack.pop()
            res = self.perform_unary_op(operand_val, operand)
            frame.stack.append(res)
            
        elif opcode == 'JUMP':
            frame.ip = operand
            
        elif opcode == 'JUMP_IF_FALSE':
            val = frame.stack.pop()
            is_falsy = not (val.val if isinstance(val, OzBool) else (val.to_native() if isinstance(val, OzValue) else val))
            if is_falsy:
                frame.ip = operand
                
        elif opcode == 'JUMP_IF_TRUE':
            val = frame.stack.pop()
            is_truthy = bool(val.val if isinstance(val, OzBool) else (val.to_native() if isinstance(val, OzValue) else val))
            if is_truthy:
                frame.ip = operand
                
        elif opcode == 'MAKE_LIST':
            elts = []
            for _ in range(operand):
                elts.append(frame.stack.pop())
            elts.reverse()
            frame.stack.append(OzList(elts))
            
        elif opcode == 'MAKE_MAP':
            keys = []
            vals = []
            for _ in range(operand):
                v = frame.stack.pop()
                k = frame.stack.pop()
                keys.append(k)
                vals.append(v)
            keys.reverse()
            vals.reverse()
            # Build dict map
            d = dict(zip(keys, vals))
            frame.stack.append(OzMap(d))
            
        elif opcode == 'LOAD_INDEX':
            index = frame.stack.pop()
            obj = frame.stack.pop()
            if isinstance(obj, (OzList, OzMap, OzString)):
                try:
                    res = obj[index]
                    frame.stack.append(wrap_value(res))
                except Exception as e:
                    raise VarynError("Dizin Hatası (IndexError)", f"Sınır dışı erişim veya geçersiz anahtar: {str(e)}", 1)
            else:
                obj_native = obj.to_native() if isinstance(obj, OzValue) else obj
                idx_native = index.to_native() if isinstance(index, OzValue) else index
                try:
                    res = obj_native[idx_native]
                    frame.stack.append(wrap_value(res))
                except Exception as e:
                    raise VarynError("Dizin Hatası (IndexError)", f"Sınır dışı erişim veya geçersiz anahtar: {str(e)}", 1)
                
        elif opcode == 'STORE_INDEX':
            index = frame.stack.pop()
            obj = frame.stack.pop()
            val = frame.stack.pop()
            if isinstance(obj, (OzList, OzMap)):
                try:
                    obj[index] = val
                except Exception as e:
                    raise VarynError("Tür Hatası (TypeError)", f"Endeks ataması başarısız: {str(e)}", 1)
            else:
                obj_native = obj.to_native() if isinstance(obj, OzValue) else obj
                idx_native = index.to_native() if isinstance(index, OzValue) else index
                try:
                    obj_native[idx_native] = val.to_native() if isinstance(val, OzValue) else val
                except Exception as e:
                    raise VarynError("Tür Hatası (TypeError)", f"Endeks ataması başarısız: {str(e)}", 1)
                
        elif opcode == 'LOAD_ATTR':
            obj = frame.stack.pop()
            attr = operand
            if isinstance(obj, OzInstance):
                frame.stack.append(wrap_value(obj.get_attr(attr)))
            elif isinstance(obj, OzValue) and hasattr(obj, 'get_attr'):
                try:
                    frame.stack.append(wrap_value(obj.get_attr(attr)))
                except AttributeError:
                    native_obj = obj.to_native()
                    res = get_attribute(native_obj, attr, 1)
                    frame.stack.append(wrap_value(res))
            else:
                native_obj = obj.to_native() if isinstance(obj, OzValue) else obj
                res = get_attribute(native_obj, attr, 1)
                frame.stack.append(wrap_value(res))
                
        elif opcode == 'STORE_ATTR':
            obj = frame.stack.pop()
            val = frame.stack.pop()
            attr = operand
            if isinstance(obj, OzInstance):
                obj.set_attr(attr, val)
            elif isinstance(obj, OzValue) and hasattr(obj, 'set_attr'):
                obj.set_attr(attr, val)
            else:
                native_obj = obj.to_native() if isinstance(obj, OzValue) else obj
                try:
                    setattr(native_obj, attr, val.to_native() if isinstance(val, OzValue) else val)
                except Exception as e:
                    raise VarynError("Öznitelik Hatası (AttributeError)", f"Öznitelik ataması başarısız: {str(e)}", 1)
                    
        elif opcode == 'GET_ITER':
            coll = frame.stack.pop()
            coll_native = coll.val if isinstance(coll, OzList) else (coll.to_native() if isinstance(coll, OzValue) else coll)
            try:
                iterator = iter(coll_native)
                frame.stack.append(iterator)
            except Exception:
                raise VarynError("Tür Hatası (TypeError)", "Döngü kurulamaz, veri yinelenebilir (iterable) değil.", 1)
                
        elif opcode == 'FOR_ITER':
            iterator = frame.stack[-1]
            try:
                next_val = next(iterator)
                frame.stack.append(wrap_value(next_val))
            except StopIteration:
                frame.stack.pop()  # Pop iterator
                frame.ip = operand  # Jump to end of loop
                
        elif opcode == 'POP_ITER':
            frame.stack.pop()
            
        elif opcode == 'MAKE_FUNCTION':
            func_bytecode = frame.bytecode.constants[operand]
            func_obj = OzFunction(
                name=func_bytecode.name,
                args=func_bytecode.arg_names,
                body=None,
                env=frame.env,
                interpreter=self
            )
            func_obj.bytecode = func_bytecode
            frame.stack.append(func_obj)
            
        elif opcode == 'MAKE_CLASS':
            class_name, class_bytecode_idx = operand
            class_bytecode = frame.bytecode.constants[class_bytecode_idx]
            
            # Execute class body inside its own sub-environment
            class_env = Environment(frame.env)
            class_frame = Frame(class_bytecode, class_env, return_ip=frame.ip, prev_frame=frame)
            class_frame.building_class_name = class_name
            self.current_frame = class_frame
            
        elif opcode == 'RETURN_CLASS_NAMESPACE':
            class_name = frame.building_class_name
            methods = frame.env.values
            klass_obj = OzClass(class_name, methods, self)
            
            # Pop class construction frame and push class object to parent frame stack
            self.pop_frame(klass_obj)
            
        elif opcode == 'CALL':
            num_args = operand
            callable_obj = frame.stack.pop()
            
            args = [frame.stack.pop() for _ in range(num_args)]
            args.reverse()
            
            if isinstance(callable_obj, OzFunction):
                local_env = Environment(callable_obj.env)
                for arg_name, arg_val in zip(callable_obj.args, args):
                    local_env.define(arg_name, wrap_value(arg_val))
                new_frame = Frame(callable_obj.bytecode, local_env, return_ip=frame.ip, prev_frame=frame)
                self.current_frame = new_frame
                
            elif isinstance(callable_obj, OzClass):
                instance = OzInstance(callable_obj)
                init_method = callable_obj.methods.get('__init__')
                if init_method:
                    local_env = Environment(init_method.env)
                    if len(init_method.args) > 0:
                        local_env.define(init_method.args[0], instance)
                        for arg_name, arg_val in zip(init_method.args[1:], args):
                            local_env.define(arg_name, wrap_value(arg_val))
                    else:
                        for arg_name, arg_val in zip(init_method.args, args):
                            local_env.define(arg_name, wrap_value(arg_val))
                    new_frame = Frame(init_method.bytecode, local_env, return_ip=frame.ip, prev_frame=frame)
                    new_frame.init_return_instance = instance
                    self.current_frame = new_frame
                else:
                    frame.stack.append(instance)
                    
            elif isinstance(callable_obj, OzBoundMethod):
                method = callable_obj.method
                instance = callable_obj.instance
                local_env = Environment(method.env)
                if len(method.args) > 0:
                    local_env.define(method.args[0], instance)
                    for arg_name, arg_val in zip(method.args[1:], args):
                        local_env.define(arg_name, wrap_value(arg_val))
                else:
                    for arg_name, arg_val in zip(method.args, args):
                        local_env.define(arg_name, wrap_value(arg_val))
                new_frame = Frame(method.bytecode, local_env, return_ip=frame.ip, prev_frame=frame)
                self.current_frame = new_frame
                
            elif isinstance(callable_obj, OzNativeCallable):
                res = callable_obj.call(args)
                frame.stack.append(res)
                
            elif callable(callable_obj):
                native_args = [v.to_native() if isinstance(v, OzValue) else v for v in args]
                res = callable_obj(*native_args)
                frame.stack.append(wrap_value(res))
            else:
                raise VarynError("Tür Hatası (TypeError)", f"'{callable_obj}' nesnesi çağrılamaz.", 1)
                
        elif opcode == 'RETURN':
            val = frame.stack.pop()
            self.pop_frame(val)
            
        elif opcode == 'SETUP_EXCEPT':
            frame.exception_handlers.append(operand)
            
        elif opcode == 'POP_EXCEPT':
            if frame.exception_handlers:
                frame.exception_handlers.pop()
                
        elif opcode == 'CHECK_EXCEPTION_TYPE':
            exc = frame.stack[-1]
            if isinstance(exc, OzValue):
                exc_unwrapped = exc.to_native()
                if exc_unwrapped is None:
                    exc_unwrapped = exc
            else:
                exc_unwrapped = exc
            is_match = check_exception_match(exc_unwrapped, operand)
            frame.stack.append(OzBool(is_match))
            
        elif opcode == 'CLEAR_EXCEPTION':
            # Pops exception object and clears handling status if still on stack
            # Since exception was already bound or popped in handler bytecode, we just pass safely
            pass
            
        elif opcode == 'RERAISE_EXCEPTION':
            exc = frame.stack.pop()
            raise exc.to_native() if isinstance(exc, OzValue) else exc
            
        elif opcode == 'IMPORT_PACKAGE':
            # Import a package dynamically!
            pkg_name = operand
            from .package_loader import load_external_package
            pkg_exports = load_external_package(pkg_name, 1, self.stdout)
            frame.env.define(pkg_name, wrap_value(pkg_exports))

    def perform_binary_op(self, left, right, op):
        left_native = left.to_native() if isinstance(left, OzValue) else left
        right_native = right.to_native() if isinstance(right, OzValue) else right
        try:
            if op == '+': res = left_native + right_native
            elif op == '-': res = left_native - right_native
            elif op == '*': res = left_native * right_native
            elif op in ('/', '%'):
                if right_native == 0:
                    raise VarynError("Sıfıra Bölme Hatası (ZeroDivisionError)", "Bir sayı sıfıra bölünemez veya mod alınamaz.", 1)
                if op == '/':
                    res = left_native / right_native
                else:
                    res = left_native % right_native
            elif op == '**': res = left_native ** right_native
            elif op == '==': res = left_native == right_native
            elif op == '!=': res = left_native != right_native
            elif op == '<': res = left_native < right_native
            elif op == '>': res = left_native > right_native
            elif op == '<=': res = left_native <= right_native
            elif op == '>=': res = left_native >= right_native
            else:
                raise VarynError("Tür Hatası (TypeError)", f"Bilinmeyen operatör '{op}'", 1)
            return wrap_value(res)
        except Exception as e:
            if isinstance(e, VarynError):
                raise e
            raise VarynError("Tür Hatası (TypeError)", f"'{op}' işlemi için uyumsuz veri türleri ({getattr(left, 'get_type_name', lambda: type(left).__name__)()} ve {getattr(right, 'get_type_name', lambda: type(right).__name__)()})", 1)

    def perform_unary_op(self, val, op):
        val_native = val.to_native() if isinstance(val, OzValue) else val
        try:
            if op == '+': res = +val_native
            elif op == '-': res = -val_native
            elif op in ('değil', 'not'): res = not val_native
            else:
                raise VarynError("Tür Hatası (TypeError)", f"Bilinmeyen tekli operatör '{op}'", 1)
            return wrap_value(res)
        except Exception as e:
            raise VarynError("Tür Hatası (TypeError)", f"'{op}' işlemi için uyumsuz veri türü ({getattr(val, 'get_type_name', lambda: type(val).__name__)()})", 1)

    # For evaluating standard Program/AST directly
    def eval(self, ast_root, env=None):
        from .bytecode_compiler import BytecodeCompiler
        compiler = BytecodeCompiler()
        bytecode = compiler.compile_program(ast_root)
        self.run(bytecode)
