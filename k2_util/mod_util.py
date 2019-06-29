import logging
import importlib
from inspect import signature, Parameter
from _collections import OrderedDict
from os import listdir
from os.path import basename, isdir, isfile, exists, dirname
import pkgutil


logger = logging.getLogger(__name__)
info = logger.info
debug = logger.debug

class MemberNotFound(Exception):
    pass

class MemberNotUnique(Exception):
    pass

class ModName(object):
    def __init__(self, name):
        self.name = name
        
    def to_dict(self):
        return self.name

    def __str__(self):
        return (self.name)
    
    def __repr__(self):
        return (self.name)
    
class Mod(object):
    
    name = ''
    description = ''
    file = ''
    members = []
    modules = []
    
    def __init__(self, module, **kw):
        
        self.name = module.__name__
        self.description = module.__doc__
        self.file = module.__file__
        self.members = kw.get('members', [])
        for member in self.members:
            setattr(member, 'module', self)
        self.modules = []
        if hasattr(module, '__path__'):
            for _, modname, _ in pkgutil.iter_modules(module.__path__):
                if modname[0] != '_':
                    if kw.get('recurse', False):
                        sub_mod = importlib.import_module('.'.join([self.name, modname]))
                        self.modules.append(Mod(sub_mod, **kw))
                    else:
                        self.modules.append(ModName(modname))
        
            
        
    def add_member(self, member):
        setattr(member, 'module', self)
        self.members.append(member)
        return member
    
    def basename(self):
        return self.name.split('.')[-1]
    
    def package_name(self):
        return '.'.join(self.name.split('.')[:-1])
    
    def package(self):
        if self.package_name():
            pack = importlib.import_module(self.package_name())
            return scan(pack)
        
    def get_member(self, **kw):
        find = self.find_members(**kw)
        if len(find) == 1:
            return find[0]
        if len(find) == 0:
            raise MemberNotFound(
                'The supplied filter {filter} did not match any members'.format(
                    filter=kw
                    )
                )
        else:
            raise MemberNotUnique(
                'The supplied filter {filter} did not match a unique member'.format(
                    filter=kw
                    )
                )
        
    def find_members(self, **kw):
        find = []
        for member in self.members:
            match = True
            for filter, value in kw.items():
                if '__' in filter:
                    name, operator = filter.split('__')
                else:
                    name, operator = (filter, None)
                if hasattr(member, name):
                    member_value = getattr(member, name)
                    if operator:
                        if operator not in [
                            'startswith',
                            'endswith',
                            'contains'
                            ]:
                            raise ValueError("The supplied operator '{o}' is not recognised".format(
                                o=operator))
                        if operator == 'startswith' and member_value[:len(value)] != value:
                                match=False
                                continue
                        if operator == 'endswith' and member_value[-len(value):] != value:
                                match=False
                                continue
                        if operator == 'contains' and value not in member_value:
                                match=False
                                continue
                    else:
                        if member_value != value:
                            match = False
                            continue
            if match:
                find.append(member)
        return find
        
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'file': self.file,
            'members': [m.to_dict() for m in self.members],
            'modules': [m.to_dict() for m in self.modules]
            }
    

class ModMember(object):
    
    class MemberTypes():
        INTEGER = 'int'
        FLOAT = 'float'
        BOOLEAN = 'bool'
        STRING = 'str'
        LIST = 'list'
        TUPLE = 'tuple'
        DICT = 'dict'
        FUNCTION = 'function'
        CLASS = 'type'
        
    name = ''
    type = ''
    description = ''
    module = None
    function = None
    cls = None
    
    def __init__(self, *args, **kw):
        self.name = kw.get('name', ModMember.name)
        self.type = kw.get('type', ModMember.type)
        self.description = kw.get('description', ModMember.description)
        self.function = kw.get('function', ModMember.function)
        self.cls = kw.get('cls', ModMember.cls)
        self.module = kw.get('module', ModMember.module)
        if self.module and isinstance(self.module, Mod):
            self.module.add_member(self)
        
        
    def to_dict(self):
        resp = {
            'name': self.name,
            'type': self.type,
            'description': self.description
            }
        if self.type == ModMember.MemberTypes.FUNCTION and self.function:
            resp['function'] = self.function if isinstance(self.function, dict) else self.function.to_dict()
        if self.type == ModMember.MemberTypes.CLASS and self.cls:
            resp['class'] = self.cls if isinstance(self.cls, dict) else self.cls.to_dict()
        return resp
    
class ModParameter(object):
    def __init__(self, parameter):
        self.kind = str(parameter.kind)
        if parameter.annotation == Parameter.empty:
            self.type = None
        else:
            if parameter.annotation.__module__ == 'builtins':
                self.type = parameter.annotation.__name__
            else:    
                self.type = '{m}.{t}'.format(m=parameter.annotation.__module__, t=parameter.annotation.__name__)
        if parameter.default == Parameter.empty:
            self.default = None
        else:
            self.default = str(parameter.default)
        
    def to_dict(self):
        return {
            'kind': self.kind,
            'default': self.default,
            'type': self.type
            }
    
class ModFunction(object):
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        self.description = func.__doc__
        self.type = ModMember.MemberTypes.FUNCTION
        sig = signature(func)
        self.parameters = {}
        for name, parameter in sig.parameters.items():
            self.parameters[name] = ModParameter(parameter)
        
    def to_dict(self):
        parms = {}
        for name, param in self.parameters.items():
            parms[name] = param.to_dict()
        return {
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'parameters': parms
            }
    
class ModClass(object):
    def __init__(self, cls):
        self.cls = cls
        self.name = cls.__name__
        self.members = []
        self.type = _member_to_member_type(cls)
        self.description = _member_to_description(cls)
        for member_name in dir(cls):
            debug('Found member of class {mod}.{cls}.{member}'.format(
                mod=cls.__module__,
                cls=cls.__name__, 
                member=member_name))
            if member_name[0] == '_':
                debug('Skipping private member of class {mod}.{cls}.{member}'.format(
                    mod=cls.__module__,
                    cls=cls.__name__, 
                    member=member_name))
            else:
                member = getattr(cls, member_name)
                mod_member = ModMember(
                    name=member_name,
                    type=_member_to_member_type(member),
                    description=_member_to_description(member),
                    )
                if mod_member.type == ModMember.MemberTypes.FUNCTION:
                    mod_member.function = ModFunction(member)
                if mod_member.type == ModMember.MemberTypes.CLASS:
                    mod_member.cls = ModClass(member)
                self.add_member(mod_member)

    def add_member(self, member):
        setattr(member, 'module', self)
        self.members.append(member)
        return member
        
    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'members': [m.to_dict() for m in self.members]
            }
    

def _member_to_member_type(member):
    type_str = type(member).__name__
#    debug('Type of: {var} is {type_str}'.format(
#        var=member,
#        type_str=type_str))
    for t in dir(ModMember.MemberTypes):
#        debug('Checking type is MemberTypes.{t}'.format(t=t))
        if t[0] != '_':
            check_type = getattr(ModMember.MemberTypes, t)
#            debug('Checking {type_str} == {check_type}'.format(
#                type_str=type_str,
#                check_type=check_type
#                ))
            if type_str == check_type:
#                debug('Type of: {var} is MemberTypes.{t}'.format(
#                    var=member,
#                    t=t))
                return type_str
    member_type = '{module}.{cls}'.format(
        module=member.__class__.__module__,
        cls=member.__class__.__name__
        )
#    debug('Type of: {var} is {type}'.format(var=member, type=member_type))
    return member_type

def _member_to_description(member):
    if _member_to_member_type(member) == ModMember.MemberTypes.BOOLEAN:
        return 'A boolean value'
    if _member_to_member_type(member) == ModMember.MemberTypes.INTEGER:
        return 'An integer value'
    if _member_to_member_type(member) == ModMember.MemberTypes.FLOAT:
        return 'A float value'
    if _member_to_member_type(member) == ModMember.MemberTypes.STRING:
        return 'A string value'
    if _member_to_member_type(member) == ModMember.MemberTypes.LIST:
        return 'A list value'
    if _member_to_member_type(member) == ModMember.MemberTypes.TUPLE:
        return 'A tuple value'
    if _member_to_member_type(member) == ModMember.MemberTypes.DICT:
        return 'A dictionary value'
    if _member_to_member_type(member) == ModMember.MemberTypes.FUNCTION:
        if member.__doc__ and len(member.__doc__) > 0:
            return member.__doc__
        return 'An undocumented function'
    if _member_to_member_type(member) == ModMember.MemberTypes.CLASS:
        if member.__doc__ and len(member.__doc__) > 0:
            return member.__doc__
        return 'An undocumented class'
    if member.__doc__ and len(member.__doc__) > 0:
        return 'An instance of {type}.\n{doc}'.format(
            type=_member_to_member_type(member),
            doc=member.__doc__)
    return 'An instance of an undocumented class'
        


def scan(module, **kw):
    debug('Scanning module {mod}'.format(mod=module.__name__))
    mod = Mod(module, **kw)
    for member_name in dir(module):
        debug('Found member {mod}.{member}'.format(mod=mod.name, member=member_name))
        if member_name[0] == '_':
            debug('Skipping private member {mod}.{member}'.format(mod=mod.name, member=member_name))
        else:
            member = getattr(module, member_name)
            mod_member = ModMember(
                name=member_name,
                type=_member_to_member_type(member),
                description=_member_to_description(member),
                )
            if mod_member.type == ModMember.MemberTypes.FUNCTION:
                mod_member.function = ModFunction(member)
            if mod_member.type == ModMember.MemberTypes.CLASS:
                mod_member.cls = ModClass(member)
            mod_member = mod.add_member(mod_member)
    return mod
        
    